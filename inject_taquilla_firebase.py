import os
import re

TAQUILLA_HTML_PATH = 'admin_AsteriscoSiete-server/admin_AsteriscoSiete7/admin_asterisco7/templates/taquilla/index.html'

def process_taquilla():
    with open(TAQUILLA_HTML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Firebase script module at the end of <head> or anywhere if missing
    if 'firebase-auth.js' not in content:
        firebase_module_tag = '\n    <script type="module" src="/static/arrejuntao/firebase-auth.js"></script>\n'
        content = content.replace('</head>', f'{firebase_module_tag}</head>')

    # 2. Add Google button to the UI if not there
    google_btn_html = """
              <!-- Separador -->
              <div class="relative flex py-4 items-center w-full">
                  <div class="flex-grow border-t border-slate-300 dark:border-slate-700"></div>
                  <span class="flex-shrink-0 mx-4 text-slate-400 text-xs font-bold uppercase">O entra con</span>
                  <div class="flex-grow border-t border-slate-300 dark:border-slate-700"></div>
              </div>

              <!-- Google Login -->
              <button onclick="if(window.loginConGoogle) window.loginConGoogle(); else alert('Módulo de Firebase cargando...')"
                  class="w-full relative flex items-center justify-center gap-3 bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-600 text-slate-700 dark:text-white font-bold py-3 rounded-xl shadow-sm transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                  <img src="https://www.svgrepo.com/show/475656/google-color.svg" class="w-5 h-5" alt="Google">
                  <span class="text-sm">Continuar con Google</span>
              </button>
              
              <!-- Registrarse Link -->
              <div class="mt-6 text-center">
                  <p class="text-xs text-slate-500 dark:text-slate-400">¿No tienes cuenta? <a href="#" onclick="alert('Contacta al administrador para habilitar un Cajero/Taquilla.')" class="text-indigo-500 hover:text-indigo-400 font-bold transition-colors">Solicitar Registro</a></p>
              </div>"""
    
    if "Continuar con Google" not in content:
        content = content.replace('INGRESAR\n              </button>', f'INGRESAR\n              </button>{google_btn_html}')

    # 3. Rewrite attemptLogin() so that it uses window.loginConEmail(...) and removes /taquilla/login/ POST
    # We will just replace attemptLogin content since it's hard to regex perfectly. 
    # Or just write a small shim inside attemptLogin.

    attempt_login_func = """async function attemptLogin() {
            const user = (document.getElementById('login-user-input').value || '').trim();
            const pass = (document.getElementById('login-pass-input').value || '').trim();
            const errEl = document.getElementById('login-error-msg');
            const btn   = document.getElementById('login-submit-btn');

            errEl.classList.add('hidden');
            errEl.textContent = '';

            if (!user || !pass) {
                errEl.textContent = 'Ingresa usuario (correo) y contraseña.';
                errEl.classList.remove('hidden');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Verificando...';

            if (window.loginConEmail) {
                // Firebase Login wrapper
                window.loginConEmail(user, pass);
                setTimeout(() => {
                    btn.disabled = false;
                    btn.textContent = 'INGRESAR';
                }, 2000);
            } else {
                errEl.textContent = 'Módulo de autenticación no cargado.';
                errEl.classList.remove('hidden');
                btn.disabled = false;
                btn.textContent = 'INGRESAR';
            }
        }"""

    # We replace the old attemptLogin with the newly authored one using regex.
    # The old attemptLogin goes from "async function attemptLogin() {" to "}" just before "function showTaquillaDashboard" 
    import re
    content = re.sub(r'async function attemptLogin\(\) \{.*?\n\s+function openReportesModal', attempt_login_func + '\n\n        function openReportesModal', content, flags=re.DOTALL)

    # 4. In order to handle Firebase session mapping properly, Firebase handles its state on AuthStateChanged. 
    # Let's ensure when user logs in via firebase, we close the modal.
    # We can inject a listener inside <script> at the bottom.
    firebase_listener = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // Check Firebase status periodically to close modal if logged in
            setInterval(() => {
                const user = sessionStorage.getItem('ast7_user');
                const token = sessionStorage.getItem('ast7_token');
                
                if (user && token && typeof window.firebase !== 'undefined' && window.firebase.auth().currentUser) {
                    const loginModal = document.getElementById('login-modal');
                    if (loginModal && !loginModal.classList.contains('hidden')) {
                         loginModal.classList.add('hidden');
                         // Save user globally
                         window.logged_user = window.firebase.auth().currentUser;
                         document.getElementById('system-title').innerHTML = `TAQUILLA • Arrejuntao <span class="text-indigo-400 text-xs ml-2 uppercase opacity-80 font-bold tracking-widest">[CAJERO: ${window.logged_user.email}]</span>`;
                    }
                }
            }, 1000);
            
            // Add interceptor to fetch requests to automatically send the Firebase Token!
            const originalFetch = window.fetch;
            window.fetch = async function() {
                let [resource, config] = arguments;
                const token = sessionStorage.getItem('ast7_token');
                if (token) {
                    if (!config) config = {};
                    if (!config.headers) config.headers = {};
                    config.headers['Authorization'] = 'Bearer ' + token;
                }
                return originalFetch(resource, config);
            };
        });
    </script>
    """
    if "setInterval(() => {" not in content:
        content = content.replace('</body>', f'{firebase_listener}\n</body>')

    with open(TAQUILLA_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Taquilla template updated with Firebase Auth.")

if __name__ == '__main__':
    process_taquilla()

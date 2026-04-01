// ═══════════════════════════════════════════════════════════
//  firebase-auth.js  –  Autenticación EL ARREJUNTAO
// ═══════════════════════════════════════════════════════════

import { auth, googleProvider } from "./firebase.js";
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  signInWithRedirect,
  getRedirectResult,
  signOut,
  sendPasswordResetEmail,
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";

import { initFirestore } from "./firestore-sync.js";

// ── UI: referencias ──────────────────────────────────────────
const loginScreen  = document.getElementById("login-screen");
const appContent   = document.getElementById("app-content");
const loginEmail   = document.getElementById("login-email");
const loginPass    = document.getElementById("login-pass");
const loginError   = document.getElementById("login-error");
const loginSpinner = document.getElementById("login-spinner");
const userBadge    = document.getElementById("user-badge");

// ── UID del administrador ─────────────────────────────────────
const ADMIN_UID = "akNzRVKB0JbQ1RtEIwCwx5zmYLR2";

// ── Helpers ──────────────────────────────────────────────────
function showAuthError(msg) {
  if (loginError) {
    loginError.textContent = msg;
    loginError.style.display = "block";
  }
  console.error("Auth error:", msg);
}

function clearError() {
  if (loginError) loginError.style.display = "none";
}

function setLoading(on) {
  if (loginSpinner) loginSpinner.style.display = on ? "flex" : "none";
  document.querySelectorAll(".auth-btn").forEach(b => { b.disabled = on; });
}

// ── Traducción de errores Firebase ──────────────────────────
function traducirError(code) {
  const map = {
    "auth/invalid-email":             "El correo electrónico no es válido.",
    "auth/user-not-found":            "No existe una cuenta con este correo.",
    "auth/wrong-password":            "Contraseña incorrecta.",
    "auth/email-already-in-use":      "Este correo ya está registrado.",
    "auth/weak-password":             "La contraseña debe tener al menos 6 caracteres.",
    "auth/popup-closed-by-user":      "Cerraste la ventana de Google. Intenta de nuevo.",
    "auth/popup-blocked":             "El navegador bloqueó la ventana. Permite ventanas emergentes.",
    "auth/network-request-failed":    "Error de red. Comprueba tu conexión.",
    "auth/too-many-requests":         "Demasiados intentos. Espera un momento.",
    "auth/invalid-credential":        "Credenciales incorrectas. Verifica tu correo y contraseña.",
    "auth/unauthorized-domain":       "Dominio no autorizado. Contacta al administrador.",
    "auth/operation-not-allowed":     "Método de inicio de sesión no habilitado en Firebase.",
    "auth/cancelled-popup-request":   "Solicitud cancelada. Intenta de nuevo.",
    "auth/account-exists-with-different-credential": "Ya existe una cuenta con este correo usando otro método.",
  };
  return map[code] || `Error (${code}). Intenta de nuevo.`;
}

// ── Estado de Auth ───────────────────────────────────────────
onAuthStateChanged(auth, async (user) => {
  if (user) {
    // Usuario autenticado → mostrar app
    if (loginScreen) loginScreen.style.display = "none";
    if (appContent)  appContent.style.display  = "";
    setLoading(false);

    const isAdmin = user.uid === ADMIN_UID;
    if (userBadge) {
      userBadge.textContent = isAdmin
        ? "👑 " + (user.displayName || user.email || "Admin")
        : (user.email || user.displayName || "Usuario");
      userBadge.title = user.uid;
      if (isAdmin) {
        userBadge.style.background  = "rgba(245,208,32,0.15)";
        userBadge.style.borderColor = "rgba(245,208,32,0.4)";
        userBadge.style.color       = "#f5d020";
      }
    }

    // Inicializar Firestore
    try { await initFirestore(user.uid); } catch(e) { console.warn("Firestore init:", e); }

  } else {
    // Sin sesión → mostrar pantalla de login
    if (loginScreen) loginScreen.style.display = "";
    if (appContent)  appContent.style.display  = "none";
    setLoading(false);
  }
});

// ── Capturar resultado del redirect de Google ────────────────
(async () => {
  try {
    const result = await getRedirectResult(auth);
    if (result?.user) {
      console.log("✅ Google redirect login:", result.user.email);
    }
  } catch (e) {
    if (e.code && !["auth/null-user", "auth/no-auth-event"].includes(e.code)) {
      console.error("Redirect result error:", e.code);
      showAuthError(traducirError(e.code));
    }
  }
})();

// ── Acciones públicas ─────────────────────────────────────────
window.loginConEmail = async function() {
  const email = loginEmail?.value.trim();
  const pass  = loginPass?.value;
  if (!email || !pass) { showAuthError("Completa el correo y la contraseña."); return; }
  clearError();
  setLoading(true);
  try {
    await signInWithEmailAndPassword(auth, email, pass);
  } catch (e) {
    showAuthError(traducirError(e.code));
    setLoading(false);
  }
};

window.registrarse = async function() {
  const email = loginEmail?.value.trim();
  const pass  = loginPass?.value;
  if (!email || !pass) { showAuthError("Completa el correo y la contraseña."); return; }
  if (pass.length < 6) { showAuthError("La contraseña debe tener al menos 6 caracteres."); return; }
  clearError();
  setLoading(true);
  try {
    await createUserWithEmailAndPassword(auth, email, pass);
  } catch (e) {
    showAuthError(traducirError(e.code));
    setLoading(false);
  }
};

window.loginConGoogle = async function() {
  clearError();
  setLoading(true);
  try {
    // Intentar popup primero; si falla por bloqueo, usar redirect
    await signInWithPopup(auth, googleProvider);
  } catch (e) {
    if (e.code === "auth/popup-blocked" || e.code === "auth/popup-closed-by-user") {
      // Fallback a redirect
      try {
        await signInWithRedirect(auth, googleProvider);
      } catch (e2) {
        showAuthError(traducirError(e2.code));
        setLoading(false);
      }
    } else {
      showAuthError(traducirError(e.code));
      setLoading(false);
    }
  }
};

window.cerrarSesion = async function() {
  await signOut(auth);
};

window.resetPassword = async function(email) {
  if (!email) return;
  try {
    await sendPasswordResetEmail(auth, email);
    alert("✉️ Correo de recuperación enviado a " + email);
  } catch (e) {
    alert("Error: " + traducirError(e.code));
  }
};

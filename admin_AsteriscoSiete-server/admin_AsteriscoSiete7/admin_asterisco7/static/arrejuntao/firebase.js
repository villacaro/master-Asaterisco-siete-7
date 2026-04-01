// ═══════════════════════════════════════════════════════════
//  firebase.js  –  Configuración de Firebase para EL ARREJUNTAO
//  ⚠️  RELLENA los valores de tu proyecto en Firebase Console
//     Configuración → Tus apps → (selecciona la app web) → SDK
// ═══════════════════════════════════════════════════════════

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// ────────────────────────────────────────────────
//  🔴 REEMPLAZA ESTOS VALORES CON LOS DE TU PROYECTO
// ────────────────────────────────────────────────
const firebaseConfig = {
  apiKey:            "AIzaSyBiWv7Zrn0UUoqTm-oq_84761SvOzEBAM0",
  authDomain:        "app-el-arrejuntao.firebaseapp.com",
  projectId:         "app-el-arrejuntao",
  storageBucket:     "app-el-arrejuntao.firebasestorage.app",
  messagingSenderId: "578381240300",
  appId:             "1:578381240300:web:e63b553ac5cfd8606e92c9",
  measurementId:     "G-5KRM2KCPEY"
};
// ────────────────────────────────────────────────

const app            = initializeApp(firebaseConfig);
export const auth    = getAuth(app);
export const db      = getFirestore(app);
export const googleProvider = new GoogleAuthProvider();

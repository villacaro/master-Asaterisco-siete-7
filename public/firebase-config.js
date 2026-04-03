// Importar las funciones que necesitas de los SDKs que requieras
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";
import { getMessaging } from "firebase/messaging";
// TODO: Agregar los SDKs de los productos de Firebase que quieras usar
// https://firebase.google.com/docs/web/setup#available-libraries

// Configuración de tu aplicación web de Firebase
// Para Firebase JS SDK v7.20.0 y posteriores, measurementId es opcional
const firebaseConfig = {
  apiKey: "AIzaSyDQs4cEW8JWHxiZqp_MiNojRwuCV_jMtj4",
  authDomain: "app-asterisco-siete.firebaseapp.com",
  projectId: "app-asterisco-siete",
  storageBucket: "app-asterisco-siete.firebasestorage.app",
  messagingSenderId: "256057006492",
  appId: "1:256057006492:web:bebf76680c470f3bb41059",
  measurementId: "G-ZLV057XQHX"
};

// Inicializar Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Exportar servicios adicionales
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);
export const messaging = getMessaging(app);

export { app, analytics };

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
  apiKey: "AIzaSyB-Zb4ncXbgT0OAo3sN-K9hnAIifNmYMxE",
  authDomain: "asterisco-siete.firebaseapp.com",
  databaseURL: "https://asterisco-siete.firebaseio.com",
  projectId: "asterisco-siete",
  storageBucket: "asterisco-siete.firebasestorage.app",
  messagingSenderId: "653707713955",
  appId: "1:653707713955:web:9d0b5d5d66883cdbfbce16",
  measurementId: "G-PYTWSFTXW8"
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

// ═══════════════════════════════════════════════════════════
//  fcm-init.js  –  Firebase Cloud Messaging para EL ARREJUNTAO
//  Solicita permiso y guarda el token FCM del usuario en Firestore
// ═══════════════════════════════════════════════════════════

import { db } from "./firebase.js";
import { doc, setDoc, serverTimestamp }
  from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
import { getMessaging, getToken, onMessage }
  from "https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging.js";

const VAPID_KEY = "BLBz7yXJCq8sD8q2pKpWE7g3bRn7yXRhfGkQVcP8KNDF3yvNNnBQ_mFnXSf5Z0Tg7yP_IFPe4GMOFqJKkuqHuA";

let messaging = null;

export async function iniciarFCM(uid) {
  if (!("Notification" in window)) return;

  try {
    messaging = getMessaging();

    // Pedir permiso si no está concedido
    if (Notification.permission !== "granted") {
      const perm = await Notification.requestPermission();
      if (perm !== "granted") return;
    }

    // Obtener token del dispositivo
    const token = await getToken(messaging, {
      vapidKey: VAPID_KEY,
      serviceWorkerRegistration: await navigator.serviceWorker.ready
    });

    if (token) {
      // Guardar token en Firestore asociado al usuario
      await setDoc(doc(db, "fcm_tokens", uid), {
        token,
        uid,
        updatedAt: serverTimestamp()
      }, { merge: true });
      console.log("✅ FCM token guardado");
    }

    // Notificaciones en primer plano
    onMessage(messaging, (payload) => {
      const { title, body } = payload.notification || {};
      if (title) {
        // Mostrar toast personalizado
        if (typeof window.toast === "function") {
          window.toast(`🔔 ${title}: ${body || ""}`, false);
        } else {
          const n = new Notification(title, { body, icon: "/elarrejuntao.png" });
        }
      }
    });

  } catch (e) {
    console.warn("FCM error:", e.message);
  }
}

// Mostrar notificación local inmediata (sin push)
export function notificarLocal(titulo, cuerpo) {
  if (Notification.permission === "granted") {
    new Notification(titulo, {
      body: cuerpo,
      icon: "/elarrejuntao.png",
      badge: "/elarrejuntao.png"
    });
  }
}

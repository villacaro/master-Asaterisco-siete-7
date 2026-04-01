// ═══════════════════════════════════════════════════════════
//  firestore-sync.js  –  Sincronización de datos con Firestore
//  Reemplaza localStorage con Firestore manteniendo la misma API
// ═══════════════════════════════════════════════════════════

import { db } from "./firebase.js";
import {
  collection, doc,
  addDoc, setDoc, updateDoc, deleteDoc, getDoc, getDocs,
  onSnapshot, serverTimestamp, query, orderBy, writeBatch
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

let currentUid = null;
let _unsubResultados   = null;
let _unsubApuestas     = null;
let _unsubAniApuestas  = null;

// ── Refs helpers ─────────────────────────────────────────────
const clientesRef  = () => collection(db, "usuarios", currentUid, "clientes");
const apuestasRef  = () => collection(db, "usuarios", currentUid, "apuestas");
const aniRef       = () => collection(db, "usuarios", currentUid, "animalitos_apuestas");
const resultsRef   = () => collection(db, "resultados_sorteos");

// ════════════════════════════════════════════════════════════
// INIT – llamada al autenticarse
// ════════════════════════════════════════════════════════════
export async function initFirestore(uid) {
  currentUid = uid;

  // 1. Cargar clientes desde Firestore
  await cargarClientesDesdeFirestore();

  // 2. Cargar historial de apuestas y suscribir en tiempo real
  suscribirApuestas();
  suscribirAniApuestas();

  // 3. Suscribir resultados en tiempo real
  suscribirResultados();
}

// ════════════════════════════════════════════════════════════
// CLIENTES
// ════════════════════════════════════════════════════════════
async function cargarClientesDesideFirestore() {
  // alias por compatibilidad
  return cargarClientesDesdeFirestore();
}

async function cargarClientesDesdeFirestore() {
  try {
    const snap = await getDocs(clientesRef());
    window.clientes = snap.docs.map(d => ({ _fsId: d.id, ...d.data() }));
    if (typeof renderClientes === "function") renderClientes();
    if (typeof populateClienteSelect === "function") populateClienteSelect("apuesta-cliente");
  } catch (e) {
    console.error("Error cargando clientes:", e);
  }
}

// Guardar clientes batch (carga CSV)
window.saveClientesFirestore = async function(lista) {
  if (!currentUid) return;
  const batch = writeBatch(db);
  lista.forEach(c => {
    const ref = doc(clientesRef());
    batch.set(ref, { ...c, creado_el: serverTimestamp() });
  });
  await batch.commit();
  await cargarClientesDesdeFirestore();
};

// Crear cliente individual
window.saveClienteNuevo = async function(cliente) {
  if (!currentUid) return;
  const docRef = await addDoc(clientesRef(), { ...cliente, creado_el: serverTimestamp() });
  cliente._fsId = docRef.id;
  window.clientes.unshift(cliente);
  if (typeof renderClientes === "function") renderClientes();
  if (typeof populateClienteSelect === "function") populateClienteSelect("apuesta-cliente");
};

// Actualizar cliente
window.updateClienteFirestore = async function(fsId, datos) {
  if (!currentUid || !fsId) return;
  await updateDoc(doc(db, "usuarios", currentUid, "clientes", fsId), datos);
};

// Eliminar un cliente
window.deleteClienteFirestore = async function(fsId) {
  if (!currentUid || !fsId) return;
  await deleteDoc(doc(db, "usuarios", currentUid, "clientes", fsId));
};

// Limpiar todos los clientes
window.limpiarClientesFirestore = async function() {
  if (!currentUid) return;
  const snap = await getDocs(clientesRef());
  const batch = writeBatch(db);
  snap.docs.forEach(d => batch.delete(d.ref));
  await batch.commit();
  window.clientes = [];
  if (typeof renderClientes === "function") renderClientes();
  if (typeof populateClienteSelect === "function") populateClienteSelect("apuesta-cliente");
};

// Actualizar saldo de un cliente
window.actualizarSaldoFirestore = async function(fsId, nuevoSaldo) {
  if (!currentUid || !fsId) return;
  await updateDoc(doc(db, "usuarios", currentUid, "clientes", fsId), {
    credito_disponible: nuevoSaldo
  });
};

// ════════════════════════════════════════════════════════════
// APUESTAS (Triples / Pegadito) – tiempo real
// ════════════════════════════════════════════════════════════
function suscribirApuestas() {
  if (_unsubApuestas) _unsubApuestas();
  const q = query(apuestasRef(), orderBy("fecha", "desc"));
  _unsubApuestas = onSnapshot(q, snap => {
    window.apuestas = snap.docs.map(d => ({ _fsId: d.id, ...d.data(),
      fecha: d.data().fecha?.toDate?.()?.toLocaleString("es-VE") || d.data().fecha }));
    if (typeof renderHistorial === "function") renderHistorial();
  }, e => console.error("Error apuestas:", e));
}

window.saveApuestaFirestore = async function(apuesta) {
  if (!currentUid) return;
  await addDoc(apuestasRef(), { ...apuesta, fecha: serverTimestamp() });
};

window.limpiarApuestasFirestore = async function() {
  if (!currentUid) return;
  const snap = await getDocs(apuestasRef());
  const batch = writeBatch(db);
  snap.docs.forEach(d => batch.delete(d.ref));
  await batch.commit();
};

// ════════════════════════════════════════════════════════════
// ANIMALITOS APUESTAS – tiempo real
// ════════════════════════════════════════════════════════════
function suscribirAniApuestas() {
  if (_unsubAniApuestas) _unsubAniApuestas();
  const q = query(aniRef(), orderBy("fecha", "desc"));
  _unsubAniApuestas = onSnapshot(q, snap => {
    window.aniApuestas = snap.docs.map(d => ({ _fsId: d.id, ...d.data(),
      fecha: d.data().fecha?.toDate?.()?.toLocaleString("es-VE") || d.data().fecha }));
    if (typeof renderAniHistorial === "function") renderAniHistorial();
  }, e => console.error("Error animalitos:", e));
}

window.saveAniApuestaFirestore = async function(apuesta) {
  if (!currentUid) return;
  await addDoc(aniRef(), { ...apuesta, fecha: serverTimestamp() });
};

window.limpiarAniApuestasFirestore = async function() {
  if (!currentUid) return;
  const snap = await getDocs(aniRef());
  const batch = writeBatch(db);
  snap.docs.forEach(d => batch.delete(d.ref));
  await batch.commit();
};

// ════════════════════════════════════════════════════════════
// RESULTADOS – tiempo real (colección global)
// ════════════════════════════════════════════════════════════
function suscribirResultados() {
  if (_unsubResultados) _unsubResultados();
  _unsubResultados = onSnapshot(query(resultsRef()), snap => {
    snap.docs.forEach(d => {
      const data = d.data();
      // Actualizar UI según tipo de resultado
      if (data.tipo === "arrimao" && data.numero) {
        const n = data.numero;
        const ids = ["arrimao-r1","arrimao-r2","arrimao-r3"];
        ids.forEach((id, i) => {
          const el = document.getElementById(id);
          if (el) el.textContent = n[i] || "-";
        });
        const disp = document.getElementById("arrimao-display");
        if (disp) disp.classList.remove("hidden");
      }
      if (data.tipo === "pegadito" && data.numero) {
        const n = data.numero;
        const ids = ["peg-r1","peg-r2","peg-r3","peg-r4"];
        ids.forEach((id, i) => {
          const el = document.getElementById(id);
          if (el) el.textContent = n[i] || "-";
        });
        const disp = document.getElementById("pegadito-display");
        if (disp) disp.classList.remove("hidden");
      }
      if (data.tipo === "animalito" && data.animalito) {
        const badge = document.getElementById("animalito-badge");
        if (badge) badge.textContent = `${data.animalito.icono} ${data.animalito.nombre} #${data.animalito.numero}`;
        const disp = document.getElementById("animalito-display");
        if (disp) {
          const ic = document.getElementById("ani-icon");
          const nm = document.getElementById("ani-nombre");
          const nu = document.getElementById("ani-num");
          if (ic) ic.textContent = data.animalito.icono;
          if (nm) nm.textContent = data.animalito.nombre;
          if (nu) nu.textContent = "Número: " + data.animalito.numero;
          disp.classList.remove("hidden");
        }
      }
    });
  }, e => console.error("Error resultados:", e));
}

// Publicar resultado (Triples / Pegadito / Animalito)
window.saveResultadoFirestore = async function(tipo, datos) {
  if (!currentUid) return;
  const fechaHoy = new Date().toISOString().split("T")[0];
  const horario  = datos.horario?.replace(/[: ]/g, "") || "general";
  const docId    = `${fechaHoy}_${tipo}_${horario}`;
  await setDoc(doc(db, "resultados_sorteos", docId), {
    tipo,
    ...datos,
    fecha: serverTimestamp()
  });
};

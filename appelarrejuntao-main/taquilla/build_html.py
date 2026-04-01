#!/usr/bin/env python3
# Script para crear taquilla/index.html

import os

OUTFILE = r'c:\Users\villa\OneDrive\Documentos\appelarrejuntao\taquilla\index.html'

HTML = r'''<!DOCTYPE html>
<html lang="es" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Taquilla Asterisco Siete (*7)</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
<script>
if(localStorage.theme==="dark"||(!("theme"in localStorage)&&window.matchMedia("(prefers-color-scheme: dark)").matches)){document.documentElement.classList.add("dark")}else{document.documentElement.classList.remove("dark")}
tailwind.config={darkMode:"class",theme:{extend:{fontFamily:{sans:["Inter","sans-serif"],mono:["Roboto Mono","monospace"]}}}}
</script>
<style>
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-thumb{background:#475569;border-radius:3px}
.thermal-receipt{background:#fff;color:#000;font-family:"Courier New",monospace;font-size:11px;line-height:1.3;padding:12px;width:280px;margin:0 auto;border-bottom:2px dashed #ccc}
.receipt-divider{border-bottom:1px dashed #000;margin:6px 0}
.receipt-row{display:flex;justify-content:space-between;margin-bottom:3px;font-size:10px}
.receipt-total{font-size:13px;font-weight:bold;border-top:1px solid #000;padding-top:4px;display:flex;justify-content:space-between;margin-top:6px}
.receipt-footer{margin-top:8px;text-align:center;font-size:9px}
.time-btn.sel-m{background:#facc15;color:#422006;border-color:#eab308;font-weight:800}
.time-btn.sel-t{background:#3b82f6;color:#fff;border-color:#2563eb;font-weight:800}
.time-btn.sel-n{background:#ef4444;color:#fff;border-color:#dc2626;font-weight:800}
.animal-btn{display:flex;flex-direction:column;align-items:center;justify-content:center;height:56px;border-radius:8px;border:1px solid #334155;background:#1e293b;color:#cbd5e1;transition:all .1s;cursor:pointer}
.animal-btn:hover{background:#334155}.animal-btn.sel{background:#059669;border-color:#10b981;color:#fff}
.animal-num{font-weight:bold;font-size:1rem}
.animal-name{font-size:0.52rem;text-transform:uppercase;margin-top:2px;text-align:center;line-height:1.1}
.lot-card{border:2px solid transparent;border-radius:10px;padding:10px;cursor:pointer;transition:all .15s;background:#1e293b}
.lot-card.sel{border-color:#6366f1;background:#1e1b4b}
.lot-time-btn{font-size:10px;padding:2px 6px;border-radius:4px;border:1px solid #475569;color:#94a3b8;cursor:pointer;transition:all .1s}
.lot-time-btn:hover{background:#334155;color:#fff}
.lot-time-btn.sel-m{background:#facc15;color:#422006;border-color:#eab308}
.lot-time-btn.sel-t{background:#3b82f6;color:#fff;border-color:#2563eb}
.lot-time-btn.sel-n{background:#ef4444;color:#fff;border-color:#dc2626}
@keyframes fadeIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
.fade-in{animation:fadeIn .2s ease-out}
@media print{body *{visibility:hidden}#printable-area,#printable-area *{visibility:visible}#printable-area{position:absolute;left:0;top:0;background:#fff;color:#000;width:300px}}
</style>
</head>
<body class="bg-slate-900 text-slate-200 font-sans antialiased h-screen flex overflow-hidden">

<!-- SIDEBAR -->
<nav class="w-16 md:w-20 h-full flex-shrink-0 bg-slate-950 border-r border-slate-800 flex flex-col justify-between items-center py-4">
  <div class="flex flex-col items-center gap-1">
    <div class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center font-black text-white text-lg mb-3 shadow-lg cursor-pointer" title="Asterisco Siete (*7)">*7</div>
    <button onclick="changeView('pos')" id="nav-pos" class="nav-btn w-12 h-12 rounded-xl flex flex-col items-center justify-center text-indigo-400 bg-slate-800 border-l-2 border-indigo-500 transition-colors" title="Taquilla">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
      <span class="text-[8px] mt-0.5 font-bold">POS</span>
    </button>
    <button onclick="changeView('management')" id="nav-management" class="nav-btn w-12 h-12 rounded-xl flex flex-col items-center justify-center text-slate-400 hover:bg-slate-800 hover:text-blue-400 transition-colors" title="Tickets">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
      <span class="text-[8px] mt-0.5 font-bold">Tickets</span>
    </button>
    <button onclick="changeView('reports')" id="nav-reports" class="nav-btn w-12 h-12 rounded-xl flex flex-col items-center justify-center text-slate-400 hover:bg-slate-800 hover:text-purple-400 transition-colors" title="Reportes">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
      <span class="text-[8px] mt-0.5 font-bold">Reportes</span>
    </button>
    <button onclick="changeView('animals')" id="nav-animals" class="nav-btn w-12 h-12 rounded-xl flex flex-col items-center justify-center text-slate-400 hover:bg-slate-800 hover:text-emerald-400 transition-colors" title="Animalitos">
      <span class="text-xl">🐾</span>
      <span class="text-[8px] mt-0.5 font-bold">Animal</span>
    </button>
  </div>
  <div class="flex flex-col items-center gap-2">
    <button onclick="toggleTheme()" class="w-10 h-10 rounded-xl text-slate-500 hover:bg-slate-800 hover:text-yellow-400 transition-colors flex items-center justify-center">
      <svg class="w-5 h-5 dark:block hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
      <svg class="w-5 h-5 dark:hidden block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
    </button>
  </div>
</nav>

<!-- MAIN -->
<main class="flex-1 flex overflow-hidden bg-slate-50 dark:bg-slate-900 transition-colors">

  <!-- POS VIEW -->
  <div id="view-pos" class="w-full h-full flex overflow-hidden">
    <!-- LEFT PANEL -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <div class="h-12 px-4 flex items-center justify-between bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 flex-shrink-0">
        <div>
          <span class="font-bold text-slate-800 dark:text-white text-sm">⭐ Asterisco Siete (*7)</span>
          <span class="text-slate-400 text-xs ml-3" id="clock">--:--:--</span>
        </div>
        <div class="text-xs text-emerald-500 font-bold" id="today-sales">Ventas: Bs 0,00</div>
      </div>
      <!-- Input bar -->
      <div class="p-3 bg-white dark:bg-slate-850 border-b border-slate-200 dark:border-slate-800 flex-shrink-0">
        <div class="flex flex-wrap gap-2 items-end max-w-4xl mx-auto">
          <div>
            <label class="block text-[9px] font-bold text-slate-500 uppercase mb-1">Número</label>
            <input id="betNum" type="text" maxlength="4" placeholder="---" autocomplete="off"
              class="w-28 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-600 text-slate-900 dark:text-white text-xl font-mono font-bold text-center h-10 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none">
          </div>
          <div>
            <div class="flex justify-between mb-1"><label class="text-[9px] font-bold text-slate-500 uppercase">Monto Bs</label><span class="text-[8px] text-emerald-500 font-bold">mín 50</span></div>
            <input id="betAmt" type="number" placeholder="50"
              class="w-28 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-600 text-emerald-600 dark:text-emerald-400 text-xl font-mono font-bold text-right h-10 px-2 rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none">
          </div>
          <div class="flex gap-2">
            <button onclick="setMode('normal')" id="modeNormal" class="h-10 px-3 rounded-lg text-xs font-bold bg-indigo-600 text-white">3D</button>
            <button onclick="setMode('terminal')" id="modeTerminal" class="h-10 px-3 rounded-lg text-xs font-bold bg-slate-700 text-slate-300 hover:bg-slate-600">Term</button>
            <button onclick="setMode('serie')" id="modeSerie" class="h-10 px-3 rounded-lg text-xs font-bold bg-slate-700 text-slate-300 hover:bg-slate-600">Serie</button>
            <button onclick="setMode('cuatro')" id="modeCuatro" class="h-10 px-3 rounded-lg text-xs font-bold bg-slate-700 text-slate-300 hover:bg-slate-600">4C</button>
          </div>
          <button onclick="addBet()" class="h-10 px-6 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg shadow-lg transition-all flex items-center gap-2">
            Agregar <span class="text-xl">+</span>
          </button>
        </div>
      </div>
      <!-- Lottery grid -->
      <div class="flex-1 overflow-y-auto p-4">
        <p class="text-[10px] text-slate-500 uppercase font-bold mb-3">Seleccione Loterías y Horarios</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 max-w-4xl mx-auto" id="lottery-grid"></div>
      </div>
    </div>
    <!-- RIGHT TICKET PANEL -->
    <div class="w-[280px] flex-shrink-0 bg-white dark:bg-slate-950 border-l border-slate-200 dark:border-slate-800 flex flex-col">
      <div class="p-3 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 text-center">
        <span class="text-xs font-bold text-slate-600 dark:text-slate-300 uppercase tracking-widest">Ticket en Curso</span>
      </div>
      <div class="flex-1 overflow-y-auto p-3 bg-slate-100 dark:bg-slate-900" id="ticket-preview">
        <p class="text-center text-slate-500 text-xs italic mt-8">...esperando apuestas...</p>
      </div>
      <div class="p-3 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900">
        <div class="flex justify-between mb-2">
          <span class="text-xs font-bold text-slate-500">TOTAL:</span>
          <span class="text-xl font-bold text-slate-800 dark:text-white" id="grand-total">Bs 0,00</span>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <button onclick="clearTicket()" class="py-2 rounded bg-red-100 dark:bg-red-900/30 text-red-600 font-bold text-xs border border-red-200 dark:border-red-800">Cancelar</button>
          <button onclick="openPreview()" id="btn-verify" disabled class="py-2 rounded bg-emerald-600 text-white font-bold text-xs opacity-50 cursor-not-allowed">Verificar</button>
        </div>
      </div>
    </div>
  </div>

  <!-- MANAGEMENT VIEW -->
  <div id="view-management" class="hidden w-full h-full flex flex-col p-5 overflow-hidden">
    <div class="flex justify-between items-center mb-5">
      <h1 class="text-2xl font-bold text-slate-800 dark:text-white">Gestión de Tickets</h1>
      <div class="flex gap-2">
        <button onclick="filterStatus('all')" class="px-3 py-1.5 rounded-full text-xs bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-white font-bold">Todos</button>
        <button onclick="filterStatus('Pendiente')" class="px-3 py-1.5 rounded-full text-xs border border-yellow-400 text-yellow-600 dark:text-yellow-400 font-bold">Pendientes</button>
        <button onclick="filterStatus('Ganador')" class="px-3 py-1.5 rounded-full text-xs border border-emerald-400 text-emerald-600 dark:text-emerald-400 font-bold">Ganadores</button>
        <button onclick="simulateWinner()" class="px-3 py-1.5 rounded text-xs bg-purple-600 text-white font-bold">Simular Sorteo</button>
      </div>
    </div>
    <div class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 flex-1 overflow-auto">
      <table class="w-full text-sm min-w-[500px]">
        <thead class="bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-300 text-xs uppercase font-bold sticky top-0">
          <tr>
            <th class="p-4 text-left">Ticket</th>
            <th class="p-4 text-left">Fecha/Hora</th>
            <th class="p-4 text-right">Monto</th>
            <th class="p-4 text-center">Estado</th>
            <th class="p-4 text-center">Acción</th>
          </tr>
        </thead>
        <tbody id="mgmt-body"></tbody>
      </table>
    </div>
  </div>

  <!-- REPORTS VIEW -->
  <div id="view-reports" class="hidden w-full h-full flex flex-col p-5 overflow-y-auto">
    <h1 class="text-2xl font-bold text-slate-800 dark:text-white mb-6">Reportes y Cierre de Caja</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-6">
      <div class="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700">
        <p class="text-xs font-bold text-blue-500 uppercase mb-1">Entradas (Ventas)</p>
        <p class="text-3xl font-bold text-slate-900 dark:text-white" id="rep-sales">Bs 0,00</p>
        <p class="text-xs text-slate-400 mt-1" id="rep-sales-count">0 tickets</p>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700">
        <p class="text-xs font-bold text-red-500 uppercase mb-1">Salidas (Premios)</p>
        <p class="text-3xl font-bold text-slate-900 dark:text-white" id="rep-payouts">Bs 0,00</p>
        <p class="text-xs text-slate-400 mt-1" id="rep-payouts-count">0 pagados</p>
      </div>
      <div class="bg-gradient-to-br from-emerald-50 to-emerald-100 dark:from-slate-800 dark:to-emerald-900/30 rounded-xl p-5 border border-emerald-200 dark:border-emerald-700/30">
        <p class="text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase mb-1">Balance en Caja</p>
        <p class="text-3xl font-bold text-emerald-800 dark:text-white" id="rep-balance">Bs 0,00</p>
      </div>
    </div>
    <div class="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-auto flex-1">
      <table class="w-full text-sm min-w-[400px]">
        <thead class="bg-slate-100 dark:bg-slate-900 text-xs uppercase font-bold text-slate-600 dark:text-slate-300 sticky top-0">
          <tr>
            <th class="p-4 text-left">Ticket</th>
            <th class="p-4 text-left">Fecha/Hora</th>
            <th class="p-4 text-right">Monto</th>
            <th class="p-4 text-center">Estado</th>
          </tr>
        </thead>
        <tbody id="reports-body"></tbody>
      </table>
    </div>
  </div>

  <!-- ANIMALITOS VIEW -->
  <div id="view-animals" class="hidden w-full h-full flex overflow-hidden">
    <div class="flex-1 flex flex-col overflow-hidden">
      <div class="h-12 px-4 flex items-center bg-white dark:bg-slate-900 border-b border-slate-800 flex-shrink-0">
        <span class="font-bold text-slate-800 dark:text-white text-sm">🐾 Animalitos</span>
      </div>
      <!-- Controls -->
      <div class="p-3 border-b border-slate-800 bg-slate-900 flex-shrink-0">
        <div class="flex flex-wrap gap-2 items-end mb-2">
          <div>
            <label class="block text-[9px] font-bold text-slate-500 uppercase mb-1">Monto Bs</label>
            <input id="animalAmt" type="number" placeholder="50"
              class="w-24 bg-slate-800 border border-slate-600 text-emerald-400 text-lg font-bold text-right h-9 px-2 rounded-lg outline-none focus:ring-2 focus:ring-emerald-500">
          </div>
          <button onclick="addAnimalBets()" class="h-9 px-5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg text-sm">Agregar</button>
          <button onclick="toggleAllAnimals()" class="h-9 px-4 bg-slate-700 hover:bg-slate-600 text-slate-300 font-bold rounded-lg text-xs">Todos/Ninguno</button>
        </div>
        <div class="flex flex-wrap gap-1.5" id="animal-lottery-btns"></div>
        <div class="flex flex-wrap gap-1.5 mt-2" id="animal-time-btns"></div>
      </div>
      <!-- Grid -->
      <div class="flex-1 overflow-y-auto p-3">
        <div class="grid grid-cols-5 sm:grid-cols-7 md:grid-cols-9 gap-1.5" id="animal-grid"></div>
      </div>
    </div>
    <!-- Ticket panel reuse -->
    <div class="w-[280px] flex-shrink-0 bg-white dark:bg-slate-950 border-l border-slate-800 flex flex-col">
      <div class="p-3 border-b border-slate-800 bg-slate-900 text-center">
        <span class="text-xs font-bold text-slate-300 uppercase tracking-widest">Ticket en Curso</span>
      </div>
      <div class="flex-1 overflow-y-auto p-3 bg-slate-900" id="animal-ticket-preview">
        <p class="text-center text-slate-500 text-xs italic mt-8">...esperando apuestas...</p>
      </div>
      <div class="p-3 border-t border-slate-800 bg-slate-900">
        <div class="flex justify-between mb-2">
          <span class="text-xs font-bold text-slate-500">TOTAL:</span>
          <span class="text-xl font-bold text-white" id="animal-grand-total">Bs 0,00</span>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <button onclick="clearTicket()" class="py-2 rounded bg-red-900/30 text-red-400 font-bold text-xs border border-red-800">Cancelar</button>
          <button onclick="openPreview()" id="btn-verify-animal" disabled class="py-2 rounded bg-emerald-600 text-white font-bold text-xs opacity-50 cursor-not-allowed">Verificar</button>
        </div>
      </div>
    </div>
  </div>

</main>

<!-- MODALS -->
<!-- Preview/Confirm Modal -->
<div id="preview-modal" class="fixed inset-0 z-50 bg-black/80 flex items-center justify-center hidden p-4">
  <div class="bg-white rounded-xl w-full max-w-[300px] overflow-hidden shadow-2xl">
    <div class="bg-slate-800 text-white p-3 flex justify-between items-center">
      <h3 class="font-bold text-sm uppercase">Confirmar Ticket</h3>
      <button onclick="closePreview()" class="text-slate-400 hover:text-white">✕</button>
    </div>
    <div class="p-4 bg-slate-100 flex justify-center" id="final-preview"></div>
    <div class="p-3 bg-white border-t flex gap-2">
      <button onclick="closePreview()" class="flex-1 py-2 border border-slate-300 rounded font-bold text-xs">Cancelar</button>
      <button onclick="confirmPDF()" class="flex-1 py-2 bg-orange-600 text-white rounded font-bold text-xs">PDF</button>
      <button onclick="confirmPrint()" class="flex-1 py-2 bg-indigo-600 text-white rounded font-bold text-xs">Imprimir</button>
    </div>
  </div>
</div>

<!-- Action Modal (view/void/pay) -->
<div id="action-modal" class="fixed inset-0 z-50 bg-black/80 flex items-center justify-center hidden p-4">
  <div class="bg-white dark:bg-slate-800 rounded-xl w-full max-w-[340px] overflow-hidden shadow-2xl">
    <div class="p-4 border-b border-slate-200 dark:border-slate-700 flex justify-between items-center">
      <h3 class="font-bold text-slate-800 dark:text-white">Detalle de Ticket</h3>
      <button onclick="closeActionModal()" class="text-slate-400 hover:text-slate-700 dark:hover:text-white">✕</button>
    </div>
    <div class="p-4 bg-slate-100 dark:bg-slate-900 flex justify-center" id="action-preview"></div>
    <div class="p-4 flex flex-wrap gap-2 justify-end border-t border-slate-200 dark:border-slate-700" id="action-btns"></div>
  </div>
</div>

<!-- Toast -->
<div id="toast-container" class="fixed top-4 left-1/2 -translate-x-1/2 z-[200] flex flex-col gap-2 pointer-events-none"></div>

<!-- Hidden print area -->
<div id="printable-area" class="hidden"></div>

<script>
// ─── CONFIG ──────────────────────────────────────────────────────────
const AGENCY = {name:'ASTERISCO SIETE (*7)', rif:'Licencia: *7-0001', addr:'Sistema de Apuestas'};
const LOTTERIES = [
  {name:'Táchira'},{name:'Zulia'},{name:'Chance'},{name:'Caracas'},
  {name:'Caliente'},{name:'Zamorano'},{name:'SUPERGANA'},{name:'TRIPLE GANA'},{name:'NAPA GANA'}
];
const TIMES = [{label:'9AM',type:'morning'},{label:'12PM',type:'afternoon'},{label:'3PM',type:'afternoon'},{label:'7PM',type:'night'}];
const ANIMAL_LOTS = ['Lotto Activo','La Granjita','Animalitos Arrejuntao','Selva Plus','Guacharo Activo'];
const ANIMALS = [
  {n:'1',name:'Carnero'},{n:'2',name:'Toro'},{n:'3',name:'Ciempiés'},{n:'4',name:'Alacrán'},
  {n:'5',name:'León'},{n:'6',name:'Rana'},{n:'7',name:'Perico'},{n:'8',name:'Ratón'},
  {n:'9',name:'Águila'},{n:'10',name:'Tigre'},{n:'11',name:'Gato'},{n:'12',name:'Caballo'},
  {n:'13',name:'Mono'},{n:'14',name:'Paloma'},{n:'15',name:'Zorro'},{n:'16',name:'Oso'},
  {n:'17',name:'Pavo'},{n:'18',name:'Burro'},{n:'19',name:'Chivo'},{n:'20',name:'Cochino'},
  {n:'21',name:'Gallo'},{n:'22',name:'Camello'},{n:'23',name:'Cebra'},{n:'24',name:'Iguana'},
  {n:'25',name:'Gallina'},{n:'26',name:'Vaca'},{n:'27',name:'Perro'},{n:'28',name:'Zamuro'},
  {n:'29',name:'Elefante'},{n:'30',name:'Caimán'},{n:'31',name:'Lapa'},{n:'32',name:'Ardilla'},
  {n:'33',name:'Pez'},{n:'34',name:'Venado'},{n:'35',name:'Jirafa'},{n:'36',name:'Culebra'}
];

// ─── STATE ────────────────────────────────────────────────────────────
let currentTicket = [];
let selectedLots = {}; // {lotName: timeType}
let selAnimals = [];
let selAnimalLots = ['Lotto Activo'];
let selAnimalTime = 'morning';
let betMode = 'normal';
let nextId = parseInt(localStorage.getItem('ast7_nextid')||'1001');
let transactions = JSON.parse(localStorage.getItem('ast7_tx')||'[]');
let selectedTxId = null;

function save(){
  localStorage.setItem('ast7_tx', JSON.stringify(transactions));
  localStorage.setItem('ast7_nextid', String(nextId));
}

// ─── CLOCK ────────────────────────────────────────────────────────────
function updateClock(){
  const now = new Date();
  const t = document.getElementById('clock');
  if(t) t.textContent = now.toLocaleTimeString('es-VE',{hour12:true});
}
setInterval(updateClock, 1000);
updateClock();

// ─── THEME ────────────────────────────────────────────────────────────
function toggleTheme(){
  const d = document.documentElement;
  if(d.classList.contains('dark')){d.classList.remove('dark');localStorage.theme='light';}
  else{d.classList.add('dark');localStorage.theme='dark';}
}

// ─── VIEWS ────────────────────────────────────────────────────────────
function changeView(v){
  ['pos','management','reports','animals'].forEach(name=>{
    document.getElementById('view-'+name).classList.add('hidden');
    const n = document.getElementById('nav-'+name);
    if(n){ n.classList.remove('text-indigo-400','bg-slate-800','border-l-2','border-indigo-500','text-blue-400','text-purple-400','text-emerald-400');
      n.classList.add('text-slate-400'); }
  });
  document.getElementById('view-'+v).classList.remove('hidden');
  const btn = document.getElementById('nav-'+v);
  if(btn){
    btn.classList.remove('text-slate-400');
    const colors = {pos:'text-indigo-400',management:'text-blue-400',reports:'text-purple-400',animals:'text-emerald-400'};
    btn.classList.add(colors[v],'bg-slate-800');
  }
  if(v==='management') renderMgmt();
  if(v==='reports') renderReports();
  if(v==='animals') renderAnimalGrid();
}

// ─── LOTTERY GRID ─────────────────────────────────────────────────────
function renderLotteryGrid(){
  const grid = document.getElementById('lottery-grid');
  grid.innerHTML = '';
  LOTTERIES.forEach(lot=>{
    const hasSel = Object.keys(selectedLots).some(k=>k.startsWith(lot.name+' '));
    const card = document.createElement('div');
    card.className = 'lot-card'+(hasSel?' sel':'');
    card.innerHTML = `<div class="flex items-center justify-between mb-2">
      <span class="font-bold text-sm text-slate-800 dark:text-white">${lot.name}</span>
      ${hasSel?'<span class="text-[10px] text-indigo-400 font-bold">✓ SEL</span>':''}
    </div>
    <div class="flex flex-wrap gap-1">
      ${TIMES.map(t=>{
        const key=lot.name+' '+t.label;
        const isSel=key in selectedLots;
        const cls = isSel?(t.type==='morning'?'sel-m':t.type==='afternoon'?'sel-t':'sel-n'):'';
        return `<button class="lot-time-btn ${cls}" onclick="toggleLotTime('${lot.name}','${t.label}','${t.type}')" >${t.label}</button>`;
      }).join('')}
    </div>`;
    grid.appendChild(card);
  });
}

function toggleLotTime(name, label, type){
  const key = name+' '+label;
  if(key in selectedLots){ delete selectedLots[key]; }
  else { selectedLots[key] = {type, label, name}; }
  renderLotteryGrid();
}

// ─── BET MODE ─────────────────────────────────────────────────────────
function setMode(m){
  betMode = m;
  ['Normal','Terminal','Serie','Cuatro'].forEach(x=>{
    const b = document.getElementById('mode'+x);
    if(b){ b.className = b.className.replace('bg-indigo-600 text-white','bg-slate-700 text-slate-300 hover:bg-slate-600'); }
  });
  const active = document.getElementById('mode'+m.charAt(0).toUpperCase()+m.slice(1));
  if(active){ active.className = active.className.replace('bg-slate-700 text-slate-300 hover:bg-slate-600','bg-indigo-600 text-white'); }
  const input = document.getElementById('betNum');
  if(m==='normal'){input.maxLength=3;input.placeholder='---';}
  else if(m==='terminal'){input.maxLength=2;input.placeholder='--';}
  else if(m==='serie'){input.maxLength=2;input.placeholder='--';}
  else if(m==='cuatro'){input.maxLength=4;input.placeholder='----';}
}

// ─── ADD BET ──────────────────────────────────────────────────────────
function addBet(){
  const num = document.getElementById('betNum').value.trim();
  const amt = parseFloat(document.getElementById('betAmt').value);
  if(!num || isNaN(amt) || amt < 50){ showToast('Monto mínimo 50 Bs y número requerido','error'); return; }
  const keys = Object.keys(selectedLots);
  if(!keys.length){ showToast('Seleccione al menos una lotería y horario','error'); return; }
  
  let numbers = [];
  if(betMode==='serie'){
    for(let i=0;i<=9;i++) numbers.push({val:`${i}${num}`,label:`${i}${num} (S)`});
  } else {
    const label = betMode==='terminal'?`${num} (T)`:betMode==='cuatro'?`${num} (4C)`:num;
    numbers.push({val:num,label});
  }

  keys.forEach(k=>{
    numbers.forEach(n=>{
      currentTicket.push({type:'lottery',lottery:k,number:n.label,amount:amt});
    });
  });

  renderTicket();
  document.getElementById('betNum').value='';
  document.getElementById('betNum').focus();
  showToast('Apuesta agregada ✓','success');
}

// ─── TICKET RENDER ────────────────────────────────────────────────────
function renderReceiptHTML(items, total, ticketId, validCode, dateStr, timeStr, editable){
  if(!items.length) return '<p class="text-center text-slate-500 text-xs italic mt-8">...esperando apuestas...</p>';
  
  let rows = items.map((item,i)=>`
    <div style="display:flex;justify-content:space-between;margin-bottom:2px;font-size:10px;align-items:center">
      <div style="flex:1;overflow:hidden">
        <div style="font-weight:bold;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${item.lottery||item.type}</div>
        <div style="font-size:9px">${item.number||item.animal||''}</div>
      </div>
      <div style="text-align:right;min-width:50px;font-weight:bold">${item.amount.toFixed(2)}</div>
      ${editable?`<div onclick="removeBet(${i})" style="cursor:pointer;color:#dc2626;padding-left:4px;font-size:12px">×</div>`:''}
    </div>`).join('');

  return `<div class="thermal-receipt">
    <div style="text-align:center;margin-bottom:8px">
      <div style="font-size:16px;font-weight:900">${AGENCY.name}</div>
      <div style="font-size:9px">${AGENCY.rif} | ${AGENCY.addr}</div>
    </div>
    <div class="receipt-divider"></div>
    <div class="receipt-row"><span>Ticket: ${ticketId||'######'}</span><span>${dateStr||new Date().toLocaleDateString('es-VE')}</span></div>
    <div class="receipt-row"><span>Código: ${validCode||'----------'}</span><span>${timeStr||new Date().toLocaleTimeString('es-VE',{hour12:true})}</span></div>
    <div class="receipt-divider"></div>
    <div style="margin-bottom:4px;font-size:10px;font-weight:bold;display:flex;justify-content:space-between"><span>APUESTA</span><span>MONTO${editable?'  ':'  '}</span></div>
    ${rows}
    <div class="receipt-total"><span>TOTAL:</span><span>Bs ${total.toFixed(2)}</span></div>
    <div class="receipt-footer"><p>*** GRACIAS POR SU PREFERENCIA ***</p><p>Revise su ticket antes de retirarse</p><p>Caduca a los 3 días</p></div>
  </div>`;
}

function renderTicket(){
  const total = currentTicket.reduce((s,i)=>s+i.amount,0);
  const now = new Date();
  document.getElementById('ticket-preview').innerHTML = renderReceiptHTML(currentTicket,total,null,null,null,null,true);
  document.getElementById('animal-ticket-preview').innerHTML = document.getElementById('ticket-preview').innerHTML;
  document.getElementById('grand-total').textContent = 'Bs '+total.toFixed(2);
  document.getElementById('animal-grand-total').textContent = 'Bs '+total.toFixed(2);
  const hasItems = currentTicket.length>0;
  ['btn-verify','btn-verify-animal'].forEach(id=>{
    const b = document.getElementById(id);
    if(b){b.disabled=!hasItems; b.classList.toggle('opacity-50',!hasItems); b.classList.toggle('cursor-not-allowed',!hasItems);}
  });
}

function removeBet(i){
  currentTicket.splice(i,1);
  renderTicket();
}

function clearTicket(){
  if(currentTicket.length && !confirm('¿Cancelar todas las apuestas?')) return;
  currentTicket=[];
  renderTicket();
}

function genCode(){
  return Array.from({length:10},()=>'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'[Math.floor(Math.random()*32)]).join('');
}

// ─── PREVIEW / CONFIRM ────────────────────────────────────────────────
function openPreview(){
  if(!currentTicket.length) return;
  const total = currentTicket.reduce((s,i)=>s+i.amount,0);
  const now = new Date();
  document.getElementById('final-preview').innerHTML = renderReceiptHTML(currentTicket,total,'#'+nextId,genCode(),now.toLocaleDateString('es-VE'),now.toLocaleTimeString('es-VE',{hour12:true}),false);
  document.getElementById('preview-modal').classList.remove('hidden');
}
function closePreview(){ document.getElementById('preview-modal').classList.add('hidden'); }

function confirmAndSave(){
  const total = currentTicket.reduce((s,i)=>s+i.amount,0);
  const now = new Date();
  const tx = {
    id:nextId++, status:'Pendiente', total,
    items:[...currentTicket],
    validCode:genCode(),
    dateOnly:now.toLocaleDateString('es-VE'),
    timeOnly:now.toLocaleTimeString('es-VE',{hour12:true}),
    timestamp:now.toISOString()
  };
  transactions.unshift(tx);
  save();
  updateTodaySales();
  currentTicket=[];
  renderTicket();
  return tx;
}

function confirmPrint(){
  const tx = confirmAndSave();
  closePreview();
  document.getElementById('printable-area').innerHTML = renderReceiptHTML(tx.items,tx.total,'#'+tx.id,tx.validCode,tx.dateOnly,tx.timeOnly,false);
  window.print();
  showToast('Ticket #'+tx.id+' impreso','success');
}

function confirmPDF(){
  const tx = confirmAndSave();
  closePreview();
  const el = document.getElementById('final-preview');
  html2pdf().set({margin:0.1,filename:`Ticket_*7_${tx.id}.pdf`,image:{type:'jpeg',quality:0.98},html2canvas:{scale:2,backgroundColor:'#ffffff'},jsPDF:{unit:'in',format:[3.15,8],orientation:'portrait'}}).from(el).save();
  showToast('PDF descargado','success');
}

// ─── TODAY SALES ──────────────────────────────────────────────────────
function updateTodaySales(){
  const today = new Date().toLocaleDateString('es-VE');
  const total = transactions.filter(t=>t.dateOnly===today&&t.status!=='Anulado').reduce((s,t)=>s+t.total,0);
  const el = document.getElementById('today-sales');
  if(el) el.textContent = 'Ventas: Bs '+total.toFixed(2);
}

// ─── MANAGEMENT ───────────────────────────────────────────────────────
function renderMgmt(statusFilter='all'){
  const tbody = document.getElementById('mgmt-body');
  if(!tbody) return;
  let filtered = statusFilter==='all'?transactions:transactions.filter(t=>t.status===statusFilter);
  if(!filtered.length){ tbody.innerHTML='<tr><td colspan="5" class="p-8 text-center text-slate-400 italic text-sm">No hay tickets.</td></tr>'; return; }
  
  tbody.innerHTML = filtered.map(t=>{
    const sc = t.status==='Pendiente'?'text-yellow-400':t.status==='Ganador'?'text-emerald-400':t.status==='Pagado'?'text-blue-400':'text-red-400';
    return `<tr class="border-b border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/30">
      <td class="p-4 font-mono font-bold text-slate-900 dark:text-white">#${t.id}</td>
      <td class="p-4 text-xs text-slate-500 dark:text-slate-400">${t.dateOnly} ${t.timeOnly}</td>
      <td class="p-4 text-right font-bold text-emerald-600 dark:text-emerald-400">Bs ${t.total.toFixed(2)}</td>
      <td class="p-4 text-center"><span class="${sc} text-xs font-bold uppercase">${t.status}</span></td>
      <td class="p-4 text-center">
        <button onclick="openAction(${t.id})" class="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-500 dark:text-slate-300">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
        </button>
      </td>
    </tr>`;
  }).join('');
}

function filterStatus(s){ renderMgmt(s); }

function simulateWinner(){
  const pend = transactions.filter(t=>t.status==='Pendiente');
  if(!pend.length){ showToast('No hay tickets pendientes','error'); return; }
  const t = pend[Math.floor(Math.random()*pend.length)];
  t.status='Ganador'; t.prizeValue=t.total*30;
  save(); renderMgmt();
  showToast('Ticket #'+t.id+' GANADOR! Premio: Bs '+t.prizeValue.toFixed(2),'success');
}

function openAction(id){
  const t = transactions.find(x=>x.id===id);
  if(!t) return;
  selectedTxId=id;
  document.getElementById('action-preview').innerHTML = renderReceiptHTML(t.items,t.total,'#'+t.id,t.validCode,t.dateOnly,t.timeOnly,false);
  const btns = document.getElementById('action-btns');
  let extra='';
  if(t.status==='Pendiente') extra=`<button onclick="voidTicket()" class="px-4 py-2 rounded bg-red-600 text-white font-bold text-xs">Anular</button>`;
  else if(t.status==='Ganador') extra=`<button onclick="payTicket()" class="px-4 py-2 rounded bg-emerald-600 text-white font-bold text-xs">Pagar Bs ${(t.prizeValue||t.total*30).toFixed(2)}</button>`;
  btns.innerHTML=`<button onclick="closeActionModal()" class="px-4 py-2 rounded border border-slate-300 dark:border-slate-600 text-sm font-bold text-slate-700 dark:text-slate-300">Cerrar</button>${extra}`;
  document.getElementById('action-modal').classList.remove('hidden');
}
function closeActionModal(){ document.getElementById('action-modal').classList.add('hidden'); selectedTxId=null; }
function voidTicket(){
  const r = prompt('Motivo de anulación:'); if(!r) return;
  const t = transactions.find(x=>x.id===selectedTxId);
  if(t){t.status='Anulado';t.voidReason=r;save();renderMgmt();updateTodaySales();}
  closeActionModal(); showToast('Ticket anulado','success');
}
function payTicket(){
  const t = transactions.find(x=>x.id===selectedTxId);
  if(t){t.status='Pagado';t.prizeValue=t.prizeValue||t.total*30;save();renderMgmt();}
  closeActionModal(); showToast('Premio pagado ✓','success');
}

// ─── REPORTS ──────────────────────────────────────────────────────────
function renderReports(){
  let sales=0,payouts=0,cnt=0,pcnt=0;
  transactions.forEach(t=>{
    if(t.status!=='Anulado'){sales+=t.total;cnt++;}
    if(t.status==='Pagado'){payouts+=t.prizeValue||0;pcnt++;}
  });
  document.getElementById('rep-sales').textContent='Bs '+sales.toFixed(2);
  document.getElementById('rep-sales-count').textContent=cnt+' tickets';
  document.getElementById('rep-payouts').textContent='Bs '+payouts.toFixed(2);
  document.getElementById('rep-payouts-count').textContent=pcnt+' pagados';
  document.getElementById('rep-balance').textContent='Bs '+(sales-payouts).toFixed(2);
  const tbody=document.getElementById('reports-body');
  tbody.innerHTML=transactions.map(t=>{
    const sc=t.status==='Pendiente'?'text-yellow-500':t.status==='Ganador'?'text-emerald-500':t.status==='Pagado'?'text-blue-500':'text-red-500';
    return `<tr class="border-b border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/30">
      <td class="p-4 font-mono font-bold text-slate-900 dark:text-white">#${t.id}</td>
      <td class="p-4 text-xs text-slate-500 dark:text-slate-400">${t.dateOnly} ${t.timeOnly}</td>
      <td class="p-4 text-right font-bold text-emerald-600 dark:text-emerald-400">Bs ${t.total.toFixed(2)}</td>
      <td class="p-4 text-center"><span class="${sc} text-xs font-bold">${t.status}</span></td>
    </tr>`;
  }).join('');
}

// ─── ANIMALITOS ───────────────────────────────────────────────────────
function renderAnimalGrid(){
  // Lottery buttons
  const lotBtns = document.getElementById('animal-lottery-btns');
  lotBtns.innerHTML = ANIMAL_LOTS.map(l=>`
    <button onclick="toggleAnimalLot('${l}')" class="px-2 py-1 rounded text-xs font-bold border transition-all ${selAnimalLots.includes(l)?'bg-emerald-600 border-emerald-600 text-white':'border-slate-600 text-slate-400 hover:border-emerald-500 hover:text-emerald-400'}">${l}</button>`).join('');
  
  // Time buttons
  const timeBtns = document.getElementById('animal-time-btns');
  timeBtns.innerHTML = TIMES.map(t=>`
    <button onclick="setAnimalTime('${t.type}')" class="px-2 py-1 rounded time-btn text-xs ${selAnimalTime===t.type?(t.type==='morning'?'sel-m':t.type==='afternoon'?'sel-t':'sel-n'):'border border-slate-600 text-slate-400'}">${t.label}</button>`).join('');

  // Animal grid
  const grid = document.getElementById('animal-grid');
  grid.innerHTML = ANIMALS.map(a=>`
    <div onclick="toggleAnimal('${a.n}')" class="animal-btn ${selAnimals.includes(a.n)?'sel':''}">
      <div class="animal-num">${a.n}</div>
      <div class="animal-name">${a.name}</div>
    </div>`).join('');
}

function toggleAnimalLot(l){
  const i=selAnimalLots.indexOf(l);
  if(i>-1)selAnimalLots.splice(i,1); else selAnimalLots.push(l);
  renderAnimalGrid();
}
function setAnimalTime(t){selAnimalTime=t;renderAnimalGrid();}
function toggleAnimal(n){
  const i=selAnimals.indexOf(n);
  if(i>-1)selAnimals.splice(i,1); else selAnimals.push(n);
  renderAnimalGrid();
}
function toggleAllAnimals(){
  selAnimals = selAnimals.length===ANIMALS.length?[]:ANIMALS.map(a=>a.n);
  renderAnimalGrid();
}

function addAnimalBets(){
  const amt=parseFloat(document.getElementById('animalAmt').value);
  if(!selAnimals.length||!selAnimalLots.length||isNaN(amt)||amt<50){
    showToast('Seleccione animales, loterías y monto mínimo 50 Bs','error'); return;
  }
  selAnimals.forEach(n=>{
    const a=ANIMALS.find(x=>x.n===n);
    selAnimalLots.forEach(l=>{
      currentTicket.push({type:'animal',lottery:l+' '+selAnimalTime.substring(0,1).toUpperCase(),number:n+' '+a.name,amount:amt});
    });
  });
  selAnimals=[];
  renderAnimalGrid();
  renderTicket();
  showToast(currentTicket.length+' apuestas agregadas ✓','success');
}

// ─── TOAST ────────────────────────────────────────────────────────────
function showToast(msg,type='info'){
  const c=document.getElementById('toast-container');
  const div=document.createElement('div');
  const bg=type==='error'?'bg-red-600':type==='success'?'bg-emerald-600':'bg-indigo-600';
  div.className=`${bg} text-white px-5 py-2.5 rounded-lg font-bold shadow-xl text-sm fade-in`;
  div.textContent=msg;
  c.appendChild(div);
  setTimeout(()=>{div.style.opacity='0';div.style.transform='translateY(-10px)';div.style.transition='all .3s';setTimeout(()=>div.remove(),300);},2500);
}

// ─── INIT ─────────────────────────────────────────────────────────────
renderLotteryGrid();
updateTodaySales();
</script>
</body>
</html>'''

with open(r'c:\Users\villa\OneDrive\Documentos\appelarrejuntao\taquilla\index.html','w',encoding='utf-8') as f:
    f.write(HTML)

print('✓ taquilla/index.html creado')
print('Tamanio:', len(HTML), 'bytes')

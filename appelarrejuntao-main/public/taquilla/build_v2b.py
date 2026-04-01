#!/usr/bin/env python3
OUT = r'c:\Users\villa\OneDrive\Documentos\appelarrejuntao\taquilla\index.html'

P2 = r'''
<main class="flex-1 flex overflow-hidden relative bg-slate-900 no-print transition-colors">

<!-- POS VIEW -->
<div id="view-pos" class="w-full h-full flex flex-col hidden">
  <!-- Top Header Bar -->
  <div class="h-12 flex items-center justify-between px-4 bg-slate-900 border-b border-slate-800 shrink-0">
    <div class="flex items-center gap-3">
      <h2 class="text-white font-bold text-sm">Venta Taquilla</h2>
      <span class="text-slate-400 text-xs hidden sm:block" id="header-date">...</span>
    </div>
    <div class="flex items-center gap-4">
      <span id="header-time" class="font-mono text-xs text-slate-300">00:00:00</span>
      <div class="flex items-center gap-1.5">
        <span class="text-slate-500 text-xs">VENTAS HOY:</span>
        <span id="pos-today-sales" class="text-emerald-400 font-bold text-xs">Bs 0,00</span>
      </div>
    </div>
  </div>

  <!-- Betting Controls Bar -->
  <div class="bg-slate-900 border-b border-slate-800 px-4 py-3 shrink-0">
    <!-- Mode buttons row -->
    <div class="flex items-end gap-4 max-w-5xl mx-auto">
      <!-- Left: Animal / Arrejuntao -->
      <div class="flex gap-2 shrink-0">
        <button onclick="toggleAnimalitos()" class="h-14 px-3 rounded-lg flex flex-col items-center justify-center gap-0.5 bg-emerald-900/30 border border-emerald-700/50 text-emerald-400 hover:bg-emerald-800/40 transition-all">
          <span class="text-lg leading-none">🐾</span>
          <span class="text-[9px] font-bold uppercase">ANIMAL</span>
        </button>
        <button onclick="openMultiProductModal()" class="h-14 px-3 rounded-lg flex flex-col items-center justify-center gap-0.5 bg-orange-900/30 border border-orange-600/50 text-orange-400 hover:bg-orange-800/40 transition-all">
          <span class="text-lg leading-none">🔥</span>
          <span class="text-[9px] font-bold uppercase leading-tight text-center">EL<br>ARREJUNTAO</span>
        </button>
      </div>
      <!-- Divider -->
      <div class="w-px h-10 bg-slate-700 shrink-0"></div>
      <!-- Mode selector -->
      <div class="flex gap-2 shrink-0">
        <button onclick="setMode('normal')" id="btn-mode-normal" class="mode-btn h-14 px-3 rounded-lg flex flex-col items-center justify-center gap-0.5 bg-slate-800 border border-slate-700 text-slate-300 hover:bg-slate-700 transition-all min-w-[52px]">
          <span class="text-[8px] font-mono font-bold text-slate-500">≡≡≡</span>
          <span class="text-[9px] font-bold uppercase">SERIE</span>
          <span class="text-[7px] text-slate-500">0-9</span>
        </button>
        <button onclick="togglePermuta()" id="btn-permuta" class="mode-btn h-14 px-3 rounded-lg flex flex-col items-center justify-center gap-0.5 bg-slate-800 border border-slate-700 text-slate-300 hover:bg-slate-700 transition-all min-w-[52px]">
          <span class="text-[8px] font-mono font-bold text-slate-500">#</span>
          <span class="text-[9px] font-bold uppercase">PERMUTA</span>
          <span class="text-[7px] text-slate-500 leading-tight">Permutación</span>
        </button>
        <button onclick="setMode('terminal')" id="btn-mode-terminal" class="mode-btn h-14 px-3 rounded-lg flex flex-col items-center justify-center gap-0.5 bg-slate-800 border border-slate-700 text-slate-300 hover:bg-slate-700 transition-all min-w-[52px]">
          <span class="text-[8px] font-mono font-bold text-slate-500">##</span>
          <span class="text-[9px] font-bold uppercase">TERMINAL</span>
          <span class="text-[7px] text-slate-500">2 Dígitos</span>
        </button>
        <button onclick="setMode('cuatro')" id="btn-mode-cuatro" class="mode-btn h-14 px-3 rounded-lg flex flex-col items-center justify-center gap-0.5 bg-slate-800 border border-slate-700 text-slate-300 hover:bg-slate-700 transition-all min-w-[52px]">
          <span class="text-[8px] font-mono font-bold text-slate-500">####</span>
          <span class="text-[9px] font-bold uppercase">4 CIFRAS</span>
          <span class="text-[7px] text-slate-500">Completo</span>
        </button>
      </div>
      <!-- Divider -->
      <div class="w-px h-10 bg-slate-700 shrink-0 hidden sm:block"></div>
      <!-- Inputs -->
      <div class="flex items-end gap-3 flex-1">
        <div class="flex-1 max-w-[200px]">
          <label class="block text-[8px] font-bold text-slate-500 uppercase mb-1" id="label-bet-number">4 CIFRAS</label>
          <input type="text" id="betNumber" maxlength="3" autocomplete="off"
            class="block w-full bg-slate-800 border border-slate-700 text-white text-xl font-mono font-bold text-center h-11 rounded-lg focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none placeholder-slate-600"
            placeholder="----">
        </div>
        <div class="flex-1 max-w-[160px]">
          <div class="flex justify-between mb-1">
            <label class="text-[8px] font-bold text-slate-500 uppercase">MONTO</label>
            <span class="text-[7px] text-emerald-500 font-bold">MÍN 50 Bs</span>
          </div>
          <div class="flex items-center bg-slate-800 border border-slate-700 rounded-lg h-11 focus-within:border-emerald-500 focus-within:ring-1 focus-within:ring-emerald-500">
            <span class="text-slate-400 pl-3 font-bold text-sm">Bs</span>
            <input type="number" id="betAmount" class="flex-1 bg-transparent text-emerald-400 text-xl font-bold text-right pr-3 outline-none" placeholder="50">
          </div>
        </div>
        <button onclick="addBet(this)" class="h-11 px-6 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-lg flex items-center gap-2 text-sm uppercase tracking-wide transition-all active:scale-95 shadow-lg shadow-indigo-900/50">
          AGREGAR <span class="text-xl font-light">+</span>
        </button>
      </div>
    </div>
    <!-- Zodiac pills row -->
    <div class="flex overflow-x-auto gap-1.5 pt-3 no-scrollbar" id="zodiac-scroll"></div>
  </div>

  <!-- Main content: lottery grid + ticket -->
  <div class="flex-1 flex overflow-hidden">
    <!-- Lottery grid area -->
    <div class="flex-1 overflow-y-auto p-4 bg-slate-900">
      <p class="text-[10px] text-slate-500 uppercase font-bold tracking-wider mb-3">Loterías Disponibles</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3" id="lottery-grid-container"></div>
    </div>

    <!-- Ticket Panel (right side, always visible on desktop) -->
    <div id="pos-ticket-panel" class="fixed md:relative top-0 right-0 h-full w-[85%] sm:w-[300px] md:w-[300px] bg-slate-950 flex flex-col border-l border-slate-800 shadow-2xl md:shadow-none z-[55] md:z-10 transform translate-x-full md:translate-x-0 transition-transform duration-300 no-print">
      <div class="p-3 bg-slate-900 border-b border-slate-800 flex justify-between items-center shrink-0">
        <h3 class="text-white font-bold tracking-widest uppercase text-xs">Ticket en Curso</h3>
        <button class="md:hidden text-slate-500 hover:text-white" onclick="toggleMobileCart()">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
      <div class="flex-1 overflow-y-auto bg-slate-900 flex flex-col items-center p-3" id="receipts-container">
        <div class="text-center text-slate-600 text-xs italic mt-10">... Esperando apuestas ...</div>
      </div>
      <div class="p-3 bg-slate-900 border-t border-slate-800 shrink-0">
        <div class="flex justify-between items-center mb-3">
          <span class="text-slate-400 text-xs font-bold uppercase">Gran Total:</span>
          <span id="grand-total-live" class="text-white font-bold text-xl">Bs 0,00</span>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <button onclick="clearTicket()" class="bg-red-900/30 border border-red-800/50 text-red-400 hover:bg-red-900/50 py-2.5 rounded-lg font-bold text-[10px] uppercase tracking-wider">Cancelar (F2)</button>
          <button id="btn-print-main" onclick="openPrintPreview()" disabled class="bg-emerald-600 hover:bg-emerald-500 text-white py-2.5 rounded-lg font-bold text-[10px] uppercase tracking-wider opacity-50 cursor-not-allowed">Verificar (F10)</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Mobile overlay + FAB -->
  <div id="pos-ticket-overlay" class="fixed inset-0 bg-slate-900/70 z-[54] hidden md:hidden backdrop-blur-sm" onclick="toggleMobileCart()"></div>
  <button id="fab-main" onclick="toggleMobileCart()" class="md:hidden fixed bottom-6 right-4 z-[50] bg-emerald-600 text-white rounded-full px-5 py-3.5 shadow-2xl flex items-center gap-3 border border-emerald-500/40 active:scale-95 transition-transform">
    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
    <div class="flex flex-col text-left"><span class="text-[9px] uppercase font-bold text-emerald-200 leading-none">Ver Ticket</span><span id="mobile-cart-total" class="font-bold text-sm">Bs 0,00</span></div>
  </button>
</div>

<!-- MANAGEMENT VIEW -->
<div id="view-management" class="hidden w-full h-full flex flex-col p-4 bg-slate-900 overflow-y-auto">
  <div class="flex flex-col md:flex-row justify-between md:items-center gap-4 mb-5 border-b border-slate-800 pb-4">
    <h1 class="text-xl font-bold text-white">Gestión de Tickets</h1>
    <div class="flex flex-wrap gap-2">
      <input type="text" id="mgmt-search" placeholder="Buscar #" class="bg-slate-800 border border-slate-700 text-white px-3 py-2 rounded text-sm w-28 outline-none focus:border-indigo-500">
      <button onclick="filterTickets()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded text-sm font-bold">🔍</button>
      <button onclick="simulateWinners()" class="bg-purple-700 hover:bg-purple-600 text-white px-3 py-2 rounded text-xs font-bold">Simular Sorteo</button>
    </div>
  </div>
  <div class="flex gap-2 mb-4 overflow-x-auto no-scrollbar">
    <button onclick="filterStatus('all')" class="px-3 py-1.5 whitespace-nowrap bg-slate-800 rounded-full text-xs border border-slate-700 text-slate-300 hover:bg-slate-700">Todos</button>
    <button onclick="filterStatus('Pendiente')" class="px-3 py-1.5 whitespace-nowrap rounded-full text-xs border border-yellow-800 text-yellow-400">Pendientes</button>
    <button onclick="filterStatus('Ganador')" class="px-3 py-1.5 whitespace-nowrap rounded-full text-xs border border-emerald-800 text-emerald-400">Ganadores</button>
    <button onclick="filterStatus('Pagado')" class="px-3 py-1.5 whitespace-nowrap rounded-full text-xs border border-blue-800 text-blue-400">Pagados</button>
    <button onclick="filterStatus('Anulado')" class="px-3 py-1.5 whitespace-nowrap rounded-full text-xs border border-red-900 text-red-400">Anulados</button>
  </div>
  <div class="bg-slate-800 rounded-xl border border-slate-700 flex-1 overflow-auto">
    <table class="w-full text-left text-sm min-w-[500px]">
      <thead class="bg-slate-900 text-slate-400 uppercase text-xs font-bold sticky top-0">
        <tr><th class="p-3">Ticket</th><th class="p-3">Fecha/Hora</th><th class="p-3 text-right">Monto</th><th class="p-3 text-center">Estado</th><th class="p-3 text-center">Ver</th></tr>
      </thead>
      <tbody id="mgmt-table-body"></tbody>
    </table>
  </div>
</div>

<!-- REPORTS VIEW -->
<div id="view-reports" class="hidden w-full h-full flex flex-col p-4 bg-slate-900 overflow-y-auto">
  <div class="flex flex-col md:flex-row justify-between md:items-center gap-4 mb-5 border-b border-slate-800 pb-4">
    <h1 class="text-xl font-bold text-white">Reportes y Cierre</h1>
    <div class="flex gap-1.5 bg-slate-800 p-1 rounded-lg">
      <button onclick="switchReportTab('cierre')" id="rtab-cierre" class="px-3 py-2 rounded-md text-xs font-bold bg-purple-700 text-white">Cierre</button>
      <button onclick="switchReportTab('transacciones')" id="rtab-transacciones" class="px-3 py-2 rounded-md text-xs font-bold text-slate-400">Historial</button>
      <button onclick="switchReportTab('ganadores')" id="rtab-ganadores" class="px-3 py-2 rounded-md text-xs font-bold text-slate-400">Ganadores</button>
    </div>
  </div>
  <div id="report-content-cierre" class="flex-1 flex flex-col overflow-y-auto pb-6">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
      <div class="bg-slate-800 rounded-xl p-5 border border-slate-700"><h3 class="text-blue-400 text-xs font-bold uppercase mb-1">Ventas</h3><p id="cierre-sales" class="text-3xl font-bold text-white">Bs 0,00</p><p id="cierre-sales-count" class="text-xs text-slate-500">0 tickets</p></div>
      <div class="bg-slate-800 rounded-xl p-5 border border-slate-700"><h3 class="text-red-400 text-xs font-bold uppercase mb-1">Premios</h3><p id="cierre-payouts" class="text-3xl font-bold text-white">Bs 0,00</p><p id="cierre-payouts-count" class="text-xs text-slate-500">0 pagados</p></div>
      <div class="bg-emerald-900/30 rounded-xl p-5 border border-emerald-700/30"><h3 class="text-emerald-400 text-xs font-bold uppercase mb-1">Caja Neta</h3><p id="cierre-balance" class="text-3xl font-bold text-white">Bs 0,00</p></div>
    </div>
    <div class="flex gap-3 flex-wrap">
      <button onclick="realizarCierreZ()" class="bg-slate-700 hover:bg-slate-600 text-white px-6 py-3 rounded-lg font-bold text-sm">Imprimir Reporte Z</button>
      <button onclick="exportTransaccionesCSV()" class="bg-emerald-700 hover:bg-emerald-600 text-white px-6 py-3 rounded-lg font-bold text-sm">Exportar CSV</button>
    </div>
  </div>
  <div id="report-content-transacciones" class="hidden flex-1 overflow-auto">
    <div class="bg-slate-800 rounded-xl border border-slate-700 overflow-auto h-full">
      <table class="w-full text-left text-sm min-w-[400px]">
        <thead class="bg-slate-900 text-xs uppercase font-bold text-slate-400 sticky top-0"><tr><th class="p-3">Fecha</th><th class="p-3">Ticket</th><th class="p-3 text-right">Monto</th><th class="p-3 text-center">Estado</th></tr></thead>
        <tbody id="history-table-body"></tbody>
      </table>
    </div>
  </div>
  <div id="report-content-ganadores" class="hidden flex-1 overflow-auto">
    <div class="bg-slate-800 rounded-xl border border-slate-700 overflow-auto h-full">
      <table class="w-full text-left text-sm min-w-[400px]">
        <thead class="bg-slate-900 text-xs uppercase font-bold text-slate-400 sticky top-0"><tr><th class="p-3">Ticket</th><th class="p-3 text-right">Apostado</th><th class="p-3 text-right text-emerald-400">Premio</th><th class="p-3 text-center">Estado</th></tr></thead>
        <tbody id="winners-report-body"></tbody>
      </table>
    </div>
  </div>
</div>

<!-- CONFIG VIEW -->
<div id="view-config" class="hidden w-full h-full flex flex-col p-4 bg-slate-900 overflow-y-auto">
  <div class="mb-5 border-b border-slate-800 pb-4"><h1 class="text-xl font-bold text-white">Configuración</h1></div>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl">
    <div class="bg-slate-800 p-6 rounded-xl border border-slate-700">
      <h3 class="font-bold text-lg mb-4 text-indigo-400">Datos de la Agencia</h3>
      <div class="space-y-4">
        <div><label class="block text-xs font-bold text-slate-500 uppercase mb-1">Nombre Comercial</label><input type="text" id="cfg-agency-name" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-1 focus:ring-indigo-500 outline-none"></div>
        <div><label class="block text-xs font-bold text-slate-500 uppercase mb-1">RIF / Licencia</label><input type="text" id="cfg-agency-rif" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white focus:ring-1 focus:ring-indigo-500 outline-none"></div>
      </div>
    </div>
    <div class="bg-slate-800 p-6 rounded-xl border border-slate-700">
      <h3 class="font-bold text-lg mb-4 text-orange-400">Topes y Seguridad</h3>
      <div class="space-y-4">
        <div class="flex items-center justify-between"><label class="text-sm font-bold text-slate-300">Control de Topes</label><label class="relative inline-flex items-center cursor-pointer"><input type="checkbox" id="cfg-enable-topes" class="sr-only peer"><div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-orange-500"></div></label></div>
        <div><label class="block text-xs font-bold text-slate-500 uppercase mb-1">Tope Máximo (Bs)</label><input type="number" id="cfg-max-bet" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white outline-none"></div>
        <div><label class="block text-xs font-bold text-slate-500 uppercase mb-1">PIN de Seguridad</label><input type="password" id="cfg-pin" maxlength="4" class="w-32 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white outline-none font-mono text-center text-lg tracking-widest"></div>
      </div>
    </div>
  </div>
  <div class="mt-6"><button onclick="saveSystemConfig()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 px-8 rounded-lg">Guardar Cambios</button></div>
</div>
</main>
'''

with open(OUT, 'a', encoding='utf-8') as f:
    f.write(P2)
print("Part 2 written:", len(P2), "bytes")

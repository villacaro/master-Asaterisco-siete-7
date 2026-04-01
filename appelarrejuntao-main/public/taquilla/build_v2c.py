#!/usr/bin/env python3
OUT = r'c:\Users\villa\OneDrive\Documentos\appelarrejuntao\taquilla\index.html'

MODALS = r'''
<!-- ANIMALITOS MODAL -->
<div id="animalitos-modal" class="fixed inset-0 z-[70] bg-slate-900/90 flex items-center justify-center hidden backdrop-blur-md no-print p-0">
  <div class="w-full h-full flex flex-col md:flex-row relative">
    <div class="flex-1 flex flex-col h-full overflow-hidden bg-slate-50 dark:bg-slate-950 border-r border-slate-200 dark:border-slate-800">
      <div class="h-14 flex items-center justify-between px-3 md:px-6 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 shrink-0">
        <div class="flex items-center gap-3">
          <span class="text-2xl">🐾</span>
          <div><h2 class="text-slate-900 dark:text-white font-bold text-sm leading-tight">Apuestas de Animalitos</h2></div>
        </div>
        <button onclick="toggleAnimalitos()" class="text-slate-400 hover:text-slate-800 dark:hover:text-white p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
      <div class="flex-1 flex flex-col overflow-hidden">
        <div class="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 p-3 shrink-0">
          <label class="text-[9px] font-bold text-slate-500 uppercase mb-1 block">Loterías</label>
          <div id="animal-lottery-buttons" class="flex flex-wrap gap-1.5"></div>
        </div>
        <div class="bg-slate-50 dark:bg-slate-900/50 border-b border-slate-200 dark:border-slate-800 p-3 max-h-32 overflow-y-auto shrink-0">
          <div class="flex flex-col gap-2" id="animal-times-container"></div>
        </div>
        <div class="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 p-3 flex items-center gap-3 shrink-0">
          <div class="flex gap-1 bg-slate-100 dark:bg-slate-800 p-1 rounded-lg">
            <button onclick="setAnimalMode('normal')" id="btn-animal-normal" class="px-4 py-1.5 rounded-md text-xs font-bold bg-emerald-600 text-white">Normal</button>
            <button onclick="setAnimalMode('arrejuntao')" id="btn-animal-arrejuntao" class="px-4 py-1.5 rounded-md text-xs font-bold text-slate-500 dark:text-slate-400">Arrejuntao</button>
          </div>
          <div class="relative w-36">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 font-bold text-sm">Bs</span>
            <input type="number" id="animal-bet-amount" class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-600 text-emerald-600 dark:text-emerald-400 text-lg font-bold text-right py-1.5 px-3 rounded focus:ring-emerald-500 outline-none" placeholder="50">
          </div>
          <button onclick="toggleAllAnimals()" id="btn-toggle-all" class="text-xs text-indigo-500 font-bold border border-indigo-200 dark:border-indigo-900/50 px-3 py-2 rounded hover:bg-indigo-50 dark:hover:bg-indigo-900/20">Todos</button>
          <button onclick="addAnimalBets(this)" class="bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-2 rounded-lg font-bold text-sm shadow-lg ml-auto">Agregar</button>
        </div>
        <div class="flex-1 p-3 overflow-y-auto bg-slate-100 dark:bg-slate-950">
          <div class="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 lg:grid-cols-9 gap-1.5" id="animal-grid"></div>
        </div>
      </div>
      <button id="fab-animal" onclick="toggleAnimalMobileCart()" class="md:hidden absolute bottom-6 right-4 z-[70] bg-emerald-600 text-white rounded-full px-5 py-3.5 shadow-2xl flex items-center gap-3 border border-emerald-500/50 active:scale-95 transition-transform">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
        <span id="animal-mobile-cart-total" class="font-bold text-sm">Bs 0,00</span>
      </button>
      <div id="animal-ticket-overlay" class="fixed inset-0 bg-slate-900/60 z-[74] hidden md:hidden" onclick="toggleAnimalMobileCart()"></div>
    </div>
    <div id="animal-ticket-panel" class="fixed md:relative top-0 right-0 h-full w-[85%] sm:w-[310px] md:w-[310px] bg-white dark:bg-slate-950 flex flex-col border-l border-slate-200 dark:border-slate-800 shadow-2xl md:shadow-none z-[75] md:z-10 transform translate-x-full md:translate-x-0 transition-transform duration-300">
      <div class="p-3 bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center shrink-0">
        <h3 class="text-slate-800 dark:text-white font-bold uppercase text-xs">Ticket en Curso</h3>
        <button class="md:hidden bg-slate-200 dark:bg-slate-800 rounded-full p-1" onclick="toggleAnimalMobileCart()"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button>
      </div>
      <div class="flex-1 p-3 bg-slate-100 dark:bg-slate-900 overflow-y-auto flex flex-col items-center pb-4" id="receipts-container-modal">
        <div class="text-center text-gray-400 text-xs italic mt-10">... Esperando apuestas ...</div>
      </div>
      <div class="p-3 bg-slate-50 dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 shrink-0">
        <div class="flex justify-between items-end mb-3 px-2"><span class="font-bold text-slate-500 text-xs">GRAN TOTAL:</span><span id="grand-total-live-modal" class="font-bold text-xl text-slate-800 dark:text-white">Bs 0,00</span></div>
        <div class="grid grid-cols-2 gap-2">
          <button onclick="clearTicket()" class="bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 py-2 rounded font-bold border border-red-200 dark:border-red-900/50 text-[10px] uppercase">Cancelar</button>
          <button id="btn-print-modal" onclick="openPrintPreview()" class="bg-emerald-600 text-white py-2 rounded font-bold text-[10px] uppercase opacity-50 cursor-not-allowed" disabled>Verificar</button>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- MULTI-PRODUCT MODAL (El Arrejuntao) -->
<div id="multi-product-modal" class="fixed inset-0 z-[80] bg-slate-900/90 flex items-center justify-center hidden backdrop-blur-md no-print">
  <div class="w-full h-full flex flex-col md:flex-row relative">
    <div class="flex-1 flex flex-col h-full overflow-hidden bg-slate-50 dark:bg-slate-950">
      <div class="h-14 flex items-center justify-between px-3 md:px-6 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 shrink-0">
        <div class="flex items-center gap-3"><span class="text-2xl">🔥</span><h3 class="text-slate-900 dark:text-white font-bold text-sm">Sistema Asterisco Siete (*7) — Modalidades</h3></div>
        <button onclick="closeMultiProductModal()" class="text-slate-400 hover:text-slate-800 dark:hover:text-white p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button>
      </div>
      <div class="flex-1 overflow-y-auto p-5 md:p-8 flex flex-col gap-6 pb-24 md:pb-8 bg-slate-50 dark:bg-slate-950">
        <div>
          <div class="flex items-center gap-2 mb-3"><span class="w-6 h-6 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center justify-center text-[10px] font-bold">1</span><h4 class="text-slate-500 dark:text-slate-400 font-bold text-xs uppercase">Seleccione Horario</h4></div>
          <div class="flex flex-wrap gap-2 pl-8" id="multi-times-container"></div>
        </div>
        <div>
          <div class="flex items-center gap-2 mb-3"><span class="w-6 h-6 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center justify-center text-[10px] font-bold">2</span><h4 class="text-slate-500 dark:text-slate-400 font-bold text-xs uppercase">Categoría Principal</h4></div>
          <div class="flex flex-wrap gap-3 pl-8" id="multi-categories-container"></div>
        </div>
        <div>
          <div class="flex items-center gap-2 mb-3"><span class="w-6 h-6 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center justify-center text-[10px] font-bold">3</span><h4 class="text-slate-500 dark:text-slate-400 font-bold text-xs uppercase">Apuestas Adicionales</h4></div>
          <div class="flex flex-wrap gap-3 pl-8" id="multi-additional-container"></div>
        </div>
        <div class="bg-white dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700/50 rounded-2xl p-4 md:p-6 flex flex-col md:flex-row gap-3 items-end mt-2 shadow-sm">
          <div class="flex-1 w-full"><label class="block text-[9px] font-bold text-slate-500 uppercase mb-1">Número (3 Cifras)</label><input type="text" id="multi-bet-number" maxlength="3" class="w-full bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-600 text-slate-900 dark:text-white text-xl font-mono font-bold text-center h-11 rounded-lg focus:border-orange-500 focus:ring-2 focus:ring-orange-500/30 outline-none" placeholder="---" autocomplete="off"></div>
          <div class="flex-1 w-full"><label class="block text-[9px] font-bold text-slate-500 uppercase mb-1">Monto</label><div class="relative"><span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 font-bold text-sm">Bs</span><input type="number" id="multi-bet-amount" class="w-full bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-600 text-emerald-600 dark:text-emerald-400 text-xl font-mono font-bold text-right h-11 pr-3 pl-8 rounded-lg focus:border-orange-500 focus:ring-2 focus:ring-orange-500/30 outline-none" placeholder="50"></div></div>
          <button onclick="addMultiBet()" class="w-full md:w-auto h-11 px-6 md:px-8 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white font-bold rounded-lg shadow-lg active:scale-95 transition-all flex items-center justify-center gap-2 uppercase tracking-wide text-sm">Agregar <span class="text-xl font-light">+</span></button>
        </div>
      </div>
    </div>
    <div id="multi-ticket-panel" class="fixed md:relative top-0 right-0 h-full w-[85%] sm:w-[310px] md:w-[310px] bg-white dark:bg-slate-950 flex flex-col border-l border-slate-200 dark:border-slate-800 shadow-2xl md:shadow-none z-[85] md:z-10 transform translate-x-full md:translate-x-0 transition-transform duration-300">
      <div class="p-3 bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 shrink-0 flex justify-between items-center">
        <h3 class="text-slate-800 dark:text-white font-bold uppercase text-xs">Ticket en Curso</h3>
        <button class="md:hidden bg-slate-200 dark:bg-slate-800 rounded-full p-1" onclick="toggleMultiMobileCart()"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button>
      </div>
      <div class="flex-1 p-3 bg-slate-100 dark:bg-slate-900 overflow-y-auto items-center pb-4" id="receipts-container-multi"><div class="text-center text-gray-400 text-xs italic mt-10">... Esperando apuestas ...</div></div>
      <div class="p-3 bg-slate-50 dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 shrink-0">
        <div class="flex justify-between items-end mb-3 px-2"><span class="font-bold text-slate-500 text-xs">GRAN TOTAL:</span><span id="grand-total-live-multi" class="font-bold text-xl text-slate-800 dark:text-white">Bs 0,00</span></div>
        <div class="grid grid-cols-2 gap-2"><button onclick="clearTicket()" class="bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 py-2 rounded font-bold border border-red-200 text-[10px] uppercase">Cancelar</button><button id="btn-print-multi" onclick="openPrintPreview()" class="bg-emerald-600 text-white py-2 rounded font-bold text-[10px] uppercase opacity-50 cursor-not-allowed" disabled>Verificar</button></div>
      </div>
    </div>
    <div id="multi-ticket-overlay" class="fixed inset-0 bg-slate-900/60 z-[83] hidden md:hidden" onclick="toggleMultiMobileCart()"></div>
    <button id="fab-multi" onclick="toggleMultiMobileCart()" class="md:hidden absolute bottom-6 right-4 z-[82] bg-orange-600 text-white rounded-full px-5 py-3.5 shadow-2xl flex items-center gap-3 border border-orange-500/50 active:scale-95 transition-transform"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg><span id="multi-mobile-cart-total" class="font-bold text-sm">Bs 0,00</span></button>
  </div>
</div>

<!-- PREVIEW MODAL -->
<div id="preview-modal" class="fixed inset-0 z-[100] bg-black/80 flex items-center justify-center hidden backdrop-blur-sm no-print p-4">
  <div class="bg-white text-black rounded-lg w-full max-w-[320px] overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
    <div class="p-4 bg-slate-800 text-white flex justify-between items-center shrink-0"><h3 class="font-bold text-sm uppercase">Confirmar Ticket</h3><button onclick="closePreview()" class="text-slate-400 hover:text-white"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div>
    <div class="p-4 overflow-y-auto bg-slate-100 flex justify-center"><div id="final-ticket-preview" class="w-full"></div></div>
    <div class="p-3 bg-gray-50 border-t border-gray-200 flex gap-2 shrink-0">
      <button onclick="closePreview()" class="flex-1 py-2 rounded border border-gray-300 font-bold text-xs uppercase hover:bg-gray-100">Cancelar</button>
      <button onclick="confirmAndDownloadPDF()" class="flex-1 py-2 rounded bg-orange-600 text-white font-bold text-xs uppercase hover:bg-orange-500">PDF</button>
      <button onclick="confirmAndPrint()" class="flex-1 py-2 rounded bg-indigo-600 text-white font-bold text-xs uppercase hover:bg-indigo-500">Imprimir</button>
    </div>
  </div>
</div>

<!-- ACTION MODAL -->
<div id="action-modal" class="fixed inset-0 z-[110] bg-black/80 flex items-center justify-center hidden backdrop-blur-sm no-print p-4">
  <div class="bg-white dark:bg-slate-800 rounded-xl w-full max-w-lg flex flex-col max-h-[90vh]">
    <div class="p-4 border-b border-slate-200 dark:border-slate-700 flex justify-between items-center"><h3 class="text-slate-800 dark:text-white font-bold text-lg">Detalle de Ticket</h3><button onclick="closeActionModal()" class="text-slate-400 hover:text-slate-800 dark:hover:text-white"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div>
    <div class="p-6 overflow-y-auto bg-slate-100 dark:bg-slate-900 flex justify-center"><div id="action-ticket-preview" class="w-full"></div></div>
    <div class="p-4 border-t border-slate-200 dark:border-slate-700 flex flex-wrap justify-center gap-2" id="action-buttons"></div>
  </div>
</div>

<!-- VOID CONFIRM MODAL -->
<div id="void-confirm-modal" class="fixed inset-0 z-[120] bg-black/90 flex items-center justify-center hidden backdrop-blur-md p-4">
  <div class="bg-white dark:bg-slate-900 border border-red-500/50 rounded-xl w-full max-w-sm p-6 shadow-2xl">
    <h3 class="text-red-500 font-bold text-lg mb-2">⚠ Anular Ticket</h3>
    <p class="text-slate-600 dark:text-slate-300 text-sm mb-4">¿Está seguro? Esta acción no se puede deshacer.</p>
    <input type="text" id="void-reason" placeholder="Motivo de anulación..." class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-red-500/30 rounded p-3 text-slate-900 dark:text-white mb-4 text-sm outline-none focus:border-red-500">
    <div class="flex gap-2"><button onclick="closeVoidModal()" class="flex-1 py-3 rounded bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-white text-xs font-bold hover:bg-slate-300">Cancelar</button><button onclick="processVoid()" class="flex-1 py-3 rounded bg-red-600 text-white text-xs font-bold hover:bg-red-500">Confirmar</button></div>
  </div>
</div>

<!-- LOGIN MODAL -->
<div id="login-modal" class="fixed inset-0 z-[999] bg-slate-900 flex items-center justify-center">
  <div class="bg-white dark:bg-slate-800 p-8 rounded-2xl shadow-2xl w-full max-w-sm mx-4 flex flex-col items-center border border-slate-700">
    <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center text-white font-black text-2xl shadow-lg mb-6">*7</div>
    <h2 class="text-2xl font-bold text-slate-900 dark:text-white mb-2">Asterisco Siete</h2>
    <p class="text-sm text-slate-500 dark:text-slate-400 mb-6 text-center">Ingrese su PIN de acceso.</p>
    <input type="password" id="login-pin-input" maxlength="4" placeholder="••••" autocomplete="off" class="w-full text-center text-3xl tracking-[1em] font-mono bg-slate-50 dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl py-4 outline-none focus:border-indigo-500 mb-6 text-slate-900 dark:text-white">
    <button onclick="attemptLogin()" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-4 rounded-xl shadow-lg text-lg">INGRESAR</button>
  </div>
</div>

<!-- GENERIC CONFIRM MODAL -->
<div id="generic-confirm-modal" class="fixed inset-0 z-[200] bg-black/80 flex items-center justify-center hidden backdrop-blur-sm p-4">
  <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl w-full max-w-sm p-6 shadow-2xl text-center">
    <h3 id="generic-confirm-title" class="text-slate-900 dark:text-white font-bold text-xl mb-2">Confirmar</h3>
    <p id="generic-confirm-msg" class="text-slate-500 dark:text-slate-400 text-sm mb-6">¿Está seguro?</p>
    <div class="grid grid-cols-2 gap-3">
      <button onclick="closeGenericConfirm()" class="py-3 rounded-lg border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 font-bold hover:bg-slate-50 dark:hover:bg-slate-800 uppercase text-xs">Cancelar</button>
      <button id="generic-confirm-btn" class="py-3 rounded-lg bg-blue-600 text-white font-bold hover:bg-blue-500 uppercase text-xs">Confirmar</button>
    </div>
  </div>
</div>

<div id="toast-container" class="fixed top-4 left-1/2 transform -translate-x-1/2 z-[999] flex flex-col gap-2 pointer-events-none"></div>
<div id="printable-area" class="hidden"></div>
'''

with open(OUT, 'a', encoding='utf-8') as f:
    f.write(MODALS)
print("Modals written:", len(MODALS), "bytes")

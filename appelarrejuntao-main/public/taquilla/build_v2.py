#!/usr/bin/env python3
# Script generador del HTML completo - Taquilla Asterisco Siete (*7)
import os
OUT = r'c:\Users\villa\OneDrive\Documentos\appelarrejuntao\taquilla\index.html'

P1 = r'''<!DOCTYPE html>
<html lang="es" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Taquilla Asterisco Siete (*7)</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
<script>
if(localStorage.theme==='dark'||(!('theme'in localStorage)&&window.matchMedia('(prefers-color-scheme: dark)').matches)){document.documentElement.classList.add('dark')}else{document.documentElement.classList.remove('dark')}
tailwind.config={darkMode:'class',theme:{extend:{fontFamily:{sans:['Inter','sans-serif'],mono:['Roboto Mono','monospace']},colors:{thermal:{bg:'#fffdf0',text:'#1a1a1a'}}}}}
</script>
<style>
::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:3px}.dark ::-webkit-scrollbar-thumb{background:#475569}
.no-scrollbar::-webkit-scrollbar{display:none}.no-scrollbar{-ms-overflow-style:none;scrollbar-width:none}
.thermal-receipt{background:#fff;color:#000;font-family:'Courier New',monospace;font-size:11px;line-height:1.3;padding:14px;width:100%;max-width:310px;margin:0 auto;border-bottom:2px dashed #ccc}
.receipt-header{text-align:center;margin-bottom:8px}.receipt-title{font-size:15px;font-weight:900}.receipt-info{font-size:9px}
.receipt-divider{border-bottom:1px dashed #000;margin:6px 0;width:100%}
.receipt-row{display:flex;justify-content:space-between;margin-bottom:3px;font-size:10px}
.receipt-item-row{display:flex;justify-content:space-between;margin-bottom:2px;font-size:10px;align-items:center}
.receipt-total{font-size:13px;font-weight:bold;margin-top:5px;border-top:1px solid #000;padding-top:4px;display:flex;justify-content:space-between}
.receipt-footer{margin-top:8px;text-align:center;font-size:9px}
.lottery-btn{transition:all .1s}
.lottery-btn.selected-morning{background:#facc15;color:#422006;border-color:#eab308;font-weight:800}
.lottery-btn.selected-afternoon{background:#3b82f6;color:#fff;border-color:#2563eb;font-weight:800}
.lottery-btn.selected-night{background:#ef4444;color:#fff;border-color:#dc2626;font-weight:800}
.mod-btn{font-size:.65rem;border-radius:4px;border:1px solid #cbd5e1;color:#64748b;font-weight:bold;transition:all .1s;display:flex;align-items:center;justify-content:center}
.dark .mod-btn{border-color:#475569;color:#94a3b8}
.mod-btn:hover{background:#e2e8f0;color:#1e293b}.dark .mod-btn:hover{background:#334155;color:#fff}
.mod-btn.active{background:#4f46e5;border-color:#4f46e5;color:#fff}
.animal-btn{display:flex;flex-direction:column;align-items:center;justify-content:center;height:58px;border-radius:8px;border:1px solid #e2e8f0;background:#f8fafc;color:#475569;transition:all .1s;cursor:pointer}
.dark .animal-btn{border-color:#334155;background:#1e293b;color:#cbd5e1}
.animal-btn:hover{background:#e2e8f0}.dark .animal-btn:hover{background:#334155}
.animal-btn.selected{background:#059669;border-color:#10b981;color:#fff}
.animal-number{font-size:1rem;font-weight:bold;line-height:1}
.animal-name{font-size:.58rem;text-transform:uppercase;margin-top:2px;text-align:center;line-height:1.1}
.opt-btn{display:flex;flex-direction:column;justify-content:center;align-items:center;height:48px;padding:0 4px;border-radius:12px;border:1px solid;transition:all .2s;cursor:pointer;user-select:none;position:relative;overflow:hidden}
.opt-btn-inactive{background:#fff;border-color:#e2e8f0;color:#64748b}.dark .opt-btn-inactive{background:#1e293b;border-color:#334155;color:#94a3b8}
.opt-btn-active{background:linear-gradient(to bottom,#6366f1,#4f46e5);border-color:#6366f1;color:#fff;box-shadow:0 4px 15px rgba(99,102,241,.3);transform:scale(1.05)}
.fade-in{animation:fadeIn .3s ease-out}
@keyframes fadeIn{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulseGlow{0%,100%{box-shadow:0 0 12px rgba(99,102,241,.4)}50%{box-shadow:0 0 24px rgba(99,102,241,.7)}}
@media print{body *{visibility:hidden}#printable-area,#printable-area *{visibility:visible}#printable-area{position:absolute;left:0;top:0;width:100%;background:#fff;color:#000}nav,.modal-backdrop,.no-print{display:none!important}}
</style>
</head>
<body class="bg-slate-50 text-slate-800 dark:bg-slate-900 dark:text-slate-200 font-sans antialiased overflow-hidden h-screen flex flex-col-reverse md:flex-row transition-colors duration-300">

<!-- NAV -->
<nav class="w-full h-16 md:w-20 md:h-full flex-shrink-0 bg-white dark:bg-slate-950 border-t md:border-t-0 md:border-r border-slate-200 dark:border-slate-800 flex flex-row md:flex-col justify-around md:justify-between items-center py-2 md:py-6 z-[60] no-print transition-colors duration-300">
  <div class="flex flex-row md:flex-col items-center gap-1 md:gap-4 w-full md:w-auto justify-around md:justify-start">
    <div class="hidden md:flex w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl items-center justify-center text-white font-black text-sm shadow-lg">*7</div>
    <div class="flex flex-row md:flex-col gap-1 w-full md:w-auto px-2 justify-around flex-1">
      <button onclick="changeView('pos')" id="nav-pos" class="nav-btn p-2 md:p-3 rounded-xl bg-slate-100 text-indigo-600 dark:bg-slate-800 dark:text-indigo-400 transition-colors" title="Taquilla">
        <svg class="w-5 h-5 md:w-6 md:h-6 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
        <span class="text-[8px] font-bold hidden md:block mt-0.5">POS</span>
      </button>
      <button onclick="toggleAnimalitos()" class="nav-btn p-2 md:p-3 rounded-xl text-emerald-600 hover:bg-emerald-50 dark:text-emerald-400 dark:hover:bg-emerald-900/30 transition-colors" title="Animalitos">
        <svg class="w-5 h-5 md:w-6 md:h-6 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        <span class="text-[8px] font-bold hidden md:block mt-0.5">Animal</span>
      </button>
      <button onclick="changeView('management')" id="nav-management" class="nav-btn p-2 md:p-3 rounded-xl text-blue-600 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900/30 transition-colors" title="Gestión">
        <svg class="w-5 h-5 md:w-6 md:h-6 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/></svg>
        <span class="text-[8px] font-bold hidden md:block mt-0.5">Tickets</span>
      </button>
      <button onclick="changeView('reports')" id="nav-reports" class="nav-btn p-2 md:p-3 rounded-xl text-purple-600 hover:bg-purple-50 dark:text-purple-400 dark:hover:bg-purple-900/30 transition-colors" title="Reportes">
        <svg class="w-5 h-5 md:w-6 md:h-6 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
        <span class="text-[8px] font-bold hidden md:block mt-0.5">Reportes</span>
      </button>
      <button onclick="changeView('config')" id="nav-config" class="nav-btn p-2 md:p-3 rounded-xl text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors hidden sm:block" title="Config">
        <svg class="w-5 h-5 md:w-6 md:h-6 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
      </button>
    </div>
    <div class="flex flex-row md:flex-col items-center gap-1 border-l md:border-l-0 md:border-t border-slate-200 dark:border-slate-800 pl-2 md:pl-0 md:pt-4">
      <button onclick="toggleTheme()" class="p-2 md:p-3 rounded-xl text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-orange-500 dark:hover:text-yellow-400 transition-colors" title="Tema">
        <svg class="w-5 h-5 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
        <svg class="w-5 h-5 block dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
      </button>
      <button onclick="location.reload()" class="p-2 md:p-3 text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl transition-colors" title="Salir">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
      </button>
    </div>
  </div>
</nav>
'''

print("Part 1 ready:", len(P1), "bytes")

# Write part 1
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(P1)

print("Part 1 written.")

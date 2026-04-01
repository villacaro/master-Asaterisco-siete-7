#!/usr/bin/env python3
OUT = r'c:\Users\villa\OneDrive\Documentos\appelarrejuntao\taquilla\index.html'

JS1 = r'''
<script>
// ─── CONFIG ──────────────────────────────────────────────────
let sysConfig = JSON.parse(localStorage.getItem('ast7_config')||'null') || {
  agencyName:'ASTERISCO SIETE (*7)', agencyRif:'Licencia: *7-0001',
  securityPin:'1234', enableTopes:false, maxBet:2000
};

// ─── LOTTERIES ───────────────────────────────────────────────
const lotteryConfig = [
  {name:'Táchira'},{name:'Zulia'},{name:'Chance'},{name:'Caracas'},
  {name:'Caliente'},{name:'Zamorano'},{name:'SUPERGANA'},{name:'TRIPLE GANA'},{name:'NAPA GANA'}
];
const lotteryDrawTimes = {morning:'11:15',afternoon:'15:30',night:'19:00'};

const zodiacs = [
  {code:'ari',name:'Aries',icon:'♈'},{code:'tau',name:'Tauro',icon:'♉'},
  {code:'gem',name:'Géminis',icon:'♊'},{code:'can',name:'Cáncer',icon:'♋'},
  {code:'leo',name:'Leo',icon:'♌'},{code:'vir',name:'Virgo',icon:'♍'},
  {code:'lib',name:'Libra',icon:'♎'},{code:'esc',name:'Escorpio',icon:'♏'},
  {code:'sag',name:'Sagitario',icon:'♐'},{code:'cap',name:'Capricornio',icon:'♑'},
  {code:'acu',name:'Acuario',icon:'♒'},{code:'pis',name:'Piscis',icon:'♓'}
];

// ─── ANIMALS ─────────────────────────────────────────────────
const animalsStandard = [
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
const animalsArrejuntao = [
  {n:'1',name:'Perro'},{n:'2',name:'Gato'},{n:'3',name:'Ratón'},{n:'4',name:'Conejo'},
  {n:'5',name:'Tortuga'},{n:'6',name:'Mono'},{n:'7',name:'Loro'},{n:'8',name:'Pato'},
  {n:'9',name:'León'},{n:'10',name:'Tigre'},{n:'11',name:'Oso'},{n:'12',name:'Elefante'},
  {n:'13',name:'Cebra'},{n:'14',name:'Jirafa'},{n:'15',name:'Caballo'},{n:'16',name:'Vaca'},
  {n:'17',name:'Gallina'},{n:'18',name:'Pez'},{n:'19',name:'Águila'},{n:'20',name:'Serpiente'}
];
const animalsGuacharo = [
  {n:'01',name:'Boa'},{n:'02',name:'Puma'},{n:'03',name:'Tapir'},{n:'04',name:'Jaguar'},
  {n:'05',name:'Cóndor'},{n:'06',name:'Danta'},{n:'07',name:'Armadillo'},{n:'08',name:'Guácharo'},
  {n:'09',name:'Tucaneta'},{n:'10',name:'Anaconda'},{n:'11',name:'Caiman'},{n:'12',name:'Tonina'}
];

const animalLotteriesList = ['Lotto Activo','La Granjita','Animalitos Arrejuntao','Selva Plus','Guacharo Activo'];
const timesStandard = ['9AM','12PM','3PM','7PM'];
const timesArrejuntao = ['9AM','11AM','2PM','5PM','7PM'];

const animalColors = {
  'Lotto Activo':   {main:'bg-emerald-600 text-white border-emerald-500',ghost:'border-slate-300 dark:border-slate-600 text-slate-500 dark:text-slate-400 hover:border-emerald-500 hover:text-emerald-600'},
  'La Granjita':    {main:'bg-amber-500 text-white border-amber-400',ghost:'border-slate-300 dark:border-slate-600 text-slate-500 dark:text-slate-400 hover:border-amber-400 hover:text-amber-600'},
  'Animalitos Arrejuntao':{main:'bg-orange-600 text-white border-orange-500',ghost:'border-slate-300 dark:border-slate-600 text-slate-500 dark:text-slate-400 hover:border-orange-500 hover:text-orange-600'},
  'Selva Plus':     {main:'bg-teal-600 text-white border-teal-500',ghost:'border-slate-300 dark:border-slate-600 text-slate-500 dark:text-slate-400 hover:border-teal-500 hover:text-teal-600'},
  'Guacharo Activo':{main:'bg-purple-600 text-white border-purple-500',ghost:'border-slate-300 dark:border-slate-600 text-slate-500 dark:text-slate-400 hover:border-purple-500 hover:text-purple-600'}
};

// ─── STATE ───────────────────────────────────────────────────
let currentTicket = [];
let selectedLotteries = []; // [{name,type,sub}]
let selectedMainZodiacs = [];
let betMode = 'normal';
let permuta = false;
let nextTicketId = parseInt(localStorage.getItem('ast7_nextid')||'1001');
let allTransactions = JSON.parse(localStorage.getItem('ast7_tx')||'[]');
let selectedTxId = null;
let currentStatusFilter = 'all';
let currentReportTab = 'cierre';
// animal state
let selectedAnimalLotteries = ['Lotto Activo'];
let selectedAnimalTimes = [];
let selectedAnimals = [];
let animalBetMode = 'normal';
// multi-product state
let multiSelectedTimes = [];
let multiSelectedCategories = [];
let multiSelectedAdditional = [];

const multiTimesOptions = ['9AM','11AM','2PM','5PM','7PM'];
const multiCategories = [
  {id:'tripleA',label:'TRIPLE A',color:'bg-orange-600 border-orange-500'},
  {id:'tripleB',label:'TRIPLE B',color:'bg-red-600 border-red-500'},
  {id:'tripleSigno',label:'TRIPLE+SIGNO',color:'bg-yellow-500 border-yellow-400'},
  {id:'arrimao',label:'EL ARRIMAO',color:'bg-pink-600 border-pink-500'},
  {id:'pegadito',label:'EL PEGADITO',color:'bg-orange-500 border-orange-400'},
];
const multiAdditional = [
  {id:'terminalA',label:'TERMINAL A',color:'bg-orange-600 border-orange-500'},
  {id:'terminalB',label:'TERMINAL B',color:'bg-red-600 border-red-500'},
  {id:'permutaA',label:'PERMUTA A',color:'bg-indigo-600 border-indigo-500'},
  {id:'permutaB',label:'PERMUTA B',color:'bg-blue-600 border-blue-500'},
  {id:'serieA',label:'SERIE A',color:'bg-slate-600 border-slate-500'},
  {id:'serieB',label:'SERIE B',color:'bg-slate-500 border-slate-400'},
];

// ─── PERSIST ────────────────────────────────────────────────
function saveData(){
  localStorage.setItem('ast7_tx',JSON.stringify(allTransactions));
  localStorage.setItem('ast7_nextid',String(nextTicketId));
  localStorage.setItem('ast7_config',JSON.stringify(sysConfig));
}

// ─── CLOCK ──────────────────────────────────────────────────
function updateClock(){
  const n=new Date(),pad=x=>String(x).padStart(2,'0');
  const t=`${pad(n.getHours())}:${pad(n.getMinutes())}:${pad(n.getSeconds())}`;
  const d=n.toLocaleDateString('es-VE',{weekday:'short',day:'numeric',month:'short'});
  const el=document.getElementById('header-time');if(el)el.textContent=t;
  const de=document.getElementById('header-date');if(de)de.textContent=d;
}
setInterval(updateClock,1000);updateClock();

// ─── THEME ──────────────────────────────────────────────────
function toggleTheme(){
  const d=document.documentElement;
  if(d.classList.contains('dark')){d.classList.remove('dark');localStorage.theme='light';}
  else{d.classList.add('dark');localStorage.theme='dark';}
}

// ─── TOAST ──────────────────────────────────────────────────
function showToast(msg,type='info'){
  const c=document.getElementById('toast-container');
  const d=document.createElement('div');
  const cls=type==='error'?'bg-red-600':type==='success'?'bg-emerald-600':type==='warn'?'bg-amber-500':'bg-indigo-600';
  d.className=`${cls} text-white px-5 py-3 rounded-lg font-semibold shadow-xl text-sm fade-in pointer-events-none`;
  d.textContent=msg;c.appendChild(d);
  setTimeout(()=>{d.style.opacity='0';d.style.transition='opacity .3s';setTimeout(()=>d.remove(),300);},3000);
}

// ─── CONFIRM ────────────────────────────────────────────────
let confirmCallback=null;
function showConfirm(title,msg,cb){
  document.getElementById('generic-confirm-title').textContent=title;
  document.getElementById('generic-confirm-msg').textContent=msg;
  confirmCallback=cb;
  document.getElementById('generic-confirm-modal').classList.remove('hidden');
}
function closeGenericConfirm(){document.getElementById('generic-confirm-modal').classList.add('hidden');confirmCallback=null;}
document.getElementById('generic-confirm-btn').onclick=()=>{if(confirmCallback)confirmCallback();closeGenericConfirm();};

// ─── MOBILE DRAWERS ─────────────────────────────────────────
function toggleMobileCart(){
  const p=document.getElementById('pos-ticket-panel');
  const o=document.getElementById('pos-ticket-overlay');
  const open=p.classList.contains('translate-x-0');
  p.classList.toggle('translate-x-0',!open);p.classList.toggle('translate-x-full',open);
  o.classList.toggle('hidden',open);
}
function toggleAnimalMobileCart(){
  const p=document.getElementById('animal-ticket-panel');
  const o=document.getElementById('animal-ticket-overlay');
  const open=p.classList.contains('translate-x-0');
  p.classList.toggle('translate-x-0',!open);p.classList.toggle('translate-x-full',open);
  o.classList.toggle('hidden',open);
}
function toggleMultiMobileCart(){
  const p=document.getElementById('multi-ticket-panel');
  const o=document.getElementById('multi-ticket-overlay');
  const open=p.classList.contains('translate-x-0');
  p.classList.toggle('translate-x-0',!open);p.classList.toggle('translate-x-full',open);
  o.classList.toggle('hidden',open);
}

// ─── VIEWS ──────────────────────────────────────────────────
function changeView(v){
  ['pos','management','reports','config'].forEach(n=>{
    document.getElementById('view-'+n).classList.add('hidden');
    const b=document.getElementById('nav-'+n);
    if(b)b.className=b.className.replace('bg-slate-100 text-indigo-600 dark:bg-slate-800 dark:text-indigo-400','text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800');
  });
  document.getElementById('view-'+v).classList.remove('hidden');
  const ab=document.getElementById('nav-'+v);
  if(ab)ab.className=ab.className.replace('text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800','bg-slate-100 text-indigo-600 dark:bg-slate-800 dark:text-indigo-400');
  if(v==='management')renderManagementTable();
  if(v==='reports'){renderCierreDeCaja();renderHistoryTable();}
  if(v==='config')loadSystemConfig();
}

// ─── RECEIPT LAYOUT ─────────────────────────────────────────
function genCode(){return Array.from({length:10},()=>'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'[Math.floor(Math.random()*32)]).join('');}

function renderReceiptLayout(items,total,ticketId,code,dateStr,timeStr,editable,status){
  if(!items||!items.length)return '<div class="text-center text-gray-400 text-xs italic mt-8">... Esperando apuestas ...</div>';
  const wm=status==='Anulado'?'ANULADO':status==='Pagado'?'PAGADO':'';
  let rows=items.map((it,i)=>`
    <div style="display:flex;justify-content:space-between;margin-bottom:3px;font-size:10px;align-items:center">
      <div style="flex:1;overflow:hidden;padding-right:4px">
        <div style="font-weight:bold;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:9px">${it.lottery||it.type}</div>
        <div style="font-size:9px;color:#555">${it.number||it.animal||''}</div>
      </div>
      <div style="text-align:right;min-width:52px;font-weight:bold">Bs ${it.amount.toFixed(2)}</div>
      ${editable?`<div onclick="removeBet(${i})" style="cursor:pointer;color:#dc2626;padding-left:6px;font-size:16px;font-weight:bold;line-height:1">×</div>`:''}
    </div>`).join('');
  return `<div class="thermal-receipt" style="position:relative">
    ${wm?`<div style="position:absolute;top:40%;left:50%;transform:translate(-50%,-50%) rotate(-30deg);font-size:42px;font-weight:900;color:rgba(220,38,38,0.15);pointer-events:none;white-space:nowrap;z-index:10">${wm}</div>`:''}
    <div class="receipt-header"><div class="receipt-title">${sysConfig.agencyName}</div><div class="receipt-info">${sysConfig.agencyRif}</div></div>
    <div class="receipt-divider"></div>
    <div class="receipt-row"><span>Ticket: #${ticketId||'------'}</span><span>${dateStr||new Date().toLocaleDateString('es-VE')}</span></div>
    <div class="receipt-row"><span>Código: ${code||'----------'}</span><span>${timeStr||new Date().toLocaleTimeString('es-VE',{hour12:true})}</span></div>
    <div class="receipt-divider"></div>
    <div style="display:flex;justify-content:space-between;font-size:9px;font-weight:bold;margin-bottom:4px"><span>SELECCIÓN</span><span>MONTO${editable?'  ':''}</span></div>
    ${rows}
    <div class="receipt-total"><span>TOTAL:</span><span>Bs ${total.toFixed(2)}</span></div>
    <div class="receipt-footer"><p>*** GRACIAS POR SU PREFERENCIA ***</p><p>Revise su ticket antes de retirarse</p><p>Válido por 3 días</p></div>
  </div>`;
}

// ─── RENDER TICKET (live) ────────────────────────────────────
function renderAllTicketPanels(){
  const total=currentTicket.reduce((s,i)=>s+i.amount,0);
  const html=renderReceiptLayout(currentTicket,total,null,null,null,null,true,null);
  ['receipts-container','receipts-container-modal','receipts-container-multi'].forEach(id=>{
    const el=document.getElementById(id);if(el)el.innerHTML=html;
  });
  ['grand-total-live','grand-total-live-modal','grand-total-live-multi','mobile-cart-total','animal-mobile-cart-total','multi-mobile-cart-total'].forEach(id=>{
    const el=document.getElementById(id);if(el)el.textContent='Bs '+total.toFixed(2);
  });
  const hasItems=currentTicket.length>0;
  ['btn-print-main','btn-print-modal','btn-print-multi'].forEach(id=>{
    const b=document.getElementById(id);
    if(b){b.disabled=!hasItems;b.classList.toggle('opacity-50',!hasItems);b.classList.toggle('cursor-not-allowed',!hasItems);}
  });
}

function removeBet(i){currentTicket.splice(i,1);renderAllTicketPanels();}
function clearTicket(){
  if(currentTicket.length&&!confirm('¿Cancelar todas las apuestas?'))return;
  currentTicket=[];renderAllTicketPanels();
}

// ─── TODAY SALES ─────────────────────────────────────────────
function updateLiveSalesSummary(){
  const today=new Date().toLocaleDateString('es-VE');
  const total=allTransactions.filter(t=>t.dateOnly===today&&t.status!=='Anulado').reduce((s,t)=>s+t.total,0);
  const el=document.getElementById('pos-today-sales');if(el)el.textContent='Bs '+total.toFixed(2);
}

'''

with open(OUT, 'a', encoding='utf-8') as f:
    f.write(JS1)
print("JS1 written:", len(JS1), "bytes")

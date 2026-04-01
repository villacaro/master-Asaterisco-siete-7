#!/usr/bin/env python3
"""Runner: generates complete taquilla/index.html from all build parts."""
import subprocess, sys, os
OUT = r'c:\Users\villa\OneDrive\Documentos\appelarrejuntao\taquilla\index.html'

# Fix build_v2d.py closing tags if still wrong
with open(r'c:\Users\villa\OneDrive\Documentos\appelarrejuntao\taquilla\build_v2d.py','r',encoding='utf-8') as f:
    src=f.read()
if '</script>\n</body></html>' in src or '</script>\\n</body></html>' in src or ('</script>' in src and '</body></html>' in src):
    src=src.replace('}\n</script>\n</body></html>','}\n').replace("}</script>\n</body></html>",'}')
    with open(r'c:\Users\villa\OneDrive\Documentos\appelarrejuntao\taquilla\build_v2d.py','w',encoding='utf-8') as f:
        f.write(src)
    print("Fixed build_v2d.py closing tags.")
else:
    print("build_v2d.py is fine.")

# Run parts in order
for script in ['build_v2.py','build_v2b.py','build_v2c.py','build_v2d.py']:
    path=r'c:\Users\villa\OneDrive\Documentos\appelarrejuntao\taquilla\\'+script
    r=subprocess.run([sys.executable,path],capture_output=True,text=True,encoding='utf-8')
    if r.returncode!=0:
        print(f"ERROR in {script}:\n{r.stderr}")
        sys.exit(1)
    print(f"OK: {script} -> {r.stdout.strip()}")

# Append remaining JS + close
JS_FINAL = r'''
// ─── BET MODE ────────────────────────────────────────────────
const DARK_MODE_BTN='bg-slate-700 border-indigo-500 text-white';
const DARK_NORM_BTN='bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700';
function setMode(m){
  betMode=m; permuta=false;
  const nums={'normal':3,'terminal':2,'serie':2,'cuatro':4};
  const plc={'normal':'---','terminal':'--','serie':'--','cuatro':'----'};
  const inp=document.getElementById('betNumber');
  if(inp){inp.maxLength=nums[m]||3;inp.placeholder=plc[m]||'---';}
  ['normal','serie','terminal','cuatro'].forEach(x=>{
    const b=document.getElementById('btn-mode-'+x);
    if(b){b.classList.remove('bg-slate-700','border-indigo-500','text-white','hover:bg-slate-700');
      b.classList.add('bg-slate-800','border-slate-700','text-slate-300');}
  });
  const ab=document.getElementById('btn-mode-'+m);
  if(ab){ab.classList.remove('bg-slate-800','border-slate-700','text-slate-300');
    ab.classList.add('bg-slate-700','border-indigo-500','text-white');}
  // reset permuta button
  const pb=document.getElementById('btn-permuta');
  if(pb){pb.classList.remove('bg-slate-700','border-indigo-500','text-white');
    pb.classList.add('bg-slate-800','border-slate-700','text-slate-300');}
  const lbl=document.getElementById('label-bet-number');
  if(lbl)lbl.textContent=m==='serie'?'SERIE (2D)':m==='terminal'?'TERMINAL (2D)':m==='cuatro'?'4 CIFRAS':'NÚMERO';
}
function togglePermuta(){
  permuta=!permuta;
  const b=document.getElementById('btn-permuta');
  if(b){
    if(permuta){b.classList.remove('bg-slate-800','border-slate-700','text-slate-300');b.classList.add('bg-slate-700','border-indigo-500','text-white');}
    else{b.classList.remove('bg-slate-700','border-indigo-500','text-white');b.classList.add('bg-slate-800','border-slate-700','text-slate-300');}
  }
}

// ─── ADD BET ─────────────────────────────────────────────────
function isBetAllowed(closeTime){
  const now=new Date(),h=parseInt(closeTime.split(':')[0]),m=parseInt(closeTime.split(':')[1]);
  const close=new Date();close.setHours(h,m,0,0);
  return now<close;
}
function permutations(str){
  if(str.length<=1)return[str];
  const res=[];
  for(let i=0;i<str.length;i++){
    const rest=permutations(str.slice(0,i)+str.slice(i+1));
    rest.forEach(p=>res.push(str[i]+p));
  }
  return[...new Set(res)];
}
function addBet(btn){
  const num=document.getElementById('betNumber').value.trim();
  const amt=parseFloat(document.getElementById('betAmount').value);
  if(!num){showToast('Ingrese un número','error');return;}
  if(isNaN(amt)||amt<50){showToast('Monto mínimo 50 Bs','error');return;}
  if(!selectedLotteries.length){showToast('Seleccione al menos una lotería','error');return;}
  let numbers=[];
  if(betMode==='serie'){
    for(let i=0;i<=9;i++)numbers.push({val:i+num,label:i+num+' (S)'});
  } else if(permuta&&betMode==='normal'){
    permutations(num).forEach(p=>numbers.push({val:p,label:p+' (P)'}));
  } else {
    const lbl=betMode==='terminal'?num+' (T)':betMode==='cuatro'?num+' (4C)':num;
    numbers.push({val:num,label:lbl});
  }
  selectedLotteries.forEach(sl=>{
    numbers.forEach(n=>{
      const lotLabel=sl.name+' '+sl.type.charAt(0).toUpperCase()+' ['+sl.sub+']';
      currentTicket.push({type:'lottery',lottery:lotLabel,number:n.label,amount:amt});
    });
  });
  renderAllTicketPanels();updateLiveSalesSummary();
  document.getElementById('betNumber').value='';document.getElementById('betNumber').focus();
  showToast('Apuesta agregada ✓','success');
}

// ─── PRINT / PDF ─────────────────────────────────────────────
function openPrintPreview(){
  if(!currentTicket.length)return;
  const total=currentTicket.reduce((s,i)=>s+i.amount,0);
  const now=new Date();
  document.getElementById('final-ticket-preview').innerHTML=renderReceiptLayout(
    currentTicket,total,nextTicketId,genCode(),
    now.toLocaleDateString('es-VE'),now.toLocaleTimeString('es-VE',{hour12:true}),false,null);
  document.getElementById('preview-modal').classList.remove('hidden');
}
function closePreview(){document.getElementById('preview-modal').classList.add('hidden');}
function buildTransaction(){
  const now=new Date(),total=currentTicket.reduce((s,i)=>s+i.amount,0);
  return{id:nextTicketId,status:'Pendiente',total,items:[...currentTicket],
    validationCode:genCode(),dateOnly:now.toLocaleDateString('es-VE'),
    timeOnly:now.toLocaleTimeString('es-VE',{hour12:true}),timestamp:now.toISOString()};
}
function addToHistory(tx){
  allTransactions.unshift(tx);nextTicketId++;saveData();updateLiveSalesSummary();
}
function confirmAndPrint(){
  const tx=buildTransaction();closePreview();
  document.getElementById('printable-area').innerHTML=renderReceiptLayout(tx.items,tx.total,'#'+tx.id,tx.validationCode,tx.dateOnly,tx.timeOnly,false,null);
  window.print();addToHistory(tx);currentTicket=[];renderAllTicketPanels();
  showToast('Ticket #'+tx.id+' impreso ✓','success');
}
function confirmAndDownloadPDF(){
  const tx=buildTransaction();closePreview();
  const el=document.getElementById('final-ticket-preview');
  html2pdf().set({margin:.1,filename:'Ticket_*7_'+tx.id+'.pdf',
    image:{type:'jpeg',quality:.98},html2canvas:{scale:2,backgroundColor:'#ffffff'},
    jsPDF:{unit:'in',format:[3.15,8],orientation:'portrait'}}).from(el).save()
    .then(()=>{addToHistory(tx);currentTicket=[];renderAllTicketPanels();showToast('PDF descargado ✓','success');});
}

// ─── LOTTERY GRID ────────────────────────────────────────────
function renderLotteryGrid(){
  const cont=document.getElementById('lottery-grid-container');if(!cont)return;
  cont.innerHTML='';
  const timeIcons={morning:'☀',afternoon:'⛅',night:'🌙'};
  const timeLabel={morning:'MAÑANA',afternoon:'TARDE',night:'NOCHE'};
  const timeSelCls={morning:'bg-yellow-400 text-yellow-900 border-yellow-400 font-black',afternoon:'bg-blue-500 text-white border-blue-500 font-black',night:'bg-red-500 text-white border-red-500 font-black'};
  const timeGhost='border-slate-700 text-slate-400 hover:border-slate-500 hover:text-slate-300';
  const subSelCls={morning:'bg-yellow-400 text-yellow-900 border-yellow-400',afternoon:'bg-blue-500 text-white border-blue-500',night:'bg-red-600 text-white border-red-500'};
  const subGhost='bg-slate-800 border-slate-700 text-slate-400 hover:bg-slate-700 hover:text-slate-200';
  lotteryConfig.forEach(lot=>{
    const isSpecial=lot.name.includes('GANA')||lot.name.includes('TRIPLE');
    const subs=isSpecial?['A','S']:['A','B','C'];
    const types=['morning','afternoon','night'];
    const allSel=types.every(t=>subs.every(s=>selectedLotteries.some(sl=>sl.name===lot.name&&sl.type===t&&sl.sub===s)));
    const card=document.createElement('div');
    card.className='bg-slate-800 rounded-xl p-3.5 border border-slate-700 hover:border-slate-600 transition-all';
    let timesHtml=types.map(type=>{
      const hasSel=selectedLotteries.some(sl=>sl.name===lot.name&&sl.type===type);
      const timeAllowed=isBetAllowed(lotteryDrawTimes[type]);
      const subBtns=subs.map(sub=>{
        const isSel=selectedLotteries.some(sl=>sl.name===lot.name&&sl.type===type&&sl.sub===sub);
        return `<button class="mod-btn px-2.5 py-0.5 text-[9px] rounded border ${isSel?subSelCls[type]:subGhost} ${!timeAllowed?'opacity-25 cursor-not-allowed':''}" ${!timeAllowed?'disabled':''} onclick="toggleLotteryBtn('${lot.name}','${type}','${sub}')">${sub}</button>`;
      }).join('');
      const timeCls=hasSel?timeSelCls[type]:timeGhost;
      return `<div class="flex items-center gap-1.5 ${!timeAllowed?'opacity-30':''}">
        <button class="flex items-center gap-1 text-[8px] px-2 py-0.5 rounded border font-bold ${timeCls} ${!timeAllowed?'cursor-not-allowed':''}" ${!timeAllowed?'disabled':''} onclick="toggleAllLotteryTime('${lot.name}','${type}')">${timeIcons[type]} ${timeLabel[type]}</button>
        <button onclick="toggleAllLotteryTime('${lot.name}','${type}')" class="text-[7px] font-bold border border-slate-700 text-slate-500 hover:text-slate-300 px-1.5 py-0.5 rounded ${!timeAllowed?'cursor-not-allowed':''}">TODO</button>
        <div class="flex gap-0.5">${subBtns}</div>
      </div>`;
    }).join('');
    card.innerHTML=`<div class="flex items-center justify-between mb-2.5">
      <h4 class="font-bold text-sm text-white">${lot.name}</h4>
      <button onclick="toggleAllLottery('${lot.name}')" class="text-[8px] px-2.5 py-0.5 rounded-full font-bold border transition-all ${allSel?'bg-indigo-600 text-white border-indigo-600':'border-slate-600 text-slate-400 hover:border-indigo-500 hover:text-indigo-400'}">Todos</button>
    </div><div class="flex flex-col gap-2">${timesHtml}</div>`;
    cont.appendChild(card);
  });
}
function toggleLotteryBtn(name,type,sub){
  const idx=selectedLotteries.findIndex(sl=>sl.name===name&&sl.type===type&&sl.sub===sub);
  if(idx>-1)selectedLotteries.splice(idx,1);
  else if(isBetAllowed(lotteryDrawTimes[type]))selectedLotteries.push({name,type,sub});
  else showToast('Horario cerrado','warn');
  renderLotteryGrid();
}
function toggleAllLotteryTime(name,type){
  if(!isBetAllowed(lotteryDrawTimes[type])){showToast('Horario cerrado','warn');return;}
  const isSpecial=name.includes('GANA')||name.includes('TRIPLE');
  const subs=isSpecial?['A','S']:['A','B','C'];
  const allSel=subs.every(s=>selectedLotteries.some(sl=>sl.name===name&&sl.type===type&&sl.sub===s));
  if(allSel)selectedLotteries=selectedLotteries.filter(sl=>!(sl.name===name&&sl.type===type));
  else subs.forEach(sub=>{if(!selectedLotteries.some(sl=>sl.name===name&&sl.type===type&&sl.sub===sub))selectedLotteries.push({name,type,sub});});
  renderLotteryGrid();
}
function toggleAllLottery(name){
  const isSpecial=name.includes('GANA')||name.includes('TRIPLE');
  const subs=isSpecial?['A','S']:['A','B','C'];
  const types=['morning','afternoon','night'];
  const allSel=types.every(t=>subs.every(s=>selectedLotteries.some(sl=>sl.name===name&&sl.type===t&&sl.sub===s)));
  if(allSel){selectedLotteries=selectedLotteries.filter(sl=>sl.name!==name);}
  else{types.forEach(type=>{if(!isBetAllowed(lotteryDrawTimes[type]))return;subs.forEach(sub=>{if(!selectedLotteries.some(sl=>sl.name===name&&sl.type===type&&sl.sub===sub))selectedLotteries.push({name,type,sub});});}); }
  renderLotteryGrid();
}

// ─── ZODIACS ─────────────────────────────────────────────────
const zodiacColors=['bg-red-800','bg-orange-700','bg-yellow-700','bg-green-800','bg-teal-800','bg-blue-900','bg-indigo-900','bg-purple-900','bg-pink-900','bg-rose-800','bg-cyan-800','bg-emerald-800'];
function renderZodiacs(){
  const cont=document.getElementById('zodiac-scroll');if(!cont)return;
  cont.innerHTML=`<button onclick="clearZodiacs()" class="shrink-0 px-3 py-1.5 rounded-full text-[9px] font-bold border transition-all ${!selectedMainZodiacs.length?'bg-slate-700 text-white border-slate-600':'border-slate-700 text-slate-400 hover:bg-slate-800 hover:text-white'}">TODOS</button>`+
    zodiacs.map((z,i)=>{const sel=selectedMainZodiacs.includes(z.code);const bg=zodiacColors[i%zodiacColors.length];return`<button onclick="toggleZodiac('${z.code}')" class="shrink-0 flex items-center gap-1 px-3 py-1.5 rounded-full text-[9px] font-bold border transition-all ${sel?bg+' text-white border-transparent':'border-slate-700 text-slate-400 hover:border-slate-600 hover:text-slate-300'}">${z.icon} ${z.name}</button>`;}).join('');
}
function toggleZodiac(code){const i=selectedMainZodiacs.indexOf(code);if(i>-1)selectedMainZodiacs.splice(i,1);else selectedMainZodiacs.push(code);renderZodiacs();}
function clearZodiacs(){selectedMainZodiacs=[];renderZodiacs();}

// ─── ANIMALITOS ───────────────────────────────────────────────
function toggleAnimalitos(){
  const m=document.getElementById('animalitos-modal');
  m.classList.toggle('hidden');
  if(!m.classList.contains('hidden'))updateAnimalitosView();
}
function updateAnimalitosView(){renderAnimalLotteryButtons();renderAnimalTimes();renderAnimalGrid();}
function renderAnimalLotteryButtons(){
  const c=document.getElementById('animal-lottery-buttons');if(!c)return;
  c.innerHTML=animalLotteriesList.map(l=>{const col=animalColors[l]||animalColors['Lotto Activo'];const sel=selectedAnimalLotteries.includes(l);return`<button onclick="toggleAnimalLottery('${l}')" class="px-2 py-1 rounded text-xs font-bold border transition-all ${sel?col.main:col.ghost}">${l}</button>`;}).join('');
}
function toggleAnimalLottery(l){const i=selectedAnimalLotteries.indexOf(l);if(i>-1)selectedAnimalLotteries.splice(i,1);else selectedAnimalLotteries.push(l);updateAnimalitosView();}
function getAnimalListForLot(lot){return lot==='Animalitos Arrejuntao'||animalBetMode==='arrejuntao'?animalsArrejuntao:lot==='Guacharo Activo'?animalsGuacharo:animalsStandard;}
function getTimesForLot(lot){return lot==='Animalitos Arrejuntao'?timesArrejuntao:timesStandard;}
function renderAnimalTimes(){
  const c=document.getElementById('animal-times-container');if(!c)return;c.innerHTML='';
  selectedAnimalLotteries.forEach(lot=>{
    const times=getTimesForLot(lot);const col=animalColors[lot]||animalColors['Lotto Activo'];
    const row=document.createElement('div');row.className='flex items-center gap-1 flex-wrap';
    row.innerHTML=`<span class="text-[8px] font-bold uppercase bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400 px-2 py-0.5 rounded w-20 truncate">${lot.split(' ')[0]}</span>`+
      times.map(t=>{const sel=selectedAnimalTimes.some(at=>at.lot===lot&&at.time===t);return`<button onclick="toggleAnimalTime('${lot}','${t}')" class="px-2 py-0.5 rounded-full text-[9px] font-bold border transition-all ${sel?col.main:'border-slate-300 dark:border-slate-600 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'}">${t}</button>`;}).join('')+
      `<button onclick="toggleAllAnimalTimes('${lot}')" class="px-2 py-0.5 rounded text-[9px] border border-slate-300 dark:border-slate-600 text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800">TODO</button>`;
    c.appendChild(row);
  });
}
function toggleAnimalTime(lot,time){const i=selectedAnimalTimes.findIndex(at=>at.lot===lot&&at.time===time);if(i>-1)selectedAnimalTimes.splice(i,1);else selectedAnimalTimes.push({lot,time});renderAnimalTimes();}
function toggleAllAnimalTimes(lot){const times=getTimesForLot(lot);const allSel=times.every(t=>selectedAnimalTimes.some(at=>at.lot===lot&&at.time===t));if(allSel)selectedAnimalTimes=selectedAnimalTimes.filter(at=>at.lot!==lot);else times.forEach(t=>{if(!selectedAnimalTimes.some(at=>at.lot===lot&&at.time===t))selectedAnimalTimes.push({lot,time:t});});renderAnimalTimes();}
function renderAnimalGrid(){
  const grid=document.getElementById('animal-grid');if(!grid)return;
  const lot=selectedAnimalLotteries[0]||'Lotto Activo';
  const list=getAnimalListForLot(lot);
  const tb=document.getElementById('btn-toggle-all');if(tb)tb.textContent=`Todos (${list.length})`;
  grid.innerHTML=list.map(a=>`<div onclick="toggleAnimal('${a.n}')" class="animal-btn ${selectedAnimals.includes(a.n)?'selected':''}"><div class="animal-number">${a.n}</div><div class="animal-name">${a.name}</div></div>`).join('');
}
function toggleAnimal(n){const i=selectedAnimals.indexOf(n);if(i>-1)selectedAnimals.splice(i,1);else selectedAnimals.push(n);renderAnimalGrid();}
function toggleAllAnimals(){const lot=selectedAnimalLotteries[0]||'Lotto Activo';const list=getAnimalListForLot(lot);selectedAnimals=selectedAnimals.length===list.length?[]:list.map(a=>a.n);renderAnimalGrid();}
function setAnimalMode(mode){
  animalBetMode=mode;
  ['normal','arrejuntao'].forEach(m=>{const b=document.getElementById('btn-animal-'+m);if(b){b.className=b.className.replace(m===mode?'text-slate-500 dark:text-slate-400':'bg-emerald-600 text-white',m===mode?'bg-emerald-600 text-white':'text-slate-500 dark:text-slate-400');}});
  renderAnimalGrid();
}
function addAnimalBets(btn){
  const amt=parseFloat(document.getElementById('animal-bet-amount').value);
  if(!selectedAnimals.length){showToast('Seleccione animales','error');return;}
  if(!selectedAnimalLotteries.length){showToast('Seleccione loterías','error');return;}
  if(!selectedAnimalTimes.length){showToast('Seleccione horarios','error');return;}
  if(isNaN(amt)||amt<50){showToast('Monto mínimo 50 Bs','error');return;}
  const lot=selectedAnimalLotteries[0]||'Lotto Activo';const list=getAnimalListForLot(lot);
  selectedAnimals.forEach(an=>{
    const a=list.find(x=>x.n===an);if(!a)return;
    selectedAnimalLotteries.forEach(l=>{
      selectedAnimalTimes.filter(at=>at.lot===l).forEach(at=>{
        currentTicket.push({type:'animal',lottery:l+' '+at.time,number:an+' '+a.name,amount:amt});
      });
    });
  });
  renderAllTicketPanels();showToast('Apuestas agregadas ✓','success');selectedAnimals=[];renderAnimalGrid();
}

// ─── MULTI-PRODUCT (Arrejuntao) ───────────────────────────────
function openMultiProductModal(){document.getElementById('multi-product-modal').classList.remove('hidden');renderMultiTimes();renderMultiCategories();renderMultiAdditional();}
function closeMultiProductModal(){document.getElementById('multi-product-modal').classList.add('hidden');}
function renderMultiTimes(){const c=document.getElementById('multi-times-container');if(!c)return;c.innerHTML=multiTimesOptions.map(t=>{const sel=multiSelectedTimes.includes(t);return`<button onclick="toggleMultiTime('${t}')" class="px-4 py-2 rounded-xl text-sm font-bold border transition-all ${sel?'bg-orange-600 text-white border-orange-500 shadow-lg':'bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-600 text-slate-600 dark:text-slate-300 hover:border-orange-400'}">${t}</button>`;}).join('');}
function toggleMultiTime(t){const i=multiSelectedTimes.indexOf(t);if(i>-1)multiSelectedTimes.splice(i,1);else multiSelectedTimes.push(t);renderMultiTimes();}
function renderMultiCategories(){const c=document.getElementById('multi-categories-container');if(!c)return;c.innerHTML=`<button onclick="toggleAllMultiCats()" class="px-4 py-2 rounded-xl text-xs font-bold border transition-all bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-600 text-slate-600 dark:text-slate-300 hover:border-orange-400">✓ TODOS</button>`+multiCategories.map(cat=>{const sel=multiSelectedCategories.includes(cat.id);return`<button onclick="toggleMultiCategory('${cat.id}')" class="px-4 py-2 rounded-xl text-xs font-bold border transition-all ${sel?cat.color+' text-white shadow-lg':'bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-600 text-slate-600 dark:text-slate-300 hover:border-orange-400'}">${cat.label}</button>`;}).join('');}
function toggleAllMultiCats(){const allIds=multiCategories.map(c=>c.id);const allSel=allIds.every(id=>multiSelectedCategories.includes(id));multiSelectedCategories=allSel?[]:[...allIds];renderMultiCategories();}
function toggleMultiCategory(id){const i=multiSelectedCategories.indexOf(id);if(i>-1)multiSelectedCategories.splice(i,1);else multiSelectedCategories.push(id);renderMultiCategories();}
function renderMultiAdditional(){const c=document.getElementById('multi-additional-container');if(!c)return;c.innerHTML=`<button onclick="toggleAllMultiAdd()" class="px-3 py-2 rounded-xl text-xs font-bold border bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-600 text-slate-600 dark:text-slate-300 hover:border-orange-400">✓ TODOS</button>`+multiAdditional.map(cat=>{const sel=multiSelectedAdditional.includes(cat.id);return`<button onclick="toggleMultiAdd('${cat.id}')" class="px-3 py-2 rounded-xl text-xs font-bold border transition-all ${sel?cat.color+' text-white shadow-lg':'bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-600 text-slate-600 dark:text-slate-300 hover:border-orange-400'}">${cat.label}</button>`;}).join('');}
function toggleAllMultiAdd(){const allIds=multiAdditional.map(c=>c.id);const allSel=allIds.every(id=>multiSelectedAdditional.includes(id));multiSelectedAdditional=allSel?[]:[...allIds];renderMultiAdditional();}
function toggleMultiAdd(id){const i=multiSelectedAdditional.indexOf(id);if(i>-1)multiSelectedAdditional.splice(i,1);else multiSelectedAdditional.push(id);renderMultiAdditional();}
function addMultiBet(){
  const num=document.getElementById('multi-bet-number').value;
  const amt=parseFloat(document.getElementById('multi-bet-amount').value);
  if(!num||num.length!==3){showToast('Ingrese 3 dígitos','error');return;}
  if(isNaN(amt)||amt<50){showToast('Monto mínimo 50 Bs','error');return;}
  if(!multiSelectedTimes.length){showToast('Seleccione horarios','error');return;}
  const cats=[...multiSelectedCategories,...multiSelectedAdditional];
  if(!cats.length){showToast('Seleccione categorías','error');return;}
  multiSelectedTimes.forEach(time=>{cats.forEach(cat=>{
    const info=[...multiCategories,...multiAdditional].find(c=>c.id===cat);
    currentTicket.push({type:'lottery',lottery:'*7 '+time,number:num+' ('+( info?info.label:cat)+')',amount:amt});
  });});
  renderAllTicketPanels();showToast('Apuestas agregadas ✓','success');
  document.getElementById('multi-bet-number').value='';document.getElementById('multi-bet-number').focus();
}

// ─── MANAGEMENT ───────────────────────────────────────────────
function renderManagementTable(filter){
  filter=filter||currentStatusFilter;currentStatusFilter=filter;
  const tbody=document.getElementById('mgmt-table-body');if(!tbody)return;
  const search=document.getElementById('mgmt-search');const q=search?search.value.trim().toLowerCase():'';
  let rows=allTransactions;
  if(filter!=='all')rows=rows.filter(t=>t.status===filter);
  if(q)rows=rows.filter(t=>String(t.id).includes(q));
  if(!rows.length){tbody.innerHTML='<tr><td colspan="5" class="p-8 text-center text-slate-400 italic">No hay tickets.</td></tr>';return;}
  const sc={Pendiente:'text-yellow-500',Ganador:'text-emerald-500',Pagado:'text-blue-500',Anulado:'text-red-500'};
  tbody.innerHTML=rows.map(t=>`<tr class="border-b border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/30 cursor-pointer" onclick="openActionModal(${t.id})">
    <td class="p-3 font-mono font-bold text-slate-800 dark:text-white">#${t.id}</td>
    <td class="p-3 text-xs text-slate-500 dark:text-slate-400">${t.dateOnly} ${t.timeOnly}</td>
    <td class="p-3 text-right font-bold text-emerald-600 dark:text-emerald-400">Bs ${t.total.toFixed(2)}</td>
    <td class="p-3 text-center"><span class="${sc[t.status]||'text-slate-400'} text-xs font-bold uppercase">${t.status}</span></td>
    <td class="p-3 text-center"><button class="p-1.5 hover:bg-slate-200 dark:hover:bg-slate-600 rounded text-slate-500 dark:text-slate-400">👁</button></td>
  </tr>`).join('');
}
function filterStatus(s){renderManagementTable(s);}
function filterTickets(){renderManagementTable(currentStatusFilter);}
function simulateWinners(){
  const pend=allTransactions.filter(t=>t.status==='Pendiente');
  if(!pend.length){showToast('No hay pendientes','warn');return;}
  const t=pend[Math.floor(Math.random()*pend.length)];t.status='Ganador';t.prizeValue=t.total*75;
  saveData();renderManagementTable();showToast('Ticket #'+t.id+' GANADOR! Bs '+t.prizeValue.toFixed(2),'success');
}
function openActionModal(id){
  const t=allTransactions.find(x=>x.id===id);if(!t)return;selectedTxId=id;
  document.getElementById('action-ticket-preview').innerHTML=renderReceiptLayout(t.items,t.total,'#'+t.id,t.validationCode,t.dateOnly,t.timeOnly,false,t.status);
  const btns=document.getElementById('action-buttons');let extra='';
  if(t.status==='Pendiente')extra+=`<button onclick="openVoidModal()" class="px-3 py-2 bg-red-600 text-white rounded font-bold text-xs">Anular</button>`;
  if(t.status==='Ganador')extra+=`<button onclick="payTicket()" class="px-4 py-2 bg-emerald-600 text-white rounded font-bold text-xs">Pagar Bs ${(t.prizeValue||t.total*75).toFixed(2)}</button>`;
  btns.innerHTML=`<button onclick="reprintTicket(${id})" class="px-3 py-2 bg-slate-700 text-white rounded font-bold text-xs">Reimprimir</button>${extra}<button onclick="closeActionModal()" class="px-3 py-2 border border-slate-300 dark:border-slate-600 rounded font-bold text-xs">Cerrar</button>`;
  document.getElementById('action-modal').classList.remove('hidden');
}
function closeActionModal(){document.getElementById('action-modal').classList.add('hidden');selectedTxId=null;}
function openVoidModal(){document.getElementById('void-confirm-modal').classList.remove('hidden');}
function closeVoidModal(){document.getElementById('void-confirm-modal').classList.add('hidden');}
function processVoid(){
  const reason=document.getElementById('void-reason').value;
  const t=allTransactions.find(x=>x.id===selectedTxId);
  if(t){t.status='Anulado';t.voidReason=reason;saveData();renderManagementTable();updateLiveSalesSummary();}
  closeVoidModal();closeActionModal();showToast('Ticket anulado','success');
  document.getElementById('void-reason').value='';
}
function payTicket(){
  const t=allTransactions.find(x=>x.id===selectedTxId);
  if(t){t.status='Pagado';t.prizeValue=t.prizeValue||t.total*75;saveData();renderManagementTable();}
  closeActionModal();showToast('Premio pagado ✓','success');
}
function reprintTicket(id){
  const t=allTransactions.find(x=>x.id===id);if(!t)return;
  document.getElementById('printable-area').innerHTML=renderReceiptLayout(t.items,t.total,'#'+t.id,t.validationCode,t.dateOnly,t.timeOnly,false,t.status);
  window.print();showToast('Reimpresión #'+t.id,'info');
}

// ─── REPORTS ─────────────────────────────────────────────────
function switchReportTab(tab){
  currentReportTab=tab;
  ['cierre','transacciones','ganadores'].forEach(t=>{
    const c=document.getElementById('report-content-'+t);
    const b=document.getElementById('rtab-'+t);
    if(c)c.classList.toggle('hidden',t!==tab);
    if(b){b.className=b.className.replace(t===tab?'text-slate-500 dark:text-slate-400':'bg-purple-600 text-white',t===tab?'bg-purple-600 text-white':'text-slate-500 dark:text-slate-400');}
  });
  if(tab==='cierre')renderCierreDeCaja();
  if(tab==='transacciones')renderHistoryTable();
  if(tab==='ganadores')renderWinnersReport();
}
function renderCierreDeCaja(){
  let sales=0,payouts=0,sCnt=0,pCnt=0;
  allTransactions.forEach(t=>{if(t.status!=='Anulado'){sales+=t.total;sCnt++;}if(t.status==='Pagado'){payouts+=(t.prizeValue||0);pCnt++;}});
  document.getElementById('cierre-sales').textContent='Bs '+sales.toFixed(2);
  document.getElementById('cierre-sales-count').textContent=sCnt+' tickets';
  document.getElementById('cierre-payouts').textContent='Bs '+payouts.toFixed(2);
  document.getElementById('cierre-payouts-count').textContent=pCnt+' pagados';
  document.getElementById('cierre-balance').textContent='Bs '+(sales-payouts).toFixed(2);
}
function renderHistoryTable(){
  const tbody=document.getElementById('history-table-body');if(!tbody)return;
  const sc={Pendiente:'text-yellow-500',Ganador:'text-emerald-500',Pagado:'text-blue-500',Anulado:'text-red-500'};
  tbody.innerHTML=allTransactions.map(t=>`<tr class="border-b border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/30">
    <td class="p-3 text-xs text-slate-500 dark:text-slate-400">${t.dateOnly} ${t.timeOnly}</td>
    <td class="p-3 font-mono font-bold text-slate-800 dark:text-white">#${t.id}</td>
    <td class="p-3 text-right font-bold text-emerald-600 dark:text-emerald-400">Bs ${t.total.toFixed(2)}</td>
    <td class="p-3 text-center"><span class="${sc[t.status]||''} text-xs font-bold">${t.status}</span></td></tr>`).join('');
}
function renderWinnersReport(){
  const tbody=document.getElementById('winners-report-body');if(!tbody)return;
  const w=allTransactions.filter(t=>t.status==='Ganador'||t.status==='Pagado');
  tbody.innerHTML=w.map(t=>`<tr class="border-b border-slate-200 dark:border-slate-700">
    <td class="p-3 font-mono font-bold text-slate-900 dark:text-white">#${t.id}</td>
    <td class="p-3 text-right font-bold">Bs ${t.total.toFixed(2)}</td>
    <td class="p-3 text-right font-bold text-emerald-600">Bs ${(t.prizeValue||t.total*75).toFixed(2)}</td>
    <td class="p-3 text-center"><span class="${t.status==='Pagado'?'text-blue-500':'text-emerald-500'} text-xs font-bold">${t.status}</span></td></tr>`).join('');
}
function realizarCierreZ(){showConfirm('Cierre Z','¿Generar e imprimir Reporte Z?',()=>{renderCierreDeCaja();window.print();showToast('Reporte Z generado','info');});}
function exportTransaccionesCSV(){
  if(!allTransactions.length){showToast('Sin transacciones','warn');return;}
  const csv='Ticket,Fecha,Hora,Total,Estado\n'+allTransactions.map(t=>`${t.id},${t.dateOnly},${t.timeOnly},${t.total.toFixed(2)},${t.status}`).join('\n');
  const url=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));
  const a=document.createElement('a');a.href=url;a.download='transacciones_ast7.csv';a.click();URL.revokeObjectURL(url);
  showToast('CSV exportado ✓','success');
}

// ─── CONFIG ───────────────────────────────────────────────────
function loadSystemConfig(){
  const n=document.getElementById('cfg-agency-name');if(n)n.value=sysConfig.agencyName;
  const r=document.getElementById('cfg-agency-rif');if(r)r.value=sysConfig.agencyRif;
  const et=document.getElementById('cfg-enable-topes');if(et)et.checked=sysConfig.enableTopes;
  const mb=document.getElementById('cfg-max-bet');if(mb)mb.value=sysConfig.maxBet;
  const p=document.getElementById('cfg-pin');if(p)p.value=sysConfig.securityPin;
}
function saveSystemConfig(){
  const n=document.getElementById('cfg-agency-name');if(n)sysConfig.agencyName=n.value;
  const r=document.getElementById('cfg-agency-rif');if(r)sysConfig.agencyRif=r.value;
  const et=document.getElementById('cfg-enable-topes');if(et)sysConfig.enableTopes=et.checked;
  const mb=document.getElementById('cfg-max-bet');if(mb)sysConfig.maxBet=parseFloat(mb.value)||2000;
  const p=document.getElementById('cfg-pin');if(p)sysConfig.securityPin=p.value||'1234';
  saveData();showToast('Configuración guardada ✓','success');
}

// ─── LOGIN ────────────────────────────────────────────────────
function checkLogin(){const lm=document.getElementById('login-modal');if(sessionStorage.getItem('ast7_logged')==='true'){lm.classList.add('hidden');}else{lm.classList.remove('hidden');setTimeout(()=>{const pi=document.getElementById('login-pin-input');if(pi)pi.focus();},100);}}
function attemptLogin(){
  const pin=document.getElementById('login-pin-input').value;
  if(pin===sysConfig.securityPin){sessionStorage.setItem('ast7_logged','true');document.getElementById('login-modal').classList.add('hidden');showToast('Bienvenido a Asterisco Siete (*7)','success');}
  else{showToast('PIN incorrecto','error');document.getElementById('login-pin-input').value='';document.getElementById('login-pin-input').focus();}
}

// ─── KEYBOARD ─────────────────────────────────────────────────
document.addEventListener('keydown',function(e){
  if(e.key==='F10'){e.preventDefault();openPrintPreview();}
  if(e.key==='F2'){e.preventDefault();clearTicket();}
  if(e.key==='Escape'){closePreview();closeActionModal();}
});
document.getElementById('login-pin-input').addEventListener('keydown',e=>{if(e.key==='Enter')attemptLogin();});

// ─── DEMO DATA ────────────────────────────────────────────────
function seedDemoData(){
  const today=new Date().toLocaleDateString('es-VE');
  const demoTx=[
    {id:1001,status:'Pendiente',total:200,items:[
      {type:'lottery',lottery:'SUPERGANA M [A]',number:'1478',amount:50},
      {type:'lottery',lottery:'SUPERGANA M [S]',number:'1478',amount:50},
      {type:'lottery',lottery:'TRIPLE GANA M [A]',number:'1478',amount:50},
      {type:'lottery',lottery:'TRIPLE GANA M [S]',number:'1478',amount:50}
    ],validationCode:genCode(),dateOnly:today,timeOnly:'8:30:00 a. m.',timestamp:new Date().toISOString()},
    {id:1002,status:'Pendiente',total:150,items:[
      {type:'lottery',lottery:'Táchira M [A]',number:'45',amount:50},
      {type:'lottery',lottery:'Táchira M [B]',number:'45',amount:50},
      {type:'lottery',lottery:'Táchira T [A]',number:'45',amount:50}
    ],validationCode:genCode(),dateOnly:today,timeOnly:'8:35:00 a. m.',timestamp:new Date().toISOString()},
    {id:1003,status:'Ganador',total:100,prizeValue:7500,items:[
      {type:'lottery',lottery:'Zulia N [A]',number:'23',amount:50},
      {type:'lottery',lottery:'Caliente N [B]',number:'23',amount:50}
    ],validationCode:genCode(),dateOnly:today,timeOnly:'8:40:00 a. m.',timestamp:new Date().toISOString()},
    {id:1004,status:'Pagado',total:150,prizeValue:11250,items:[
      {type:'lottery',lottery:'Caracas T [A]',number:'07',amount:75},
      {type:'lottery',lottery:'Chance T [A]',number:'07',amount:75}
    ],validationCode:genCode(),dateOnly:today,timeOnly:'8:45:00 a. m.',timestamp:new Date().toISOString()},
    {id:1005,status:'Anulado',total:50,voidReason:'Apuesta incorrecta',items:[
      {type:'animal',lottery:'Lotto Activo 9AM',number:'5 León',amount:50}
    ],validationCode:genCode(),dateOnly:today,timeOnly:'8:50:00 a. m.',timestamp:new Date().toISOString()},
    {id:1006,status:'Pendiente',total:250,items:[
      {type:'animal',lottery:'La Granjita 12PM',number:'12 Caballo',amount:50},
      {type:'animal',lottery:'La Granjita 12PM',number:'7 Perico',amount:50},
      {type:'lottery',lottery:'Zamorano M [A]',number:'888',amount:100},
      {type:'lottery',lottery:'Zamorano M [B]',number:'888',amount:50}
    ],validationCode:genCode(),dateOnly:today,timeOnly:'9:00:00 a. m.',timestamp:new Date().toISOString()}
  ];
  allTransactions=demoTx;
  nextTicketId=1007;
  saveData();
}

// ─── INIT ─────────────────────────────────────────────────────
function init(){
  checkLogin();
  changeView('pos');
  renderLotteryGrid();
  renderZodiacs();
  // Seed demo data on first load
  if(!allTransactions.length){seedDemoData();}
  updateLiveSalesSummary();
}
init();
</script>
</body></html>'''

with open(OUT,'a',encoding='utf-8') as f:
    f.write(JS_FINAL)

size=os.path.getsize(OUT)
print(f"\n✓ COMPLETE! index.html = {size:,} bytes ({size//1024} KB)")

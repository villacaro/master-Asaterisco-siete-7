import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale,
  LinearScale, BarElement
} from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

// ─── Constants ────────────────────────────────────────────────────────────────
const APP_USER = 'admin';
const APP_PASS = '1234';
const BATCH_SIZE = 100;

// ─── Helpers ──────────────────────────────────────────────────────────────────
function parseVCF(text) {
  const contacts = [];
  const seen = new Set();
  text.split('BEGIN:VCARD').filter(b => b.trim()).forEach(block => {
    const lines = block.split('\n');
    let c = { name: 'Desconocido', phone: 'N/A', email: 'N/A', location: 'N/A', status: 'Pendiente' };
    lines.forEach(raw => {
      const line = raw.replace(/=\r?\n\s*/g, '').trim();
      if (!line || line.startsWith('END:') || line.startsWith('VERSION:')) return;
      const m = line.match(/^([^:]+):(.*)$/);
      if (!m) return;
      const [, prop, val] = m;
      const p = prop.toUpperCase();
      if (p.startsWith('FN')) { c.name = val.trim(); }
      else if (p.startsWith('N;') || p === 'N') {
        const parts = val.split(';');
        c.name = parts.length >= 2 ? `${parts[1].trim()} ${parts[0].trim()}`.trim() : val.trim();
      }
      if (p.startsWith('TEL') && c.phone === 'N/A') {
        let ph = val.trim().replace(/\D/g, '');
        if (ph.startsWith('58')) ph = ph.slice(2);
        if (ph.length === 10 && !ph.startsWith('0')) ph = '0' + ph;
        c.phone = ph || 'N/A';
      }
      if (p.startsWith('EMAIL') && c.email === 'N/A') c.email = val.trim();
      if (p.startsWith('GEO')) c.location = val.trim();
    });
    if (c.name && c.name !== 'Desconocido') {
      const key = c.phone !== 'N/A' ? c.phone : c.name;
      if (!seen.has(key)) { seen.add(key); contacts.push(c); }
    }
  });
  return contacts;
}

// ─── Toast ────────────────────────────────────────────────────────────────────
function Toast({ msg, color, onDone }) {
  useEffect(() => { const t = setTimeout(onDone, 3000); return () => clearTimeout(t); }, []);
  return (
    <div className={`fixed top-6 left-1/2 -translate-x-1/2 z-[200] px-6 py-3 rounded-lg shadow-xl text-white font-medium text-sm ${color} animate-in`}>
      {msg}
    </div>
  );
}

// ─── Login ────────────────────────────────────────────────────────────────────
function LoginScreen({ onLogin }) {
  const [u, setU] = useState('');
  const [p, setP] = useState('');
  const [err, setErr] = useState(false);

  const submit = (e) => {
    e.preventDefault();
    if (u.trim() === APP_USER && p.trim() === APP_PASS) { onLogin(); }
    else { setErr(true); setTimeout(() => setErr(false), 2000); }
  };

  return (
    <div className="fixed inset-0 z-[100] bg-slate-900 flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-md p-8 rounded-2xl shadow-2xl border border-slate-700/50 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-indigo-500 to-purple-600" />
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-indigo-600 rounded-xl flex items-center justify-center text-white shadow-lg mx-auto mb-4">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
          </div>
          <h2 className="text-2xl font-bold text-slate-800">Bienvenido</h2>
          <p className="text-slate-500 text-sm mt-2">Inicia sesión para acceder al CRM</p>
        </div>
        <form onSubmit={submit} className="space-y-5">
          <div>
            <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Usuario</label>
            <input value={u} onChange={e => setU(e.target.value)} type="text" placeholder="admin"
              className="block w-full rounded-lg border border-slate-300 bg-slate-50 py-3 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"/>
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Contraseña</label>
            <input value={p} onChange={e => setP(e.target.value)} type="password" placeholder="••••"
              className="block w-full rounded-lg border border-slate-300 bg-slate-50 py-3 px-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"/>
          </div>
          {err && <p className="text-red-500 text-xs text-center bg-red-50 p-2 rounded-lg font-medium">Credenciales incorrectas.</p>}
          <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-xl shadow-lg transition-all hover:-translate-y-0.5">
            Ingresar al Sistema
          </button>
        </form>
        <p className="text-[10px] text-slate-400 text-center mt-6">Demo: <strong>admin</strong> / <strong>1234</strong></p>
      </div>
    </div>
  );
}

// ─── Sidebar ──────────────────────────────────────────────────────────────────
const NAV_ITEMS = [
  { id: 'dashboard',   label: 'Resumen',       group: 'Menu',    icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg> },
  { id: 'management',  label: 'Contactos',     group: 'Menu',    icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg> },
  { id: 'analytics',   label: 'Analíticas',    group: 'Menu',    icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg> },
  { id: 'broadcast',   label: 'Lotes y Envíos',group: 'Menu',    icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"/></svg> },
  { id: 'calendar',    label: 'Calendario',    group: 'Menu',    icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg> },
  { id: 'team',        label: 'Equipo',        group: 'Menu',    icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg> },
  { id: 'config',      label: 'Configuración', group: 'Sistema', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg> },
  { id: 'trash',       label: 'Papelera',      group: 'Sistema', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg> },
];

function Sidebar({ active, onNav, onLogout, collapsed, onToggleMobile }) {
  const groups = ['Menu', 'Sistema'];
  return (
    <nav className={`fixed top-0 left-0 h-full w-64 bg-slate-900 text-slate-300 flex flex-col z-50 shadow-2xl transition-transform duration-300 ${collapsed ? '-translate-x-full' : 'translate-x-0'} md:translate-x-0`}>
      {/* Header */}
      <div className="h-16 flex items-center px-6 border-b border-slate-800 shrink-0">
        <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white shadow-lg shadow-indigo-500/30 mr-3">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
        </div>
        <h2 className="text-base font-bold tracking-wide text-white">CRM Admin</h2>
        <button onClick={onToggleMobile} className="md:hidden ml-auto text-slate-400 hover:text-white">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      {/* Nav */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-5">
        {groups.map(group => (
          <div key={group}>
            <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">{group}</p>
            <ul className="space-y-0.5">
              {NAV_ITEMS.filter(i => i.group === group).map(item => {
                const isActive = active === item.id;
                return (
                  <li key={item.id}>
                    <button onClick={() => onNav(item.id)}
                      className={`w-full text-left px-3 py-2.5 rounded-lg flex items-center gap-3 transition-all duration-200 border-l-[3px] text-sm font-medium
                        ${isActive
                          ? 'bg-slate-800 text-white border-indigo-500 shadow-md shadow-black/20'
                          : 'text-slate-400 hover:bg-slate-800 hover:text-white border-transparent'}`}>
                      <span className={isActive ? 'text-indigo-400' : 'text-slate-500 group-hover:text-indigo-400'}>
                        {item.icon}
                      </span>
                      {item.label}
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-slate-800 space-y-2 shrink-0">
        <button onClick={onLogout}
          className="w-full flex items-center justify-center gap-2 py-2 rounded-lg bg-red-900/20 hover:bg-red-900/40 text-red-400 hover:text-red-300 transition-colors text-xs font-bold uppercase tracking-wider border border-red-900/30">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
          Cerrar Sesión
        </button>
        <p className="text-[10px] text-slate-600 text-center uppercase tracking-widest">v2.6 Secure · El Arrejuntao</p>
      </div>
    </nav>
  );
}

// ─── Dashboard ────────────────────────────────────────────────────────────────
function ViewDashboard({ contacts, onNav }) {
  const valid   = contacts.filter(c => c.phone !== 'N/A');
  const sent    = contacts.filter(c => c.status === 'Enviado').length;
  const pending = contacts.filter(c => c.status === 'Pendiente').length;
  const batches = Math.ceil(valid.length / BATCH_SIZE);

  const donutData = {
    labels: ['Enviado', 'Pendiente'],
    datasets: [{ data: [sent, pending], backgroundColor: ['#10B981','#F59E0B'], borderWidth: 0 }]
  };
  const barData = {
    labels: ['Válidos', 'Sin Dato'],
    datasets: [{ label: 'Contactos', data: [valid.length, contacts.length - valid.length], backgroundColor: ['#6366f1','#f43f5e'], borderRadius: 4 }]
  };

  const statCards = [
    { label: 'Total Contactos',  val: contacts.length, color: 'blue',    icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg> },
    { label: 'Válidos (Únicos)', val: valid.length,    color: 'emerald', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg> },
    { label: 'Pendientes',       val: pending,         color: 'amber',   icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg> },
  ];

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((s, i) => (
          <div key={i} className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
            <div className="flex items-center justify-between mb-4">
              <p className="text-sm font-medium text-slate-500">{s.label}</p>
              <div className={`p-2 bg-${s.color}-50 rounded-lg text-${s.color}-600`}>{s.icon}</div>
            </div>
            <h3 className="text-2xl font-bold text-slate-800">{s.val}</h3>
          </div>
        ))}
        {/* Batches card */}
        <div onClick={() => onNav('broadcast')} className="bg-indigo-600 p-6 rounded-xl shadow-lg shadow-indigo-600/20 cursor-pointer hover:bg-indigo-700 transition-colors text-white">
          <div className="flex items-center justify-between mb-4">
            <p className="text-sm font-medium text-indigo-100">Lotes Listos</p>
            <div className="p-2 bg-white/10 rounded-lg"><svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z"/></svg></div>
          </div>
          <div className="flex items-baseline justify-between">
            <h3 className="text-2xl font-bold">{batches}</h3>
            <span className="text-xs bg-white/10 px-2 py-1 rounded">Ver →</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
          <h3 className="text-base font-semibold text-slate-800 mb-4">Estado de los Envíos</h3>
          <div className="h-52"><Doughnut data={donutData} options={{ responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: { legend: { position: 'bottom', labels: { usePointStyle: true, padding: 15, font: { size: 11 } } } } }}/></div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
          <h3 className="text-base font-semibold text-slate-800 mb-4">Calidad de la Base de Datos</h3>
          <div className="h-52"><Bar data={barData} options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: '#f1f5f9' } }, x: { grid: { display: false } } } }}/></div>
        </div>
      </div>
    </div>
  );
}

// ─── Contacts Table ────────────────────────────────────────────────────────────
function ContactRow({ contact, globalIndex, onEdit, onShare, onDelete, onMark }) {
  const sent = contact.status === 'Enviado';
  return (
    <tr className="hover:bg-slate-50 transition-colors group border-b border-slate-50">
      <td className="px-6 py-4 text-sm font-medium text-slate-700">{contact.name}</td>
      <td className="px-6 py-4 text-xs font-mono text-slate-500">{contact.phone}</td>
      <td className="px-6 py-4 text-xs text-slate-500 truncate max-w-[150px]">{contact.email}</td>
      <td className="px-6 py-4 text-center">
        <span className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide ${sent ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}`}>
          {sent ? 'Listo' : 'Pendiente'}
        </span>
      </td>
      <td className="px-6 py-4 text-right">
        <div className="flex items-center justify-end gap-1 opacity-100 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
          <button onClick={() => onShare(globalIndex)} title="Compartir" className="p-1.5 hover:bg-indigo-50 rounded text-slate-400 hover:text-indigo-600 transition-colors">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/></svg>
          </button>
          <button onClick={() => onEdit(globalIndex)} title="Editar" className="p-1.5 hover:bg-slate-100 rounded text-slate-400 hover:text-slate-600 transition-colors">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          </button>
          {!sent && (
            <button onClick={() => onMark(globalIndex)} title="Marcar Enviado" className="p-1.5 hover:bg-emerald-50 rounded text-slate-400 hover:text-emerald-600 transition-colors">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7"/></svg>
            </button>
          )}
          <button onClick={() => onDelete(globalIndex)} title="Eliminar" className="p-1.5 hover:bg-red-50 rounded text-slate-400 hover:text-red-600 transition-colors">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </div>
      </td>
    </tr>
  );
}

function ContactsTable({ contacts, allContacts, page, onPageChange, onEdit, onShare, onDelete, onMark }) {
  const PER_PAGE = 10;
  const total = Math.ceil(contacts.length / PER_PAGE);
  const slice = contacts.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  return (
    <div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse" style={{ minWidth: 700 }}>
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                {['Nombre','Teléfono','Email','Estado','Acciones'].map(h => (
                  <th key={h} className={`px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider ${h === 'Acciones' ? 'text-right' : h === 'Estado' ? 'text-center' : ''}`}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {slice.length === 0
                ? <tr><td colSpan={5} className="p-8 text-center text-slate-400 italic text-sm">Sin resultados.</td></tr>
                : slice.map((c) => {
                    const gi = allContacts.indexOf(c);
                    return <ContactRow key={gi} contact={c} globalIndex={gi} onEdit={onEdit} onShare={onShare} onDelete={onDelete} onMark={onMark}/>;
                  })
              }
            </tbody>
          </table>
        </div>
      </div>
      {total > 1 && (
        <nav className="flex justify-center items-center gap-2 mt-6">
          <button onClick={() => onPageChange(page - 1)} disabled={page === 1}
            className="w-8 h-8 rounded-lg border border-slate-200 flex items-center justify-center text-slate-500 disabled:opacity-30 hover:bg-white transition-colors text-sm">←</button>
          <span className="px-3 text-xs font-medium text-slate-500">{page} / {total}</span>
          <button onClick={() => onPageChange(page + 1)} disabled={page === total}
            className="w-8 h-8 rounded-lg border border-slate-200 flex items-center justify-center text-slate-500 disabled:opacity-30 hover:bg-white transition-colors text-sm">→</button>
        </nav>
      )}
    </div>
  );
}

// ─── Views ────────────────────────────────────────────────────────────────────
function Placeholder({ title, subtitle, color, svgPath }) {
  return (
    <div>
      <div className="mb-8"><h2 className="text-2xl font-bold text-slate-800">{title}</h2><p className="text-sm text-slate-500">{subtitle}</p></div>
      <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200 text-center">
        <div className={`inline-block p-4 bg-${color}-50 rounded-full text-${color}-600 mb-4`}>
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={svgPath}/></svg>
        </div>
        <h3 className="text-lg font-bold text-slate-800">Próximamente</h3>
        <p className="text-slate-500 mt-2">Esta funcionalidad estará disponible en la próxima versión.</p>
      </div>
    </div>
  );
}

// ─── Broadcast ────────────────────────────────────────────────────────────────
function ViewBroadcast({ contacts, onShowBatch }) {
  const valid = contacts.filter(c => c.phone !== 'N/A');
  const batches = [];
  for (let i = 0; i < valid.length; i += BATCH_SIZE)
    batches.push(valid.slice(i, i + BATCH_SIZE));

  return (
    <div>
      <div className="mb-8"><h2 className="text-2xl font-bold text-slate-800">Centro de Envíos</h2><p className="text-sm text-slate-500">Gestiona tus listas de difusión.</p></div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-xl p-6 shadow-sm border border-slate-100">
          <h3 className="font-semibold text-slate-800 mb-4">Lotes Disponibles</h3>
          {batches.length === 0
            ? <p className="text-center py-8 text-slate-400 text-sm">No hay contactos válidos para generar lotes.</p>
            : <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                {batches.map((batch, i) => (
                  <button key={i} onClick={() => onShowBatch(i + 1, batch)}
                    className="p-4 bg-slate-100 hover:bg-white hover:shadow-md text-slate-600 rounded-xl transition-all text-left border border-slate-200">
                    <span className="block text-lg font-bold mb-1">Lote {i + 1}</span>
                    <span className="text-xs opacity-70 block">{i * BATCH_SIZE + 1}-{Math.min((i + 1) * BATCH_SIZE, valid.length)}</span>
                    <span className="text-[10px] bg-white/40 px-2 py-0.5 rounded mt-2 inline-block font-medium">{batch.length} contactos</span>
                  </button>
                ))}
              </div>
          }
        </div>
        <div className="lg:col-span-1 bg-gradient-to-b from-slate-800 to-slate-900 rounded-xl p-6 text-white shadow-xl">
          <h3 className="font-bold text-lg mb-4">🖼️ Envío de Imágenes</h3>
          <p className="text-slate-300 text-xs mb-4 leading-relaxed">Funcionalidad manual debido a restricciones del navegador.</p>
          <ul className="space-y-3 text-xs text-slate-400">
            <li className="flex gap-2"><span className="text-indigo-400 font-bold">1.</span> Carga imagen en Configuración.</li>
            <li className="flex gap-2"><span className="text-indigo-400 font-bold">2.</span> Ve a Contactos → Compartir.</li>
            <li className="flex gap-2"><span className="text-indigo-400 font-bold">3.</span> Descarga la imagen.</li>
            <li className="flex gap-2"><span className="text-indigo-400 font-bold">4.</span> Copia el lote y adjunta en WA.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

// ─── Config ────────────────────────────────────────────────────────────────────
function ViewConfig({ onContactsLoaded, onImageLoaded, image }) {
  const [loading, setLoading] = useState(false);

  const handleVCF = (e) => {
    const files = e.target.files;
    if (!files.length) return;
    setLoading(true);
    const proms = Array.from(files).map(f => new Promise(res => {
      const r = new FileReader();
      r.onload = ev => res(parseVCF(ev.target.result));
      r.readAsText(f);
    }));
    Promise.all(proms).then(results => {
      const all = results.flat().sort((a, b) => a.name.localeCompare(b.name));
      onContactsLoaded(all);
      setLoading(false);
    });
  };

  const handleImg = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    const r = new FileReader();
    r.onload = ev => onImageLoaded(ev.target.result);
    r.readAsDataURL(f);
  };

  const clearAll = () => {
    if (confirm('¿Borrar todos los datos?')) {
      localStorage.removeItem('vcf_contacts');
      localStorage.removeItem('vcf_image');
      location.reload();
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8"><h2 className="text-2xl font-bold text-slate-800">Configuración</h2><p className="text-sm text-slate-500">Ajustes del sistema.</p></div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200 mb-6">
        <div className="flex items-center mb-4">
          <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold mr-3 text-sm">1</div>
          <label className="text-base font-semibold text-slate-800">Importar Contactos (.vcf)</label>
        </div>
        <input type="file" accept=".vcf" multiple onChange={handleVCF}
          className="w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer border border-dashed border-slate-300 rounded-lg p-3"/>
        {loading && <p className="mt-3 text-indigo-600 text-sm font-medium animate-pulse">Procesando…</p>}
      </div>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200 mb-6">
        <div className="flex items-center mb-4">
          <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold mr-3 text-sm">2</div>
          <label className="text-base font-semibold text-slate-800">Imagen Promocional</label>
        </div>
        <input type="file" accept="image/*" onChange={handleImg}
          className="w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer border border-dashed border-slate-300 rounded-lg p-3"/>
        {image && <img src={image} alt="preview" className="mt-4 max-h-40 rounded shadow-sm"/>}
      </div>

      <div className="border border-red-200 rounded-xl p-6 bg-red-50/50">
        <h3 className="text-red-700 font-bold text-sm mb-1">Zona de Peligro</h3>
        <p className="text-red-600/70 text-xs mb-4">Elimina todos los datos almacenados localmente.</p>
        <button onClick={clearAll} className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm font-medium">Resetear Sistema</button>
      </div>
    </div>
  );
}

// ─── Modals ────────────────────────────────────────────────────────────────────
function EditModal({ contact, onSave, onClose }) {
  const [name, setName]   = useState(contact.name);
  const [phone, setPhone] = useState(contact.phone === 'N/A' ? '' : contact.phone);
  const [email, setEmail] = useState(contact.email === 'N/A' ? '' : contact.email);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" onClick={onClose}/>
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-md border border-slate-200 z-10">
        <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-gray-50 rounded-t-xl">
          <h3 className="text-lg font-bold text-slate-800">Editar Contacto</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600">✕</button>
        </div>
        <div className="p-6 space-y-4">
          <div><label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Nombre</label>
            <input value={name} onChange={e => setName(e.target.value)} className="block w-full rounded-lg border border-slate-300 bg-white py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"/></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Teléfono</label>
              <input value={phone} onChange={e => setPhone(e.target.value)} className="block w-full rounded-lg border border-slate-300 bg-white py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"/></div>
            <div><label className="block text-xs font-semibold text-slate-500 uppercase mb-1">Email</label>
              <input value={email} onChange={e => setEmail(e.target.value)} className="block w-full rounded-lg border border-slate-300 bg-white py-2 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"/></div>
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button onClick={onClose} className="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50">Cancelar</button>
            <button onClick={() => onSave({ ...contact, name, phone: phone || 'N/A', email: email || 'N/A' })}
              className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 shadow-sm">Guardar</button>
          </div>
        </div>
      </div>
    </div>
  );
}

function BatchModal({ numbers, onClose }) {
  const [copied, setCopied] = useState(false);
  const copy = () => { navigator.clipboard.writeText(numbers); setCopied(true); setTimeout(() => setCopied(false), 2000); };
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" onClick={onClose}/>
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-lg border border-slate-200 z-10 p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-bold text-slate-800">Lista de Difusión</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600">✕</button>
        </div>
        <textarea readOnly rows={6} value={numbers}
          className="w-full rounded-lg bg-gray-50 border border-slate-200 text-xs font-mono p-3 text-slate-600 focus:outline-none"/>
        <div className="mt-4 flex justify-end">
          <button onClick={copy}
            className={`px-4 py-2 rounded-lg font-medium text-sm shadow-sm transition-colors ${copied ? 'bg-emerald-600 text-white' : 'bg-indigo-600 hover:bg-indigo-700 text-white'}`}>
            {copied ? '✓ Copiado!' : 'Copiar al Portapapeles'}
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── App ──────────────────────────────────────────────────────────────────────
export default function App() {
  const [authed, setAuthed]       = useState(() => sessionStorage.getItem('is_authenticated') === 'true');
  const [view, setView]           = useState('dashboard');
  const [contacts, setContacts]   = useState(() => { try { return JSON.parse(localStorage.getItem('vcf_contacts') || '[]'); } catch { return []; } });
  const [image, setImage]         = useState(() => localStorage.getItem('vcf_image') || null);
  const [search, setSearch]       = useState('');
  const [page, setPage]           = useState(1);
  const [sidebarOpen, setSidebar] = useState(false);
  const [toast, setToast]         = useState(null);

  // Modals
  const [editIdx, setEditIdx]     = useState(null);
  const [batchNums, setBatchNums] = useState(null);
  const [batchView, setBatchView] = useState(null); // { num, contacts }

  const showToast = useCallback((msg, color = 'bg-indigo-600') => setToast({ msg, color }), []);

  // Persist
  useEffect(() => { localStorage.setItem('vcf_contacts', JSON.stringify(contacts)); }, [contacts]);
  useEffect(() => { if (image) localStorage.setItem('vcf_image', image); else localStorage.removeItem('vcf_image'); }, [image]);

  const handleLogin  = () => { sessionStorage.setItem('is_authenticated', 'true'); setAuthed(true); };
  const handleLogout = () => { sessionStorage.removeItem('is_authenticated'); location.reload(); };

  const handleNav = (id) => { setView(id); setPage(1); setSidebar(false); setBatchView(null); };

  const markSent = (gi) => {
    setContacts(prev => prev.map((c, i) => i === gi ? { ...c, status: 'Enviado' } : c));
    showToast('Marcado como ENVIADO', 'bg-emerald-500');
  };

  const saveEdit = (updated) => {
    setContacts(prev => prev.map((c, i) => i === editIdx ? updated : c));
    setEditIdx(null);
    showToast('Contacto actualizado');
  };

  const deleteContact = (gi) => {
    if (!confirm(`¿Eliminar "${contacts[gi]?.name}"?`)) return;
    setContacts(prev => prev.filter((_, i) => i !== gi));
    showToast('Eliminado correctamente', 'bg-slate-600');
  };

  const filtered = contacts.filter(c =>
    !search || c.name.toLowerCase().includes(search.toLowerCase()) || c.phone.includes(search)
  );

  const handleContactsLoaded = (newContacts) => {
    setContacts(newContacts);
    showToast(`${newContacts.length} contactos importados`, 'bg-emerald-500');
  };

  const handleShowBatch = (num, batch) => {
    setBatchView({ num, contacts: batch });
    setView('batch-management');
  };

  if (!authed) return <LoginScreen onLogin={handleLogin}/>;

  return (
    <div className="flex h-screen bg-gray-50 font-sans overflow-hidden">
      {/* Sidebar */}
      <Sidebar active={view} onNav={handleNav} onLogout={handleLogout}
        collapsed={!sidebarOpen} onToggleMobile={() => setSidebar(false)}/>

      {/* Mobile overlay */}
      {sidebarOpen && <div className="fixed inset-0 bg-slate-900/50 z-40 md:hidden" onClick={() => setSidebar(false)}/>}

      {/* Main */}
      <main className="flex-1 flex flex-col overflow-hidden md:ml-64">
        {/* Header */}
        <div className="h-16 px-6 flex items-center justify-between bg-white/90 backdrop-blur-md border-b border-gray-200 z-30 shrink-0 sticky top-0">
          <div className="flex items-center gap-4">
            <button onClick={() => setSidebar(s => !s)} className="p-2 -ml-2 text-slate-500 hover:bg-slate-100 hover:text-indigo-600 rounded-lg transition-all md:hidden">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h7"/></svg>
            </button>
            <div>
              <h1 className="font-bold text-lg text-slate-800 leading-tight">CRM El Arrejuntao</h1>
              <span className="text-xs text-slate-500 hidden sm:block">Bienvenido, Administrador</span>
            </div>
          </div>
          <div className="w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold text-sm border border-indigo-200">A</div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 md:p-8">
          <div className="max-w-7xl mx-auto">

            {view === 'dashboard' && <ViewDashboard contacts={contacts} onNav={handleNav}/>}

            {view === 'management' && (
              <div>
                <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-6 gap-4">
                  <div><h2 className="text-2xl font-bold text-slate-800">Directorio</h2><p className="text-sm text-slate-500">Gestiona tus contactos.</p></div>
                  <div className="relative w-full sm:w-72">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <svg className="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                    </div>
                    <input value={search} onChange={e => { setSearch(e.target.value); setPage(1); }}
                      className="block w-full pl-10 pr-3 py-2 border border-slate-300 rounded-lg bg-white text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-indigo-500 text-sm shadow-sm"
                      placeholder="Buscar contacto..."/>
                  </div>
                </div>
                <ContactsTable contacts={filtered} allContacts={contacts} page={page}
                  onPageChange={setPage} onEdit={setEditIdx} onShare={() => {}} onDelete={deleteContact} onMark={markSent}/>
              </div>
            )}

            {view === 'batch-management' && batchView && (
              <div>
                <div className="flex items-center justify-between mb-6">
                  <div><h2 className="text-2xl font-bold text-slate-800">Lote #{batchView.num} ({batchView.contacts.length} contactos)</h2></div>
                  <div className="flex gap-3">
                    <button onClick={() => setBatchNums(batchView.contacts.map(c => c.phone).join(','))}
                      className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded-lg">Copiar Lista</button>
                    <button onClick={() => { setBatchView(null); setView('broadcast'); }}
                      className="px-4 py-2 bg-white border border-slate-300 text-slate-700 text-sm font-medium rounded-lg hover:bg-slate-50">Volver</button>
                  </div>
                </div>
                <ContactsTable contacts={batchView.contacts} allContacts={contacts} page={page}
                  onPageChange={setPage} onEdit={setEditIdx} onShare={() => {}} onDelete={deleteContact} onMark={markSent}/>
              </div>
            )}

            {view === 'analytics' && <Placeholder title="Analíticas Avanzadas" subtitle="Reportes detallados del rendimiento." color="primary" svgPath="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>}

            {view === 'broadcast' && <ViewBroadcast contacts={contacts} onShowBatch={handleShowBatch}/>}

            {view === 'calendar' && <Placeholder title="Calendario" subtitle="Agenda tus campañas." color="emerald" svgPath="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>}

            {view === 'team' && (
              <div>
                <div className="mb-8"><h2 className="text-2xl font-bold text-slate-800">Equipo</h2><p className="text-sm text-slate-500">Gestiona usuarios y permisos.</p></div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
                    <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold">A</div>
                    <div><h4 className="font-bold text-slate-800">Admin</h4><p className="text-xs text-slate-500">Super Administrador</p></div>
                  </div>
                </div>
              </div>
            )}

            {view === 'config' && <ViewConfig onContactsLoaded={handleContactsLoaded} onImageLoaded={setImage} image={image}/>}

            {view === 'trash' && (
              <div>
                <div className="mb-8"><h2 className="text-2xl font-bold text-slate-800">Papelera</h2><p className="text-sm text-slate-500">Recupera elementos eliminados.</p></div>
                <div className="bg-white p-12 rounded-xl text-center border border-slate-200"><p className="text-slate-400">La papelera está vacía.</p></div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Modals */}
      {editIdx !== null && <EditModal contact={contacts[editIdx]} onSave={saveEdit} onClose={() => setEditIdx(null)}/>}
      {batchNums !== null && <BatchModal numbers={batchNums} onClose={() => setBatchNums(null)}/>}

      {/* Toast */}
      {toast && <Toast msg={toast.msg} color={toast.color} onDone={() => setToast(null)}/>}
    </div>
  );
}

"""fix_cand_empty.py — Corrige el empty-state bug en _candConsultar()"""
with open('static/dashboard/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar el fragmento exacto
marker = "if(!_candData.length && d.ok){"
idx = content.find(marker)
if idx < 0:
    print("MARCADOR NO ENCONTRADO")
    exit(1)

# Encontrar el cierre de este bloque (el return + cierre de if + linea siguiente)
# Buscar el fallback line despues del bloque
end_marker = "if(!_candData.length) _candData = [..._CAND_DEMO];   // fallback demo si no hay datos reales"
end_idx = content.find(end_marker, idx)
if end_idx < 0:
    print("END_MARKER NO ENCONTRADO")
    print("Contexto:", repr(content[idx:idx+500]))
    exit(1)

end_pos = end_idx + len(end_marker)
block_to_replace = content[idx:end_pos]
print("Bloque encontrado:", repr(block_to_replace[:100]))

replacement = """if(!_candData.length){
      // Sin datos reales: fallback a demo con aviso visual
      _candData = [..._CAND_DEMO];
      setTimeout(()=>{
        const tabla = document.getElementById('cand-tabla');
        if(tabla){
          const info = document.createElement('div');
          info.style.cssText = 'padding:8px 16px;background:var(--surface);border:1px solid var(--border);border-radius:6px 6px 0 0;font-size:12px;color:var(--muted);text-align:center;border-bottom:none';
          info.textContent = '\\u{1F4C5} Sin ventas reales para esta fecha \\u2014 mostrando datos de demostraci\\u00f3n';
          tabla.parentNode.insertBefore(info, tabla);
        }
      }, 50);
    }"""

new_content = content[:idx] + replacement + content[end_pos:]
with open('static/dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

count_after = new_content.count("if(!_candData.length")
print(f"OK — guardado | Ocurrencias restantes de candData.length: {count_after}")

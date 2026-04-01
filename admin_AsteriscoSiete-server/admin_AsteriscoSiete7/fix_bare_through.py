"""fix_bare_through.py  — Corrige parámetros 'through' sin prefijo app."""
f = 'admin_juego/models.py'
with open(f, encoding='utf-8', errors='replace') as fh:
    c = fh.read()

c = c.replace("through='TipoProducto_Grupos'",  "through='admin_juego.TipoProducto_Grupos'")
c = c.replace("through='TipoApuesta_Grupos'",   "through='admin_juego.ModalidadJuego_Grupos'")
c = c.replace("through='GruposApuesta'",         "through='admin_juego.GruposApuesta'")

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print('OK: bare through refs corregidas')

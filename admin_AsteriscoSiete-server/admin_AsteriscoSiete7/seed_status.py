from admin_status.models import Status

required = [
    {'name': 'Habilitado',         'codename': 'status_habilitado',        'content_type': 2, 'order': 1},
    {'name': 'Pendiente',          'codename': 'status_pendiente',         'content_type': 2, 'order': 2},
    {'name': 'Reanudado',          'codename': 'status_reanudado',         'content_type': 2, 'order': 3},
    {'name': 'Eliminado',          'codename': 'status_eliminado',         'content_type': 2, 'order': 4},
    {'name': 'Eliminado frio',     'codename': 'status_eliminado_frio',    'content_type': 2, 'order': 5},
    {'name': 'Procesandose',       'codename': 'status_procesandose',      'content_type': 2, 'order': 6},
    {'name': 'Procesado',          'codename': 'status_procesado',         'content_type': 2, 'order': 7},
    {'name': 'Activo',             'codename': 'status_activo',            'content_type': 4, 'order': 1},
    {'name': 'Activo sin venta',   'codename': 'status_activo_sin_venta',  'content_type': 4, 'order': 2},
    {'name': 'Bloqueado',          'codename': 'status_bloqueado',         'content_type': 4, 'order': 3},
    {'name': 'Procesando ganador', 'codename': 'status_procesandoganador', 'content_type': 4, 'order': 4},
    {'name': 'Perdedor',           'codename': 'status_perdedor',          'content_type': 4, 'order': 5},
    {'name': 'Nuevo',              'codename': 'status_nuevo',             'content_type': 1, 'order': 1},
]

created = 0
for s in required:
    obj, c = Status.objects.get_or_create(codename=s['codename'], defaults=s)
    if c:
        created += 1

print(f"Creados: {created}, Total Status: {Status.objects.count()}")
for s in Status.objects.order_by('content_type','codename').values_list('codename','name'):
    print(f"  {s[0]} -> {s[1]}")

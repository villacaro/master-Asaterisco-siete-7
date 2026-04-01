"""
usuarios/views.py  –  Vistas del panel de administración
"""
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from . import firebase_service as fb


@staff_member_required
def lista_usuarios(request):
    """Página principal: lista todos los usuarios de Firebase Auth."""
    usuarios = fb.listar_usuarios()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})


@staff_member_required
def crear_usuario(request):
    """Formulario para crear un nuevo usuario Firebase."""
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        nombre   = request.POST.get('nombre', '').strip()

        if not email or not password:
            messages.error(request, 'El correo y la contraseña son obligatorios.')
        else:
            user, error = fb.crear_usuario(email, password, nombre)
            if user:
                messages.success(request, f'✅ Usuario {email} creado correctamente.')
                return redirect('lista_usuarios')
            else:
                messages.error(request, f'Error: {error}')

    return render(request, 'usuarios/crear.html')


@staff_member_required
def toggle_usuario(request, uid):
    """Habilita o deshabilita un usuario Firebase."""
    deshabilitar = request.GET.get('deshabilitar') == '1'
    ok, error = fb.deshabilitar_usuario(uid, deshabilitar)
    if ok:
        accion = 'deshabilitado' if deshabilitar else 'habilitado'
        messages.success(request, f'✅ Usuario {accion} correctamente.')
    else:
        messages.error(request, f'Error: {error}')
    return redirect('lista_usuarios')


@staff_member_required
def eliminar_usuario(request, uid):
    """Elimina un usuario de Firebase Auth."""
    if request.method == 'POST':
        ok, error = fb.eliminar_usuario(uid)
        if ok:
            messages.success(request, '✅ Usuario eliminado correctamente.')
        else:
            messages.error(request, f'Error: {error}')
    return redirect('lista_usuarios')


@staff_member_required
def cambiar_password(request, uid):
    """Cambia la contraseña de un usuario."""
    if request.method == 'POST':
        nueva = request.POST.get('nueva_password', '').strip()
        if len(nueva) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
        else:
            ok, error = fb.cambiar_password(uid, nueva)
            if ok:
                messages.success(request, '✅ Contraseña actualizada.')
            else:
                messages.error(request, f'Error: {error}')
    return redirect('lista_usuarios')


@staff_member_required
def detalle_usuario(request, uid):
    """Ver clientes y apuestas de un usuario específico."""
    clientes = fb.obtener_clientes_usuario(uid)
    apuestas = fb.obtener_apuestas_usuario(uid)
    return render(request, 'usuarios/detalle.html', {
        'uid':      uid,
        'clientes': clientes,
        'apuestas': apuestas,
    })

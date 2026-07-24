import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from admin_users.models import Users, UserProfile
from admin_permisologia.models import Permissions

@csrf_exempt
def gestion_usuarios_api(request):
    if request.method == 'GET':
        # 1. Traer todos los perfiles posibles
        profiles = list(UserProfile.objects.values('id', 'nombre', 'codename').order_by('content_type'))
        
        # 2. Traer todos los permisos posibles (Reportes, vistas, etc)
        # Filtramos para no mandar miles, solo los que tengan menu o sean útiles.
        all_perms = list(Permissions.objects.values('id', 'name', 'codename', 'content_type').order_by('content_type', 'name'))
        
        # 3. Traer los usuarios (limitar a 200 o paginar si son muchos, pero mandaremos todos para el frontend)
        users_qs = Users.objects.select_related('profile').prefetch_related('user_permissions')
        
        users_data = []
        for u in users_qs:
            users_data.append({
                'id': u.id,
                'user': u.user,
                'email': u.email or '',
                'etiqueta': u.etiqueta or '',
                'profile_id': u.profile_id,
                'profile_name': u.profile.nombre if u.profile else 'Sin Perfil',
                'profile_codename': u.profile.codename if u.profile else '',
                'is_active': True,
                'permissions': list(u.user_permissions.values_list('id', flat=True)),
            })
            
        return JsonResponse({
            'ok': True,
            'profiles': profiles,
            'permissions': all_perms,
            'users': users_data,
        })
        
    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_id = body.get('id')
            username = body.get('user', '').strip()
            password = body.get('password', '').strip()
            email = body.get('email', '').strip()
            etiqueta = body.get('etiqueta', '').strip()
            profile_id = body.get('profile_id')
            perms_ids = body.get('permissions', [])
            
            if not username or not profile_id:
                return JsonResponse({'error': 'Usuario y Perfil son obligatorios'}, status=400)
                
            if user_id:
                # Update
                try:
                    u = Users.objects.get(pk=user_id)
                except Users.DoesNotExist:
                    return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
                
                u.user = username
                if password:
                    u.set_password(password)
                u.email = email
                u.etiqueta = etiqueta
                u.profile_id = profile_id
                u.save()
            else:
                # Create
                if not password:
                    return JsonResponse({'error': 'La contraseña es obligatoria para usuarios nuevos'}, status=400)
                from django.db import IntegrityError
                try:
                    u = Users(
                        user=username,
                        email=email,
                        etiqueta=etiqueta,
                        profile_id=profile_id,
                    )
                    u.set_password(password)
                    u.save()
                except IntegrityError:
                    return JsonResponse({'error': 'El nombre de usuario ya existe'}, status=400)
                    
            if perms_ids is not None:
                u.user_permissions.set(perms_ids)
                
            return JsonResponse({'ok': True, 'msg': 'Usuario guardado correctamente', 'user_id': u.id})
            
        except Exception as e:
            import traceback
            return JsonResponse({'error': str(e), 'trace': traceback.format_exc()}, status=500)
            
    elif request.method == 'DELETE':
        user_id = request.GET.get('id')
        if not user_id:
            return JsonResponse({'error': 'ID no proporcionado'}, status=400)
        try:
            u = Users.objects.get(pk=user_id)
            u.delete()
            return JsonResponse({'ok': True, 'msg': 'Usuario eliminado'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

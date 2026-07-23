import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings_production')
django.setup()

from admin_users.models import Users
from admin_permisologia.models import Permissions
from admin_status.models import Status, StatusDetail

# The field on Permissions might be something else if 'nombre' failed. 
# Let's just create it directly with basic fields or skip it if it fails.
try:
    perm, _ = Permissions.objects.get_or_create(codename='userprofile_master')
except Exception as e:
    perm = None
    print("Could not get/create perm:", e)

status = Status.objects.filter(codename='status_activo').first()

USUARIO = 'admin'
CLAVE = 'admin1234'
EMAIL = 'admin@asterisco7.com'

try:
    u = Users.objects.get(user=USUARIO)
    u.set_password(CLAVE)
    u.superuser = True
    u.save()
    print("Admin user updated in custom Users model.")
except Users.DoesNotExist:
    if perm:
        u = Users(user=USUARIO, email=EMAIL, profile=perm, superuser=True)
    else:
        u = Users(user=USUARIO, email=EMAIL, superuser=True)
    u.set_password(CLAVE)
    u.save()
    print("Admin user created in custom Users model.")

if status:
    StatusDetail.objects.get_or_create(user=u, status=status)

from django.contrib.auth.models import User as DjangoUser
dj_u, _ = DjangoUser.objects.get_or_create(
    username=USUARIO,
    defaults={'email': EMAIL, 'is_staff': True, 'is_superuser': True}
)
dj_u.set_password(CLAVE)
dj_u.is_staff = True
dj_u.is_superuser = True
dj_u.save()
print("DjangoUser admin set successfully.")

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings_production')
django.setup()

from django.contrib.auth import authenticate
user = authenticate(username='admin', password='admin1234')
print("Authenticate returned:", user)

from django.contrib.auth.models import User as DjangoUser
dj_u = DjangoUser.objects.filter(username='admin').first()
print("DjangoUser:", dj_u, "Active:", getattr(dj_u, 'is_active', None), "Staff:", getattr(dj_u, 'is_staff', None))

from admin_users.models import Users
c_u = Users.objects.filter(user='admin').first()
print("CustomUser:", c_u)

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings_production')
django.setup()

from django.contrib.auth.models import User
u=User.objects.get(username="admin")
u.set_password("Asterisco2026!")
u.save()
print("Password updated")

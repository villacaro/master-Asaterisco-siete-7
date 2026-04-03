path = 'admin_AsteriscoSiete-server/admin_AsteriscoSiete7/admin_asterisco7/settings.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

if 'firebase_admin' not in text:
    injection = """
# FIREBASE ADMIN SETUP
import os
import firebase_admin
from firebase_admin import credentials

# Busca el archivo serviceAccountKey.json o cualquier firebase*.json
firebase_key_path = os.path.join(BASE_DIR, 'serviceAccountKey.json')

if os.path.exists(firebase_key_path) and not firebase_admin._apps:
    try:
        cred = credentials.Certificate(firebase_key_path)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase Admin SDK Initialized Successfully!")
    except Exception as e:
        print(f"⚠️ Failed to init Firebase Admin: {e}")
"""
    with open(path, 'a', encoding='utf-8') as f:
        f.write(injection)
    print("Injected logic!")
else:
    print("Already in settings!")

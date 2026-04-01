"""
encode_firebase_key.py
Convierte serviceAccountKey.json a base64 para Railway.

Uso:
    python encode_firebase_key.py
Luego copia el resultado y pégalo como variable de entorno FIREBASE_CREDENTIALS_B64 en Railway.
"""
import base64, os, sys

# Buscar el archivo
locations = [
    'api/serviceAccountKey.json',
    'serviceAccountKey.json',
    '../api/serviceAccountKey.json',
]

key_path = None
for loc in locations:
    if os.path.exists(loc):
        key_path = loc
        break

if not key_path:
    print("ERROR: No se encontró serviceAccountKey.json")
    print("Buscado en:", locations)
    sys.exit(1)

with open(key_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

print("=" * 60)
print("FIREBASE_CREDENTIALS_B64=")
print(b64)
print("=" * 60)
print(f"\nCopia el texto de arriba y pégalo en Railway como")
print("variable de entorno: FIREBASE_CREDENTIALS_B64")

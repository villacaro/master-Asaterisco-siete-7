import hashlib
import base64
import os

password = 'Taquilla2024!'
# Use a Django-compatible salt (22 chars)
salt = 'TaQuIlLaSaLt2024xYzAb'
iterations = 870000

dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), iterations)
encoded_hash = base64.b64encode(dk).decode('ascii')
django_hash = 'pbkdf2_sha256${}${}${}'.format(iterations, salt, encoded_hash)

print("=== HASH GENERADO ===")
print(django_hash)
print()
print("=== SQL PARA SUPABASE ===")
print("""INSERT INTO admin_comercializacion_usuariostaquilla 
("user", nombre, password, taquilla_id, status_id, pub_key_client, pub_key, priv_key, pk_clone)
VALUES (
  'taquilla1',
  'Operador Principal',
  '{}',
  1,
  1,
  '', '', '', 0
)
ON CONFLICT ("user") DO UPDATE SET password = EXCLUDED.password;""".format(django_hash))

import socket
host = "aws-1-us-east-1.pooler.supabase.com"
port = 6543
try:
    s = socket.create_connection((host, port), timeout=10)
    print("CONEXION PORT EXITOSA")
    s.close()
except Exception as e:
    print(f"ERROR: {e}")

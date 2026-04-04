import psycopg2

URL = "postgresql://postgres.ubmalhfretticpukafgy:ElArrejuntao2024Db!@aws-1-us-east-1.pooler.supabase.com:6543/postgres"

try:
    conn = psycopg2.connect(URL, connect_timeout=10)
    print("CONEXION EXITOSA")
    conn.close()
except Exception as e:
    print(f"ERROR: {str(e).strip()}")

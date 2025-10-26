import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import psycopg2

# Cargar variables del archivo .env si existe
load_dotenv()

# Variables
os.environ["user"] = "postgres.izybqmlrauuahpcjfvfb"
os.environ["password"] = "HubFastApi123456789"
os.environ["host"] = "aws-1-us-east-1.pooler.supabase.com"
os.environ["port"] = "6543"
os.environ["dbname"] = "postgres"

# Leer variables de entorno
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# URL de conexión completa (pooler + IPv4 + SSL)
DATABASE_URL = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
    f"?sslmode=require&options=-4"
)

# Crear el engine de SQLModel
engine = create_engine(DATABASE_URL, echo=True)


# Crear sesión
def get_session():
    with Session(engine) as session:
        yield session


# Prueba directa de conexión
if __name__ == "__main__":
    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME,
            sslmode="require",
            options="-4"  # Forzar IPv4
        )
        print("Conexión exitosa al pooler Supabase (IPv4, SSL habilitado)")
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        print("Hora actual en la base de datos:", cur.fetchone()[0])
        cur.close()
        conn.close()
        print("Conexión cerrada correctamente.")
    except Exception as e:
        print(f"Error al conectar: {e}")

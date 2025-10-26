import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv


# Cargar dotenv (aunque no exista, no da error)
load_dotenv()


# Variables quemadas (sin usar .env)
os.environ["user"] = "postgres"
os.environ["password"] = "HubFastApi123456789"
os.environ["host"] = "db.izybqmlrauuahpcjfvfb.supabase.co"
os.environ["port"] = "5432"
os.environ["dbname"] = "postgres"


# Leer variables de entorno
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")


# Crear la URL de conexión (PostgreSQL en Supabase)
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"


# Crear el engine
engine = create_engine(DATABASE_URL, echo=True)


# Crear sesión
def get_session():
    with Session(engine) as session:
        yield session


# Prueba de conexión directa
if __name__ == "__main__":
    import psycopg2

    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        print("✅ Conexión exitosa a la base de datos Supabase")
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        print("🕒 Hora actual en la BD:", cur.fetchone()[0])
        cur.close()
        conn.close()
        print("🔒 Conexión cerrada correctamente.")
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
# 🐍 Imagen base ligera con Python 3.11
FROM python:3.11-slim

# ⚙️ Configuración general del entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 🧩 Instalar dependencias necesarias para psycopg2 y PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 📂 Establecer el directorio de trabajo
WORKDIR /app

# 📦 Copiar e instalar dependencias primero (mejor uso de caché)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 🧠 Copiar el resto del proyecto
COPY . .

# ⚙️ Variables de entorno de conexión a Supabase (IPv4 pooler)
# Puedes sobreescribirlas con `docker run -e` o docker-compose
ENV SUPABASE_USER="postgres.izybqmlrauuahpcjfvfb" \
    SUPABASE_PASSWORD="HubFastApi123456789" \
    SUPABASE_HOST="aws-1-us-east-1.pooler.supabase.com" \
    SUPABASE_PORT="6543" \
    SUPABASE_DB="postgres" \
    SUPABASE_SSL="require" \
    SUPABASE_OPTIONS="-4"

# Construir DATABASE_URL dinámicamente en tu código Python usando estas variables,
# no directamente aquí, para mayor seguridad y flexibilidad.
# Ejemplo en Python:
# DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode={SSL}&options={OPTIONS}"

# 🌐 Exponer el puerto de tu aplicación (FastAPI)
EXPOSE 8000

# 🚀 Comando de inicio (Uvicorn para FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



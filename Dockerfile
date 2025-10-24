# Usa una imagen oficial de Python
FROM python:3.11.2-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY ./app /app

# Expone el puerto que usará FastAPI
EXPOSE 8000

# Comando para correr la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
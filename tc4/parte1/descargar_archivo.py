"""
En esta parte debe completar el código para 
descargar su imágen desde almacenamiento de objetos. 
"""
import requests
import boto3
import os

# ==========================================
# CONFIGURACIÓN
# ==========================================

# Token de Upstash Blob
UPSTASH_BLOB_TOKEN = "TU_TOKEN_DE_UPSTASH"

# Nombre del archivo que deseas descargar
ARCHIVO = "image.jpg"  # También puede ser "image.png"

# Nombre del archivo descargado
ARCHIVO_RECUPERADO = "codigoEstudiante"

# ==========================================
# VALIDAR EXTENSIÓN
# ==========================================

extension = os.path.splitext(ARCHIVO)[1].lower()

if extension not in [".jpg", ".png"]:
    raise ValueError("El archivo debe ser JPG o PNG")

# Nombre final según la extensión original
ARCHIVO_LOCAL = ARCHIVO_RECUPERADO + extension

# ==========================================
# OBTENER CREDENCIALES TEMPORALES
# ==========================================

credentials = requests.post(
    "https://blob.upstash.io/v1/credentials",
    headers={
        "Authorization": f"Bearer {UPSTASH_BLOB_TOKEN}"
    },
)

credentials.raise_for_status()
credentials = credentials.json()

# ==========================================
# CONECTAR CON S3
# ==========================================

s3 = boto3.client(
    "s3",
    endpoint_url=credentials["endpoint"],
    region_name="auto",
    aws_access_key_id=credentials["accessKeyId"],
    aws_secret_access_key=credentials["secretAccessKey"],
    aws_session_token=credentials["sessionToken"],
)

# ==========================================
# DESCARGAR ARCHIVO
# ==========================================

try:

    s3.download_file(
        credentials["bucket"],
        ARCHIVO,
        ARCHIVO_LOCAL
    )

    print("Archivo descargado correctamente")
    print(f"Archivo original: {ARCHIVO}")
    print(f"Archivo recuperado: {ARCHIVO_LOCAL}")

except Exception as e:

    print(f"Error al descargar el archivo: {e}")

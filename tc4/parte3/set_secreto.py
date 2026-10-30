
import redis
import json
import base64
import uuid
import os

from datetime import datetime, timezone

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM



# ==========================================
# CONFIGURACIÓN
# ==========================================

# URL de conexión a Upstash Redis
REDIS_URL = "rediss://default:TU_PASSWORD@TU_HOST.upstash.io:6379"

# Tópico donde se enviará el mensaje
TOPICO = "su_codigo_estudiante"


# ==========================================
# ARCHIVOS DE CLAVES
# ==========================================


# Clave pública del profesor
CLAVE_PUBLICA_PROFESOR = "profesor_public.pem"

# Clave privada del estudiante
CLAVE_PRIVADA_ESTUDIANTE = "estudiante_private.pem"


# ==========================================
# CONEXIÓN A REDIS
# ==========================================

r = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)


# ==========================================
# OBTENER MAC DEL EQUIPO
# ==========================================

def obtener_mac():

    mac = uuid.getnode()

    mac_formateada = ":".join(
        f"{(mac >> i) & 0xff:02X}"
        for i in range(40, -1, -8)
    )

    return mac_formateada


# ==========================================
# CARGAR CLAVES
# ==========================================

def cargar_clave_publica():

    with open(
        CLAVE_PUBLICA_PROFESOR,
        "rb"
    ) as archivo:

        return serialization.load_pem_public_key(
            archivo.read()
        )


def cargar_clave_privada():

    with open(
        CLAVE_PRIVADA_ESTUDIANTE,
        "rb"
    ) as archivo:

        return serialization.load_pem_private_key(
            archivo.read(),
            password=None
        )


# ==========================================
# GENERAR MENSAJE SECRETO
# ==========================================

def generar_mensaje(codigo_estudiante):

    mensaje = {

        "codigo_estudiante": codigo_estudiante,

        "mac_equipo": obtener_mac(),

        "fecha_hora": datetime.now(
            timezone.utc
        ).isoformat(),

        "id_actividad": uuid.uuid4().hex

    }

    return mensaje


# ==========================================
# FIRMAR MENSAJE
# ==========================================

def firmar_mensaje(mensaje, clave_privada):

    # Convertir mensaje a JSON
    mensaje_json = json.dumps(
        mensaje,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")

    # Generar firma RSA-PSS
    firma = clave_privada.sign(

        mensaje_json,

        padding.PSS(
            mgf=padding.MGF1(
                hashes.SHA256()
            ),
            salt_length=padding.PSS.MAX_LENGTH
        ),

        hashes.SHA256()

    )

    return mensaje_json, firma


# ==========================================
# CIFRAR MENSAJE
# ==========================================

def cifrar_mensaje(
    mensaje_json,
    firma,
    clave_publica
):

    # Construir paquete firmado
    paquete = {

        "mensaje": json.loads(
            mensaje_json.decode("utf-8")
        ),

        "firma": base64.b64encode(
            firma
        ).decode("utf-8")

    }

    paquete_json = json.dumps(
        paquete,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")

    # Generar clave AES aleatoria
    clave_aes = AESGCM.generate_key(
        bit_length=256
    )

    # Generar nonce AES-GCM
    nonce =  os.urandom(12)

    # Cifrar contenido con AES-GCM
    aes = AESGCM(clave_aes)

    contenido_cifrado = aes.encrypt(
        nonce,
        paquete_json,
        None
    )

    # Cifrar clave AES con RSA-OAEP
    clave_cifrada = clave_publica.encrypt(

        clave_aes,

        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )

    )

    # Crear sobre cifrado
    sobre = {

        "algoritmo": "RSA-OAEP+AES-GCM",

        "clave": base64.b64encode(
            clave_cifrada
        ).decode("utf-8"),

        "nonce": base64.b64encode(
            nonce
        ).decode("utf-8"),

        "contenido": base64.b64encode(
            contenido_cifrado
        ).decode("utf-8")

    }

    return json.dumps(sobre)


# ==========================================
# GENERAR BYTES ALEATORIOS
# ==========================================

def random_bytes(cantidad):

    from os import urandom

    return urandom(cantidad)


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

print("===================================")
print("GENERADOR DE MENSAJE SECRETO")
print("===================================")

codigo_estudiante = input(
    "Ingrese su código de estudiante: "
).strip()

if not codigo_estudiante:

    raise ValueError(
        "El código del estudiante no puede estar vacío"
    )


# Cargar claves
clave_publica = cargar_clave_publica()

clave_privada = cargar_clave_privada()


# Generar mensaje
mensaje = generar_mensaje(
    codigo_estudiante
)


# Firmar mensaje
mensaje_json, firma = firmar_mensaje(
    mensaje,
    clave_privada
)


# Cifrar mensaje
mensaje_cifrado = cifrar_mensaje(
    mensaje_json,
    firma,
    clave_publica
)


# ==========================================
# PUBLICAR EN REDIS
# ==========================================

resultado = r.publish(
    TOPICO,
    mensaje_cifrado
)


# ==========================================
# MOSTRAR RESULTADOS
# ==========================================

print()
print("===================================")
print("MENSAJE SECRETO GENERADO")
print("===================================")

print(f"Código estudiante: {codigo_estudiante}")

print(f"MAC equipo: {mensaje['mac_equipo']}")

print(f"Fecha y hora: {mensaje['fecha_hora']}")

print(f"ID actividad: {mensaje['id_actividad']}")

print()
print(f"Tópico Redis: {TOPICO}")

print(f"Suscriptores que lo recibieron: {resultado}")

print()
print("===================================")

r.close()

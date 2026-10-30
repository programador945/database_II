
import redis
import json
from datetime import datetime


# ==========================================
# CONFIGURACIÓN
# ==========================================

# URL de conexión a Upstash Redis
REDIS_URL = "rediss://default:TU_PASSWORD@TU_HOST.upstash.io:6379"

# Tópico al que se suscribe
TOPICO = "su_codigo_estudiante"

# Nombre del archivo donde se guardará el mensaje
ARCHIVO_SECRETO = "mensaje_secreto.txt"


# ==========================================
# CONEXIÓN A REDIS
# ==========================================

r = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)


# ==========================================
# SUSCRIPTOR SECRETO
# ==========================================

pubsub = r.pubsub()

print("===================================")
print("CONSUMIDOR SECRETO REDIS")
print("===================================")

print(f"Tópico: {TOPICO}")
print("Esperando mensaje secreto...")
print("Presiona Ctrl+C para finalizar.")
print()


try:

    # Suscribirse al tópico
    pubsub.subscribe(TOPICO)

    # Escuchar mensajes
    for mensaje in pubsub.listen():

        if mensaje["type"] == "message":

            # Recuperar mensaje cifrado
            mensaje_cifrado = mensaje["data"]

            # ==========================================
            # GUARDAR MENSAJE EN ARCHIVO TXT
            # ==========================================

            with open(
                ARCHIVO_SECRETO,
                "w",
                encoding="utf-8"
            ) as archivo:

                archivo.write(mensaje_cifrado)

            # ==========================================
            # MOSTRAR RESULTADO
            # ==========================================

            print("===================================")

            print("Mensaje secreto recibido")

            print(f"Tópico: {TOPICO}")

            print(f"Archivo generado: {ARCHIVO_SECRETO}")

            print("Mensaje guardado correctamente")

            print("===================================")

            print()

            # Finalizar después de recibir un mensaje
            break


except KeyboardInterrupt:

    print("\nConsumidor finalizado.")


finally:

    pubsub.close()
    r.close()

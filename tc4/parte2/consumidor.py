
import redis

# ==========================================
# CONFIGURACIÓN
# ==========================================

# URL de conexión a Upstash Redis
REDIS_URL = "rediss://default:TU_PASSWORD@TU_HOST.upstash.io:6379"

# Tópico al que se suscribe
TOPICO = "codigo_compañero"


# ==========================================
# CONEXIÓN A REDIS
# ==========================================

r = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
    )


# ==========================================
# SUSCRIPTOR
# ==========================================

pubsub = r.pubsub()

print("===================================")
print("SUSCRIPTOR REDIS PUB/SUB")
print("===================================")

print(f"Escuchando tópico: {TOPICO}")
print("Esperando mensajes...")
print("Presiona Ctrl+C para finalizar.")
print()

try:

    # Suscribirse al tópico
    pubsub.subscribe(TOPICO)

    # Escuchar mensajes
    for mensaje in pubsub.listen():

        if mensaje["type"] == "message":

            print(
                f"Mensaje recibido: {mensaje['data']}"
            )

except KeyboardInterrupt:

    print("\nSuscriptor finalizado.")

finally:

    pubsub.close()
    r.close()

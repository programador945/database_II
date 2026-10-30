
import redis

# ==========================================
# CONFIGURACIÓN
# ==========================================

# URL de conexión a Upstash Redis
REDIS_URL = "rediss://default:TU_PASSWORD@TU_HOST.upstash.io:6379"

# Tópico donde se publicarán los mensajes
TOPICO = "su_codigo"


# ==========================================
# CONEXIÓN A REDIS
# ==========================================

r = redis.Redis.from_url(REDIS_URL)


# ==========================================
# PRODUCTOR
# ==========================================

print("===================================")
print("PRODUCTOR REDIS PUB/SUB")
print("===================================")

print(f"Tópico: {TOPICO}")
print("Escribe 'salir' para finalizar.")
print()

try:

    while True:

        mensaje = input("Mensaje a enviar: ")

        if mensaje.lower() == "salir":
            break

        if mensaje.strip() == "":
            print("El mensaje no puede estar vacío.")
            continue

        # Publicar mensaje
        resultado = r.publish(
            TOPICO,
            mensaje
        )

        print(f"Mensaje enviado: {mensaje}")
        print(f"Suscriptores que lo recibieron: {resultado}")
        print()

except KeyboardInterrupt:

    print("\nProductor finalizado.")

finally:

    r.close()


from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generar_clave(nombre):

    # Generar clave RSA de 2048 bits
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    # Guardar clave privada
    with open(f"{nombre}_private.pem", "wb") as archivo:

        archivo.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Guardar clave pública
    with open(f"{nombre}_public.pem", "wb") as archivo:

        archivo.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print(f"Claves generadas para: {nombre}")

# Generar claves del estudiante
generar_clave("estudiante")

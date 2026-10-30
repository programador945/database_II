
import hashlib

# ==========================================
# CONFIGURACIÓN
# ==========================================

# Los estudiantes solo modifican estos nombres
ARCHIVO_ORIGINAL = "image.jpg"
ARCHIVO_DESCARGADO = "recuperada.jpg"


# ==========================================
# FUNCIÓN PARA CALCULAR SHA-256
# ==========================================

def calcular_hash(nombre_archivo):

    sha256 = hashlib.sha256()

    with open(nombre_archivo, "rb") as archivo:

        for bloque in iter(lambda: archivo.read(4096), b""):
            sha256.update(bloque)

    return sha256.hexdigest()


# ==========================================
# CALCULAR HASH DE LOS ARCHIVOS
# ==========================================

hash_original = calcular_hash(ARCHIVO_ORIGINAL)

hash_descargado = calcular_hash(ARCHIVO_DESCARGADO)


# ==========================================
# MOSTRAR RESULTADOS
# ==========================================

print("======================================")
print("COMPARACIÓN DE ARCHIVOS")
print("======================================")

print(f"Archivo original:    {ARCHIVO_ORIGINAL}")
print(f"Hash SHA-256:       {hash_original}")

print()

print(f"Archivo descargado: {ARCHIVO_DESCARGADO}")
print(f"Hash SHA-256:       {hash_descargado}")

print()
print("======================================")


# ==========================================
# COMPARAR HASHES
# ==========================================

if hash_original == hash_descargado:

    print("RESULTADO: ARCHIVOS IDENTICOS")
    print("Los hashes SHA-256 coinciden.")

else:

    print("RESULTADO: ARCHIVOS DIFERENTES")
    print("Los hashes SHA-256 no coinciden.")

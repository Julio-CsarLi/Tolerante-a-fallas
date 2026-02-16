import pickle
import os

ejemplo = "estado.pkl"

# Si el archivo existe, cargar el número guardado
if os.path.exists(ejemplo):
    with open(ejemplo, "rb") as f:
        numero = pickle.load(f)
else:
    numero = 0  # valor inicial

print("Valor actual:", numero)

# Incrementar el número
numero += 5

# Guardar el nuevo valor
with open(ejemplo, "wb") as f:
    pickle.dump(numero, f)

print("Nuevo valor guardado:", numero)
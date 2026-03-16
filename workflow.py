# lista de datos
datos = list(range(1, 101))

# procesar los datos
def filtrar_pares(lista):
    resultado = []
    
    for numero in lista:
        if numero % 2 == 0:
            resultado.append(numero)
    
    return resultado

# ejecutar procesamiento
resultado = filtrar_pares(datos)

# mostrar resultados
print("Datos originales:", datos)
print("Numeros pares:", resultado)
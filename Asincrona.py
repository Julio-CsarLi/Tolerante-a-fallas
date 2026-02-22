import asyncio
import time

async def descargar(nombre):
    print(f"Iniciando descarga {nombre}")
    await asyncio.sleep(2)
    print(f"Descarga completada {nombre}")

async def main():
    inicio = time.time()

    await asyncio.gather(
        descargar("Archivo 1"),
        descargar("Archivo 2"),
        descargar("Archivo 3")
    )

    print("Tiempo total:", time.time() - inicio)

asyncio.run(main())
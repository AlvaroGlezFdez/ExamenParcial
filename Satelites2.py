# Vamos a usar un esquema de Producer-Consumer para resolverlo





import multiprocessing
import time
import random





# Esta sería la función del producer, actualizando la cola cuando llegue una imagen
def recibir_imagen(nombre, cola, lock):
    print(f"📥 {nombre} recibida")
    with lock: # Realmente no es necesario porque la cola es una estructura process-safe, entonces podría quitarlo sin problema 
        cola.put(nombre)
        print(f"📤 {nombre} añadida a la cola")



# Esta sería la función consumer
def procesar_imagen(nombre, cola, lock):
    recibir_imagen(nombre, cola, lock)

    for fase in range(1, 4):
        duracion = random.randint(1, 3)
        time.sleep(duracion)
        print(f"{nombre} terminó fase {fase} en {duracion} segundos")

    print(f"✅ {nombre} ha sido procesada y almacenada")




# Protegemos el código para que esta parte de aquí no sufra un bucle de creación infinita de procesos

if __name__ == '__main__':
    lock = multiprocessing.Lock()
    cola = multiprocessing.Queue()

    tiempo_limite = 20 # este tiempo se puede ajustar sin problema
    inicio = time.time()
    procesos = []
    contador = 1 # este contador llevará la cuenta de cuantos procesos se mandan



    while time.time() - inicio < tiempo_limite: # ponemos que se creen tantos procesos como puedan en un tiempo determinado
        nombre = f"Imagen {contador}"
        p = multiprocessing.Process(target=procesar_imagen, args=(nombre, cola, lock))
        p.start()
        procesos.append(p)
        print(f"🚀 Lanzando {nombre}")
        contador += 1
        time.sleep(random.uniform(0.5, 2))  # Simular llegada irregular

    for p in procesos:
        p.join()




    print("\n📦 Imágenes en la cola:") # imprimimos todas las imagenes que han llegado 
    while not cola.empty():
        print(f"- {cola.get()}")






"""
🛰️ SIMULADOR DE PROCESAMIENTO DE IMÁGENES EN PARALELO

🎯 OBJETIVO:
Simular un entorno distribuido donde se reciben imágenes de forma continua
durante un tiempo limitado (20 segundos) y cada una es procesada en paralelo.
Cada imagen pasa por 3 fases de procesamiento y se guarda en una base de datos
compartida (representada con una cola).

⚠️ PROBLEMAS ENCONTRADOS Y SOLUCIONES:

1. ❌ Deadlock por uso de Barrier:
   Queríamos usar una barrera para que los procesos se sincronizaran entre fases.
   Sin embargo, como los procesos se crean dinámicamente durante 20 segundos,
   no sabíamos cuántos habría en total. Esto hacía que muchos se quedaran esperando
   indefinidamente en la barrera sin que se completara nunca -> deadlock.

   ✅ Solución: eliminar la barrera. Dejar que cada proceso trabaje a su ritmo
   sin esperar a los demás.

2. 🔐 Exclusión mutua:
   Varios procesos acceden a la base de datos (cola) al mismo tiempo. 
   Aunque `multiprocessing.Queue()` ya es segura entre procesos, hemos añadido
   un `Lock()` como medida extra de seguridad y para demostrar conocimiento
   de los mecanismos de sincronización.

3. 🧠 División lógica Producer-Consumer:
   La función `recibir_imagen()` actúa como el productor: recibe la imagen
   y la guarda en la cola. La función `procesar_imagen()` actúa como consumidor:
   procesa la imagen en 3 fases y confirma su almacenamiento.

4. ⏱️ Control por tiempo:
   Usamos `time.time()` para limitar la creación de procesos a 20 segundos exactos.
   Esto simula la recepción de imágenes en tiempo real.
"""
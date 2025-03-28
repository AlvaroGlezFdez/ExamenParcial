# ExamenParcial


# Procesamiento de Imágenes en Paralelo

Este proyecto simula el procesamiento de imágenes captadas por un satélite utilizando programación paralela. El sistema está diseñado para recibir imágenes de forma continua durante un tiempo limitado y procesarlas de forma independiente en distintos procesos, simulando un entorno distribuido con múltiples núcleos.

## Descripción

El programa genera imágenes durante un periodo de 20 segundos. Cada imagen es tratada como una tarea independiente y se asigna a un proceso, el cual ejecuta tres fases de procesamiento. Cada fase simula una operación computacional mediante una espera aleatoria.

Una vez procesada, la imagen es registrada en una estructura compartida entre procesos, representada mediante una cola (`multiprocessing.Queue`).

El sistema garantiza que todas las imágenes sean procesadas sin interferencias, permitiendo que múltiples procesos trabajen de forma concurrente sin necesidad de sincronización adicional, ya que la cola utilizada ya es segura entre procesos.

## Estructura del código

- `recibir_imagen(nombre, cola)`: función que simula la recepción de la imagen y la añade a la cola.
- `procesar_imagen(nombre, cola)`: función que representa el procesamiento completo de la imagen (3 fases).
- En el bloque principal (`if __name__ == "__main__"`), se lanza un número indefinido de procesos mientras no se supere un límite de tiempo predefinido.

Cada proceso es autónomo: recibe, procesa y registra su propia imagen.

## Tecnologías utilizadas

- Python 3
- Módulo `multiprocessing` para la creación y coordinación de procesos
- `time` y `random` para la simulación de fases y tiempos variables de procesamiento

## Consideraciones

La cola compartida entre procesos (`multiprocessing.Queue`) se utiliza como almacenamiento temporal de los resultados. Esta estructura es segura para su uso en entornos con múltiples procesos concurrentes, por lo que no se requiere el uso adicional de mecanismos de sincronización como `Lock`.

Este enfoque permite simular de forma sencilla y eficaz un entorno donde se procesan datos de manera paralela con una carga de trabajo distribuida.


# Examen Final - Computación Gráfica y Multimedia

Este repositorio contiene la solución para el Examen Final, dividido en dos secciones principales: Procesamiento de Imágenes con Python y una Escena 3D interactiva con Three.js.

## Punto 1 – Python

En esta sección se realizó la carga, manipulación y análisis de una imagen digital de un **Ajolote** (*Ambystoma mexicanum*), una especie en vía de extinción. El objetivo fue explorar técnicas fundamentales de visión artificial utilizando librerías como `OpenCV`, `Matplotlib` y `Numpy`.

### Enfoque y Metodología

El flujo de trabajo implementado en el notebook `examen_final_python.ipynb` consistió en:

1.  **Carga y Visualización:** Se cargó la imagen original y se separaron sus canales RGB para analizar la contribución de color en las branquias y cuerpo del ajolote.
2.  **Filtrado:** Se aplicaron filtros de **Suavizado (Gaussian Blur)** para reducir ruido y **Detección de Bordes (Canny/Sobel)** para resaltar la estructura morfológica del animal.
3.  **Operaciones Morfológicas:** Sobre una versión binarizada de la imagen, se aplicaron transformaciones de **Dilatación** y **Erosión**. Estas operaciones permitieron modificar la estructura de los objetos segmentados, rellenando huecos o eliminando ruido visual pequeño respectivamente.
4.  **Animación:** Se generaron secuencias visuales (GIFs) para comparar dinámicamente el antes y el después de cada procesamiento.

### Resultados Visuales

**Comparación de Filtros (Suavizado y Bordes):**
El siguiente GIF muestra la transición entre la imagen original, el efecto de desenfoque y el realce de bordes.

**Comparación de Operaciones Morfológicas:**
Aquí se observa el efecto de las operaciones morfológicas sobre la máscara binaria del ajolote, contrastando la erosión y dilatación.


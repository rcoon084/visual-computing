# Taller 2 — Computación Visual & 3D

## Fecha

`2025-10-15`

## Resumen del Taller

Este taller integra conceptos fundamentales de **gráficos por computador en 3D y visión artificial** en una serie de ejercicios prácticos y autocontenidos. El objetivo es explorar desde la manipulación de jerarquías y transformaciones en escenas 3D hasta el procesamiento y análisis de imágenes con técnicas de visión por computador. Cada módulo aborda un tema específico, como rasterización, proyección de cámaras, segmentación de imágenes, análisis geométrico, convoluciones personalizadas y control por gestos, permitiendo una comprensión transversal de cómo se crean y se interpretan los mundos digitales.

Los ejercicios se pueden desarrollar utilizando una combinación de **Python con OpenCV y NumPy**, **Three.js con React Three Fiber** y/o **Unity (LTS)**.

## Ejercicios Realizados

### Ejercicio 1 — Árbol del Movimiento (Jerarquías y Transformaciones)


### Ejercicio 2 — Ojos Digitales (Filtros y Bordes con OpenCV)


### Ejercicio 3 — Segmentando el Mundo (Binarización y Contornos)
  - **Explicación:** Se implementó un pipeline en Python con OpenCV para segmentar formas geométricas. El proceso incluyó la comparación entre umbralización fija y adaptativa para binarizar la imagen, siendo la adaptativa más robusta. Posteriormente, se utilizó `findContours` para detectar cada forma, calcular sus propiedades (centroide, área, perímetro) y, como bonus, clasificarlas (triángulo, cuadrado, etc.) según el número de vértices obtenidos con `cv2.approxPolyDP`.
  - **Evidencia:** 
<div align="center">
  <img src="gifs/EvidenciaEjercicio3.gif" alt="imagen original → segmentada → contornos/centroides" width="800">
</div>

  - **Código Fuente:** ejercicios/03_segmentacion_umbral_contornos
  - **Comentarios Personales:** Este ejercicio fue clave para entender la segmentación. La superioridad de la umbralización adaptativa en condiciones de luz variables fue una lección importante. La capacidad de extraer datos cuantitativos y clasificar formas a partir de contornos me pareció una herramienta de visión artificial increíblemente potente y fundamental.

### Ejercicio 4 — Imagen = Matriz (Canales, Slicing, Histogramas)


### Ejercicio 5 — Rasterización desde Cero (Línea, Círculo, Triángulo)


### Ejercicio 6 — Análisis Geométrico (Centroide, Área, Perímetro)


### Ejercicio 7 — Importando el Mundo (OBJ/STL/GLTF)
  - **Explicación:** Se desarrolló una aplicación dual para comparar los formatos 3D OBJ, STL y GLTF. Primero, un script de Python con `trimesh` se usó para analizar y convertir un modelo base a los tres formatos. Segundo, se construyó un visualizador web interactivo con Three.js y React (R3F) que permite cargar y alternar entre los modelos para observar directamente las diferencias en materiales, texturas y optimización.
  - **Evidencia:** 

<table>
  <thead>
    <tr>
      <th>Característica</th>
      <th><strong>OBJ (.obj)</strong></th>
      <th><strong>STL (.stl)</strong></th>
      <th><strong>GLTF/GLB (.glb)</strong></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Contenido</strong></td>
      <td>Geometría (vértices, normales, UVs), materiales externos.</td>
      <td><strong>Solo geometría</strong> de triángulos, sin color ni materiales.</td>
      <td>Escena completa: mallas, materiales PBR, texturas, animaciones.</td>
    </tr>
    <tr>
      <td><strong>Materiales</strong></td>
      <td>Sí, a través de un archivo <code>.mtl</code> separado.</td>
      <td><strong>No</strong>. Se renderiza con un color sólido por defecto.</td>
      <td><strong>Sí</strong>, soporte nativo y avanzado, todo empaquetado en un solo archivo <code>.glb</code>.</td>
    </tr>
    <tr>
      <td><strong>Uso Principal</strong></td>
      <td>Intercambio entre software de modelado (Blender, Maya).</td>
      <td><strong>Impresión 3D</strong>, prototipado rápido.</td>
      <td><strong>Web, AR/VR</strong>. Es el "JPEG del 3D", optimizado para carga rápida en tiempo real.</td>
    </tr>
    <tr>
      <td><strong>Eficiencia Web</strong></td>
      <td>Ineficiente. Múltiples peticiones (obj, mtl, texturas).</td>
      <td>Ineficiente para visualización (falta de datos visuales).</td>
      <td><strong>Altamente eficiente</strong>. Binario, comprimido y diseñado para carga rápida en la GPU.</td>
    </tr>
  </tbody>
</table>

<div align="center">
  <img src="gifs/EvidenciaEjercicio7.gif" alt="GIF con el selector de formato" width="800">
</div>

  - **Código Fuente:** /ejercicios/07_conversion_formatos_3d/
  - **Comentarios Personales:** Fue muy revelador ver en la práctica por qué **GLTF** es el estándar para la web: es eficiente y autocontenido. **STL** demostró su propósito para geometría pura (impresión 3D) al perder toda la información visual, mientras que **OBJ** funciona como un intermediario universal pero menos optimizado. Este ejercicio solidificó mi criterio para elegir el formato correcto según el caso de uso.

### Ejercicio 8 — Escenas Paramétricas (Objetos desde Datos)


### Ejercicio 9 — Filtro Visual (Convoluciones Personalizadas)


### Ejercicio 10 — Explorando el Color (RGB, HSV, CIE Lab + Simulaciones)


### Ejercicio 11 — Proyecciones 3D (Perspectiva vs Ortográfica)
  - **Explicación:** Se construyó una escena interactiva en Three.js para comparar las proyecciones de cámara. La aplicación permite al usuario alternar en tiempo real entre una **cámara de perspectiva**, que simula la visión humana con distorsión de profundidad, y una **cámara ortográfica**, que la elimina por completo. Una UI con sliders permite manipular los parámetros clave de cada una (FOV y Zoom) para observar su efecto en la percepción de la escala y la distancia.
  - **Evidencia:** 
  <div align="center">
  <img src="gifs/EvidenciaEjercicio11.gif" alt="GIF alternando modo de cámara y variando parámetros" width="800">
</div>

  - **Código Fuente:** /ejercicios/11_proyecciones_camara/
  - **Comentarios Personales:** La lección más impactante fue entender que la elección de la cámara no es una decisión técnica, sino una de diseño que define por completo la percepción del usuario. Este ejercicio práctico hizo tangible la diferencia entre crear una experiencia inmersiva y cinemática (perspectiva) versus una representación técnica y precisa (ortográfica).

### Ejercicio 12 — Gestos con Webcam (MediaPipe Hands)


-----

## Dependencias y Cómo Ejecutar

### Python (Ejercicios 2, 3, 4, 5, 6, 8, 9, 10, 12)

1.  **Clonar el repositorio:** `git clone https://github.com/tu_usuario/tu_repo.git`
2.  **Crear entorno virtual:** `python -m venv venv` y activarlo `source venv/bin/activate`.
3.  **Instalar dependencias:** `pip install -r requirements.txt` (debería incluir `opencv-python`, `numpy`, `matplotlib`, `mediapipe`, etc.).
4.  **Ejecutar:** `jupyter notebook` o `python nombre_del_script.py`.

### Three.js + React Three Fiber (Ejercicios 1, 7, 8, 11)

1.  **Navegar a la carpeta:** `cd ejercicios/XX_nombre_ejercicio/threejs/`
2.  **Instalar dependencias:** `npm install`
3.  **Iniciar servidor:** `npm run dev`

### Unity (Ejercicios 1, 8, 10, 11)

1.  Abrir **Unity Hub** y seleccionar **"Add project from disk"**.
2.  Navegar a la carpeta del ejercicio correspondiente (ej. `/ejercicios/01_jerarquias_transformaciones/unity/`).
3.  Abrir el proyecto, cargar la escena principal y presionar **Play**.

-----

## Estructura del Repositorio

```
yyyy-mm-dd_taller_cv_3d/
├── ejercicios/
│   ├── 01_jerarquias_transformaciones/
│   ├── 02_ojos_digitales_opencv/
│   ├── 03_segmentacion_umbral_contornos/
│   ├── 04_imagen_matriz_pixeles/
│   ├── 05_rasterizacion_clasica/
│   ├── 06_analisis_figuras_geometricas/
│   ├── 07_conversion_formatos_3d/
│   ├── 08_escenas_parametricas/
│   ├── 09_convoluciones_personalizadas/
│   ├── 10_modelos_color_percepcion/
│   ├── 11_proyecciones_camara/
│   └── 12_gestos_webcam_mediapipe/
├── assets/
├── gifs/
└── README.md
```

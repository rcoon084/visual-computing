
# Taller 4 — Taller Integral de Computación Visual Avanzada

## Fecha

`2025-12-03`

# Subsistema 1: Visualización 3D Optimizada y Realidad Aumentada

## Descripción del Proyecto

Este subsistema constituye el módulo encargado de la **percepción visual** dentro del proyecto de Computación Visual Avanzada. Su función es capturar video en tiempo real y ejecutar:

1. **Detección de objetos** mediante YOLOv8/YOLOv9.  
2. **Segmentación de instancias** utilizando modelos "-seg".  
3. **Representación visual estilizada** mediante un HUD moderno.  
4. **Exportación estructurada** en formato JSON para consumo de otros subsistemas.

Este módulo funciona de manera **totalmente autónoma**, independiente del resto del pipeline.

---

## Stack Tecnológico

- **Visión por Computador:** Ultralytics YOLO (v8+)
- **Segmentación:** YOLO-Seg (Modelos Nano/Small)
- **Procesamiento de Video:** OpenCV
- **Serialización:** JSON
- **Interfaz HUD:** Overlays con OpenCV
- **Lenguaje:** Python 3.10+

---

## Funcionalidades Clave

### A. Detección en Tiempo Real (YOLO)
El sistema realiza detección de múltiples objetos en la escena:
- Soporte para 80 clases del dataset COCO.
- Visualización con colores consistentes y tipografía limpia.
- Detecciones en tiempo real con webcam.

### B. Segmentación de Instancias (YOLO-Seg)
El sistema puede segmentar objetos:
- Máscaras por instancia.
- Polígonos representados en arrays.
- Exportación a JSON por cada fotograma.

### C. Interfaz Visual Optimizada (HUD)
Interfaz moderna tipo panel lateral:
- FPS en tiempo real.
- Número de objetos detectados.
- Clase y confianza del primer objeto.
- Caja semi–transparente estilo "Cyber HUD".

### D. Exportación de Datos (JSON)
Cada fotograma genera un archivo JSON con:
- Bounding boxes.
- Clase.
- Confianza.
- Máscara segmentada.

Estos archivos pueden ser consumidos por sistemas de visualización o dashboards.
---
## Instrucciones de Ejecución

### 1. Prerrequisitos
- Python 3.10 o superior
- Webcam

### 2. Instalar dependencias
```
pip install -r requirements.txt
```

### 3. Ejecutar el subsistema
```
python main.py
```

### 4. Resultados generados
- `results/detections/` — imágenes anotadas
- `results/json/` — detecciones en formato JSON

---

## Métricas de Rendimiento

| Métrica | Valor esperado |
|--------|----------------|
| FPS Promedio | 15–30 FPS |
| Latencia por frame | 30–80 ms |
| Clases detectadas | 80 (COCO) |
| Resolución | 640×480 |

Se recomienda analizar:
- Variación de FPS según resolución.
- Objetos detectados por frame.
- Tiempos de inferencia promedio.

---

## Evidencias

**Fig 1. HUD de detección y segmentación**

![alt text](../results/2_Modelado_procedural_desde_codigo.gif)


---

# **Subsistema 2: Control multimodal (voz + gestos + EEG)**

## **Descripción**

Este subsistema integra **entrada de voz**, **detección de gestos**, **simulación de señales EEG** y **visualización interactiva** en una única interfaz gráfica permitiendo controlar acciones visuales aplicadas sobre una cámara en vivo usando diferentes modalidades sensoriales:

* **Voz ( utilizando Vosk)**
* **Gestos de manos ( con MediaPipe)**
* **Señales EEG simuladas (a tráves NumPy)**
* **Fusión multimodal** para activar filtros visuales específicos

El resultado es un panel único donde se procesa video, se reconocen comandos y se aplican filtros visuales.

## **Componentes Principales**

### **1.  Reconocimiento de Voz**

El subsistema usa **Vosk** para recibir comandos hablados sin conexión a internet.

- **Flujo**:

1. Captura audio usando **sounddevice** con el sample rate recomendado por el modelo.
2. Envía los buffers al modelo Vosk (Recognizer).
3. Cuando detecta palabras clave, activa acciones visuales:

| Comando        | Acción                                     |
| -------------- | ------------------------------------------ |
| “ROJO o AZUL”       | Activa el filtro del color correspondiente            |
| “ACERCAR o ALEJAR” | Hace que la camara se acerque o se aleje |
| "CONFETI"         | Hace que aparezca confeti en la camara                               |

#### Ventajas:

* Baja latencia
* Integración sencilla

#### **Evidencia:**
<video controls src="python/subsistema_2/VOZ.mp4" title="VOZ"></video>

---

### **2. Detección de Gestos con MediaPipe Hands**

Se usa **MediaPipe Hands** para detectar la mano y clasificar dos gestos básicos:

| Gesto          | Detección                  | Acción          |
| -------------- | -------------------------- | --------------- |
| ✋ Mano abierta | Todos los dedos extendidos | Genera luces de "fiesta" |
| 👊 Puño        | Ningún dedo extendido      | Prende o apaga la luz (baja el brillo)  |
| ✌️ paz        | Dedo indice y anular extendidos      | Filtro B/N, Sepia o bordes  |

El gesto solo se activa cuando permanece **estable por un número de frames**, evitando cambios rápidos.

#### **Evidencia:**
<video controls src="python/subsistema_2/GESTOS.mp4" title="GESTOS"></video>


---

### **3. Simulación de Señales EEG**

El subsistema simula un EEG usando ondas sintéticas:

* Onda base tipo alfa (8-12 Hz)
* Ruido blanco añadido
* Valores normalizados entre −1 y 1

### **Umbrales configurados:**

* **EEG alto (> 0.6)** → Activa el modo “fusión”


### **🧩 Fusión Multimodal**


Si el umbral es mayor a 0.6, el sistema combina entradas de:

* Voz
* Gestos
* EEG

Para decidir *qué acción final aplicar*.
Tiene prioridad definida:

1. **Comandos de voz**
2. **Gestos**
3. **EEG**

Esto evita conflictos entre fuentes.

#### **Ejemplo:**

- **EEG** > 0.6, AGREGA LUCES INTENSIFICADAS A LOZ GESTOS Y VOZ YA DETERMINADOS

#### **Evidencia:**
<video controls src="python/subsistema_2/GESTOS+VOZ+EEG.mp4" title="GESTOS+VOZ+EEG"></video>

### **Conclusiones**

Este subsistema proporciona:

* Integración real de **voz + gestos + EEG**
* Una sola interfaz unificada
* Efectos visuales animados
* Procesamiento en tiempo real
* Arquitectura modular

Ideal para proyectos de interacción humano-máquina, realidad aumentada y prototipos con entradas no convencionales.


# Subsistema 3: Visualización 3D Optimizada y Realidad Aumentada
##  Descripción del Proyecto

Este subsistema es el módulo encargado de la **representación visual y experiencial** dentro del proyecto de Computación Visual Avanzada. Su objetivo es recibir datos (simulados o reales) de detección y transformarlos en una experiencia gráfica inmersiva de alto rendimiento.

El sistema implementa dos modalidades de visualización:

1.  **Modo Escena Web (Three.js):** Un entorno 3D "Cyberpunk" optimizado mediante técnicas de Nivel de Detalle (LOD) y sombras dinámicas.
2.  **Modo Realidad Aumentada (AR.js):** Visualización sobre marcadores físicos (Hiro) con lógica de optimización de distancia personalizada.

## Stack Tecnológico

  * **Motor Gráfico:** Three.js (r150+)
  * **Realidad Aumentada:** AR.js + A-Frame
  * **Entorno de Desarrollo:** Vite (Vanilla JS)
  * **Optimización:** GLTFLoader + THREE.LOD
  * **Interfaz de Control:** Lil-gui (Simulación de inputs externos)
  * **Métricas:** Stats.js

## Funcionalidades Clave (Entregables)

### A. Optimización Visual (LOD - Level of Detail)

Implementación de carga dinámica de geometría para mantener **60 FPS** estables.

  * **High Poly (.gltf):** Se carga cuando la cámara está a \< 25 metros. Incluye sombras suaves y materiales complejos.
  * **Low Poly (.glb):** Se carga cuando la cámara está a \> 25 metros. Geometría simplificada al 10% y wireframe de depuración (opcional).

### B. Interacción Simulada (GUI)

Debido a la arquitectura de subsistemas independientes, se implementó un panel de control (`lil-gui`) que simula la recepción de WebSockets del Subsistema 1 (Detección) y 2 (Control):

  * **Simulación de Gesto:** Escala el modelo en tiempo real.
  * **Simulación de Entorno:** Cambia la iluminación (Modo Día/Noche).

### C. Realidad Aumentada (AR Web)

Módulo independiente accesible vía `ar.html`.

  * Detección de marcador **Hiro**.
  * Script personalizado `lod-control` que calcula la distancia euclidiana entre la cámara y el marcador para intercambiar modelos High/Low en tiempo real.

##  Instrucciones de Ejecución

### Prerrequisitos

  * Node.js (v14 o superior)
  * Navegador con soporte WebGL (Chrome/Firefox recomendado)
  * Webcam (para módulo AR)

### Pasos

1.  **Instalar dependencias:**

    ```bash
    cd threejs
    npm install
    ```

2.  **Iniciar servidor de desarrollo:**

    ```bash
    npm run dev
    ```

3.  **Visualizar:**

      * **Escena 3D:** Abrir `http://localhost:5173/`
      * **Realidad Aumentada:** Abrir `http://localhost:5173/ar.html` (Requiere mostrar el marcador Hiro a la cámara).

## Métricas de Rendimiento

  * **FPS Promedio:** 60 FPS (Estables).
  * **Draw Calls:** \< 50 en escena Low Poly.
  * **Tiempo de carga:** \< 2s (Modelos optimizados).

## Evidencias

<p align="center">
  <strong>Fig 1. Respuesta a Eventos Simulados (GUI)</strong>
</p>

<p align="center">
  <img src="../results/sim_event_response_gui.gif" width="100%" alt="Event Response GIF">
</p>

<br> <p align="center">
  <strong>Fig 2. Test de Tracking en Realidad Aumentada</strong>
</p>

<p align="center">
  <img src="../results/ar_hiro_marker_detection.gif" width="100%" alt="AR Tracking GIF">
</p>

# Subsistema 4: Control por Voz (Reconocimiento y Comandos)

## Descripción del Proyecto

El Subsistema 4 es el módulo responsable del **control por voz** dentro del proyecto de Computación Visual Avanzada. Su función es interpretar comandos hablados en español y convertirlos en **eventos estructurados (JSON)** que pueden ser utilizados por otros subsistemas como:

- Visualización 3D (Subsistema 3)
- Detección (Subsistema 1)
- Gestos (Subsistema 2)
- Dashboards

El sistema reconoce palabras clave, ejecuta acciones internas, responde con voz sintetizada y genera archivos JSON en tiempo real con el comando detectado.

Este subsistema está diseñado para ser **autónomo**, simple y de alto rendimiento.

---

## Stack Tecnológico

**Actualización:** Ahora incluye interfaz gráfica (Tkinter) y soporte multihilo.

- **Reconocimiento de Voz:** SpeechRecognition
- **Entrada de Audio:** PyAudio
- **Síntesis de Voz:** pyttsx3
- **Serialización:** JSON
- **Lenguaje:** Python 3.10+

---

## Funcionalidades Clave

### A. Reconocimiento de Voz
El sistema escucha el micrófono y procesa comandos en español usando el motor de Google Speech.

- Captura en tiempo real
- Detección continua
- Normalización automática del audio

### B. Comandos Inteligentes
El subsistema reconoce palabras clave como:

| Palabra detectada | Acción JSON |
|------------------|-------------|
| luz, iluminar | change_light |
| rotar, girar | rotate_model |
| escala | scale_model |
| aumentar | scale_up |
| disminuir | scale_down |
| color | change_color |

Estos comandos pueden ser ampliados según las necesidades del proyecto.

### C. Respuesta por Voz (TTS)
El sistema confirma el comando reconocido:

> "Comando recibido: rotate model"

### D. Exportación de Datos (JSON)
Cada comando detectado se exporta como:

```json
{
    "timestamp": 1701546541.554,
    "command": "rotate_model"
}
```

Archivo generado en:
```
results/last_command.json
```
---

## Interfaz Gráfica (Tkinter)

El subsistema ahora incluye una **interfaz gráfica sencilla y funcional**, desarrollada con Tkinter.

### Características:
- Ventana con modo oscuro.
- Estados: **Inactivo / Escuchando**.
- Historial de comandos detectados.
- Botones *Iniciar* y *Detener* escucha.
- Exportación JSON inmediata.

### Ejecución de la interfaz

```
python Submodulo_4.py

```

## Instrucciones de Ejecución

### 1. Prerrequisitos
- Python 3.10+
- Micrófono funcional
- pip actualizado

### 2. Instalar dependencias
```
pip install -r requirements.txt
```

### 3. Ejecutar el Subsistema
```
python main.py
```

Cuando esté activo, el programa mostrará:

```
Escuchando...
```

Di un comando como:
- "rotar"
- "luz"
- "cambiar color"

### 4. Salir del programa
Presiona **CTRL + C**.

---

## Evidencias

### **Fig 1. Reconocimiento de voz y respuesta por consola**

![alt text](../results/4_evidencia_audio.gif)

---

## Estado del Subsistema

**Subsistema completado – Autónomo – Totalmente integrable con otros módulos.**

Compatible con:
- Control de escenas 3D
- Sistemas basados en WebSockets
- Sistemas de interacción multimodal
- Dashboards Python
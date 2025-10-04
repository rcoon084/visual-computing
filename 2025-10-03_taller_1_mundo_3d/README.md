# Taller 1: Escena Natural con Iluminación Dinámica en Three.js

## Mi Mundo Virtual: Refugio en el Bosque al Atardecer

### Breve Explicación del Mundo
Este proyecto es una representación estilizada de un refugio sereno en la naturaleza. La escena se compone de una cabaña de madera situada en un claro del bosque, junto a una fogata crepitante y rodeada de vegetación. El objetivo principal del taller fue explorar cómo la **iluminación, los materiales y el color** interactúan para transformar por completo la atmósfera de un mundo virtual, pasando de un día apacible a un atardecer mágico.

La escena también incluye elementos procedurales que demuestran la generación de texturas mediante código, integrándose de forma coherente con los modelos 3D y la paleta de colores definida.

---

### 1. Modelos GLB Usados
Se utilizaron tres modelos principales para dar vida a la escena, cada uno representando una categoría distinta:

* **Modelo Arquitectónico:**
    * **Nombre:** `Log cabin.glb` (Cabaña de madera).
    * **Fuente:** Obtenido de una librería de assets 3D.
    * **Modificaciones:** El modelo fue escalado a `0.08` para ajustarse a la escala de la escena, posicionado en el centro visual y rotado `7` radianes en el eje Y para ofrecer una vista atractiva desde la cámara inicial.

* **Modelo Orgánico:**
    * **Nombre:** `Nature.glb` (Conjunto de árboles y arbustos).
    * **Fuente:** Obtenido de una librería de assets 3D.
    * **Modificaciones:** Se escaló al doble de su tamaño (`2.0`) para crear un entorno boscoso denso que enmarque la cabaña y los demás elementos.

* **Modelo Utilitario:**
    * **Nombre:** `Camp fire.glb` (Fogata).
    * **Fuente:** Obtenido de una librería de assets 3D.
    * **Modificaciones:** Se escaló a un tamaño muy reducido (`0.002`) para ajustarse a las proporciones de la escena. Se instanciaron dos fogatas para añadir más puntos de interés lumínico.

---

### 2. Iluminación
El esquema de iluminación es el corazón de este proyecto y está diseñado para ser dinámico y transformador. Se basa en un sistema de tres puntos con dos presets intercambiables.

* **Key Light (Luz Principal):** Una `DirectionalLight` que actúa como el sol. Es la principal fuente de luz y la única que proyecta sombras (`castShadow = true`) para maximizar el rendimiento. Su posición es animada para simular el paso del tiempo.
* **Fill Light (Luz de Relleno):** Una `DirectionalLight` de baja intensidad y color complementario, cuya función es suavizar las sombras y añadir un tinte de color ambiental.
* **Rim Light (Luz de Contorno):** Una `DirectionalLight` posicionada detrás de la escena para crear un contorno de luz en los objetos, ayudando a separarlos del fondo.
* **Luz Ambiental:** Una `AmbientLight` que proporciona una iluminación base global, asegurando que ninguna parte de la escena quede en oscuridad absoluta.

#### Presets de Iluminación
Se puede alternar entre dos ambientes presionando las teclas `1` y `2`:

* **Preset "Día" (Tecla 1):** Simula la luz de un día soleado. Utiliza un color de sol amarillo (`#edcf58`) y un relleno azul claro (`#71dece`). El cielo es una textura diurna brillante.
* **Preset "Atardecer" (Tecla 2):** Simula la luz cálida de una puesta de sol. El sol adquiere un tono naranja intenso (`#de9937`) y el relleno un azul acero (`#4682b4`). El cielo cambia a una textura de atardecer, sincronizándose con la iluminación.

---

### 3. Materiales y Texturas PBR
Los materiales fueron un foco central para observar la interacción con la luz.

* **Material de la Cabaña:** Se asignó un `MeshStandardMaterial` a la cabaña con una textura de tablones de madera (`dark_planks_diff_2k.jpg`) en su canal de color (`.map`). Se ajustó el `roughness` a `1.0` para darle un aspecto mate y rústico, propio de la madera sin tratar.
* **Skydome (Cielo):** Se utilizó un `MeshBasicMaterial` para el cielo, ya que no debe ser afectado por las luces de la escena. La propiedad `.side` se estableció en `THREE.BackSide` para que la textura se proyectara en el interior de una esfera gigante que envuelve el mundo. La textura del mapa (`.map`) cambia dinámicamente con los presets de iluminación.

---

### 4. Shaders Procedurales
Para cumplir con los requisitos del taller, se generaron dos texturas mediante código utilizando la API de Canvas.

* **Tipo 1: Damero (Checkerboard)**
    * **Aplicado a:** El suelo de toda la escena.
    * **Parámetros:** Se generó un patrón de 10x10 celdas con dos tonos de verde bosque (`#4a5d23`, `#3a4a13`). La textura se repite 20x20 veces sobre el plano del suelo para crear una superficie densa y estilizada.
    * **Justificación:** Se usó para crear un suelo cohesivo que no distrajera de los modelos principales y para demostrar cómo una textura generada por código puede establecer la base visual de un entorno grande.

* **Tipo 2: Bandas Verticales (Stripes)**
    * **Aplicado a:** Un cilindro (tótem procedural) colocado en la escena.
    * **Parámetros:** Se generó una textura de bandas verticales utilizando tres de los cuatro colores de la paleta principal del proyecto (`#4a5d23`, `#C5C6C7`, `#1e2a3a`).
    * **Justificación:** Este objeto actúa como una "muestra de color" viviente, demostrando la paleta cromática del mundo. Su material tiene un `metalness` de `0.7` para mostrar cómo los reflejos de la luz animada interactúan con los colores de la paleta sobre una superficie procedural.

---

### 5. Cámaras
Se configuraron dos cámaras para ofrecer perspectivas únicas del mundo virtual, alternando entre ellas con la tecla `C`.

* **Cámara en Perspectiva:** La vista principal, inmersiva y cinematográfica. Está configurada con una animación sutil, un lento paneo circular que "respira" alrededor de la escena, ideal para la grabación de video y para apreciar la profundidad y los efectos de luz en los materiales.
* **Cámara Ortográfica:** Ofrece una vista isométrica, similar a la de una maqueta o un videojuego de estrategia. Es perfecta para observar la composición espacial de la escena sin la distorsión de la perspectiva, destacando la distribución de los elementos.

---

### 6. Animaciones
Se implementaron tres tipos de animación para dar vida a la escena:

* **Animación de Luz:** La `keyLight` (sol) orbita constantemente la escena siguiendo una trayectoria circular. Esto crea un ciclo dinámico de luces y sombras que se desplazan sobre el terreno y los modelos, resaltando las texturas y los relieves.
* **Animación de Objeto:** El tótem procedural rota lentamente sobre su eje Y, permitiendo ver cómo la luz incide en sus diferentes caras y colores a lo largo del tiempo.
* **Animación de Cámara:** La cámara en perspectiva tiene un movimiento sutil y continuo, orbitando suavemente alrededor de su posición inicial. Esto evita una vista estática y añade un toque profesional al recorrido visual.

---

### 7. Modelo de Color
La paleta de colores fue cuidadosamente seleccionada para evocar una sensación de naturaleza y misterio.

* **Paleta Definida (RGB/HEX):**
    * `#1E2A3A` (Azul Noche - Color de ambiente/sombras)
    * `#4A5D23` (Verde Musgo - Color principal de la naturaleza)
    * `#C5C6C7` (Plata - Detalles y rocas)
    * `#FF6700` (Naranja Fuego - Color de acento)

* **Justificación de Contraste (CIELAB):**
    Se utilizó una base de colores análogos fríos y de baja saturación (azul y verde) para crear una atmósfera tranquila. Para asegurar que la fogata fuera el punto focal indiscutible, se eligió un **naranja brillante (`#FF6700`)** como acento. Desde la perspectiva de **CIELAB**, este color tiene una alta **luminosidad (L\*)** y un fuerte componente en el eje **a\* (rojo)**, creando un contraste perceptual máximo tanto en brillo como en cromaticidad contra el fondo azul/verde. Esto dirige la atención del espectador de forma natural hacia el punto más cálido de la escena.

---

### Capturas de Pantalla y Video

*(Aquí deberías insertar tus imágenes y un GIF animado o video)*

**Vista en Perspectiva (Preset "Día")**
`![Vista de Día](renders/captura_dia.png)`

**Vista en Perspectiva (Preset "Atardecer")**
`![Vista de Atardecer](renders/captura_atardecer.png)`

**Vista Ortográfica**
`![Vista Ortográfica](renders/captura_ortografica.png)`

**Demostración Animada**
`![GIF de la escena animada](renders/escena_animada.gif)`
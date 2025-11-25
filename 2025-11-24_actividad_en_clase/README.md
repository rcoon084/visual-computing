# Algoritmos Fundamentales para Realidad Aumentada y Construcción 3D

Este documento presenta un resumen individual de los tres algoritmos fundamentales seleccionados para la actividad, detallando el problema que resuelven, su flujo de operación y sus ventajas comparativas.

---

## 1. Algoritmo de Proyección Equirectangular (ERP)
Este algoritmo es el estándar universal para la representación de imágenes 360 en superficies planas.

### Problema a resolver
El desafío fundamental es representar una esfera visual completa en un formato digital plano compatible con pantallas rectangulares. Dado que el mundo es esférico y nuestras pantallas son planas, se necesita un método para desenrollar la esfera sin perder la información espacial.

### Flujo de Operación
![Flujo ERP](./Images/Diagrama%20de%20Proyección%20Equirectangular.png)
El proceso se basa en un modelo de cámara esférica ideal situado en el centro de una esfera de radio unitario ($r=1$):

1.  **Entrada:** Se recibe la información visual de un punto del entorno 3D mediante un rayo que intersecta la esfera.
2.  **Conversión de Coordenadas:** Se describe la dirección de cada rayo usando coordenadas esféricas: Azimut ($\theta$) para el ángulo horizontal y Elevación ($\varphi$) para el vertical.
3.  **Mapeo Directo:** El algoritmo asigna linealmente estas coordenadas a los ejes cartesianos de la imagen final:
    * El **Azimut ($\theta$)** se convierte en la posición en el **Eje X**.
    * La **Elevación ($\varphi$)** se convierte en la posición en el **Eje Y**.
4.  **Salida:** Se genera una imagen rectangular con una relación de aspecto 2:1.

### Ventajas frente a técnicas alternativas
* **Simplicidad y Compatibilidad Universal:** A diferencia de proyecciones más complejas (como la Cúbica), su mapeo directo $(X,Y)$ la hace compatible con la gran mayoría de software de edición, visores 360 y sistemas GIS como Google Street View.
* **Estandarización:** Es el formato "de facto" para almacenamiento e intercambio de video inmersivo, a pesar de sufrir mayor distorsión en los polos que otras técnicas.

---

## 2. Algoritmo de "Stitching" (Costura de Imágenes)
Es el proceso de software encargado de unificar múltiples vistas parciales para crear la ilusión de una esfera continua.

### Problema a resolver
Las cámaras 360 de consumo no capturan una esfera perfecta directamente. Utilizan dos lentes "ojo de pez" opuestos que generan dos imágenes hemisféricas separadas. El problema radica en **unir estas dos imágenes circulares disjuntas en una sola panorámica coherente** sin cortes visibles.

### Flujo de Operación 
![Flujo Stitching](./Images/Diagrama%20de%20Stitching.png)
1.  **Captura Dual:** Se obtienen dos imágenes circulares con un campo de visión (FOV) superior a 180, garantizando una zona de solapamiento entre ellas.
2.  **Análisis de Solapamiento:** El algoritmo identifica las áreas comunes compartidas por ambas lentes.
3.  **Corrección y Alineación:** Se corrigen las distorsiones ópticas de las lentes y se alinean las características visuales coincidentes en la zona de unión.
4.  **Fusión (Stitching):** El software "cose" digitalmente las fronteras para eliminar costuras visibles.
5.  **Proyección:** El resultado unificado se transforma al formato estándar (generalmente equirectangular).

### Ventajas frente a técnicas tradicionales
* **Automatización en Tiempo Real:** Frente a métodos antiguos que requerían unión manual o post-procesamiento pesado en PC, las cámaras modernas (ej. Ricoh Theta X) ejecutan este algoritmo internamente en tiempo real.
* **Eficiencia de Captura:** Permite capturar todo el entorno con un solo dispositivo compacto de dos lentes, en lugar de necesitar complejos "rigs" de múltiples cámaras convencionales que complican el proceso de sincronización y unión.

---

## 3. Algoritmo SLAM Visual (Enfoque Omnidireccional)

SLAM (Simultaneous Localization and Mapping) es el proceso mediante el cual una máquina construye un mapa y se ubica en él al mismo tiempo.

### Problema a resolver
Resuelve la "Paradoja de la Navegación Autónoma": Para mapear, un robot necesita saber dónde está; pero para saber dónde está, necesita un mapa previo. SLAM permite realizar ambas acciones desde cero en un entorno desconocido sin depender de GPS externo.

### Flujo de Operación 
![Flujo SLAM](./Images/Diagrama%20de%20SLAM%20Visual.png)
El sistema opera con dos procesos paralelos o "mentes":
1.  **Front-End (Odometría Visual):**
    * **Extracción:** Identifica puntos clave (features) usando algoritmos como ORB.
    * **Matching y Pose:** Rastrea estos puntos entre fotogramas para estimar el movimiento rápido de la cámara.
    * **Triangulación:** Calcula la profundidad para crear los primeros puntos 3D del mapa.
2.  **Back-End (Optimización Global):**
    * **Detección de Bucles:** Reconoce lugares previamente visitados (Loop Closure) para corregir errores acumulados (deriva).
    * **Optimización de Grafo:** Ajusta toda la trayectoria histórica para que sea consistente.
    * **Bundle Adjustment:** Refinamiento final de todos los puntos del mapa y poses de cámara.

### Ventajas frente a técnicas tradicionales (Cámaras Pinhole)
El uso de visión omnidireccional (360) en SLAM presenta ventajas estratégicas sobre las cámaras tradicionales de campo de visión limitado (Pinhole):
* **Eliminación de Puntos Ciegos:** Al ver todo el entorno a la vez, el sistema no pierde de vista referencias importantes al girar, lo que es común en cámaras tradicionales.
* **Mayor Robustez:** Detecta más puntos de referencia estables en cada fotograma, haciendo que el rastreo sea más difícil de perder.
* **Mejor Estimación de Movimiento:** La geometría esférica permite una odometría visual más precisa y fiable, reduciendo la deriva acumulada.
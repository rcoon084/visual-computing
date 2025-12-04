# Reporte de Métricas - Subsistema 3 (Visualización)

## 1. Optimización Visual (LOD)
Se implementó la técnica Level of Detail (LOD) para garantizar 60 FPS estables.

| Estado | Modelo | Polígonos (Triángulos) | Distancia de Activación |
|--------|--------|------------------------|-------------------------|
| Cerca | High Poly (.gltf) | ~25,000 tris | 0m - 15m |
| Lejos | Low Poly (.glb) | ~2,500 tris | > 15m |
| **Reducción** | | **90%** | |

## 2. Pruebas de Rendimiento
* **Hardware:** Ryzen 7
* **FPS Promedio:** 60 FPS
* **Draw Calls:** Reducidos mediante uso de materiales compartidos.

## 3. Simulación de Interacción
Debido a la modalidad de subsistemas independientes, se implementó un panel de control (GUI) para validar la respuesta visual ante eventos externos:
* Evento "Gesto Detectado": Escala del objeto (Feedback visual).
* Evento "Peligro": Cambio de color ambiental (Feedback de entorno).
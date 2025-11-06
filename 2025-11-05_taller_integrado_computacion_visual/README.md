# Comprehensive Visual Computing Workshop

## 1. Project Concept

This project serves as an integrated ecosystem where color, form, gesture, and sound can interact. The central goal is to articulate the full graphics pipeline—from PBR materials and custom shaders to projective mathematics—and connect it to natural human inputs.

The core experiment for points 1, 3, and 11, "The Mud Dog," explores the contrast between **low-poly** geometry and **Physically Based Rendering (PBR)**. This central object acts as a canvas, reacting dynamically to procedural generation, custom visual effects, and a suite of multimodal inputs including voice commands, real-time hand gestures, and simulated BCI signals. The objective is to create a clear, reproducible, and aesthetically grounded interactive experience.

## 2. Tools and Environment

* **Primary Engine:** Unity 2022.3.x (LTS) with Universal Render Pipeline (URP)
* **Scripting:** C# (for Unity) and Python (for multimodal input processing)
* **Libraries:**
  * **Python:** MediaPipe, SpeechRecognition, OpenCV, PyGame, NumPy, SciPy
  * **Unity:** Open Sound Control (OSC) for bridging Python and Unity
* **Shading:** Unity Shader Graph
* **Version Control:** Git / GitHub

## 3. Description of Applied Modules (A–K)

This section documents the techniques implemented for each activity in the workshop.

###  1. Materials, Light, and Color (PBR & Color Models)
* **Description:** This foundational section established the scene's base appearance.
  * **PBR Textures:** A PBR texture set (`Albedo`, `Normal Map (OpenGL)`, `Ambient Occlusion`) was applied to the low-poly dog model using the `URP/Lit` shader, allowing it to react realistically to light.
  * **Multiple Lighting:** The scene is lit using a 3-point scheme (Key, Fill, Rim) plus an HDRI skybox for global illumination and reflections.
  * **Cameras:** A C# script (`ControlCamaras.cs`) was implemented to toggle (with the 'C' key) between a `Perspective Camera` (standard 3D view) and an `Orthographic Camera` (2D view).
  * **Color Analysis (CIELAB):** A CIELAB analysis was performed, confirming a strong luminance contrast (**ΔL ≈ 28**) between the dark object (**L\* ≈ 32**) and the lighter background (**L\* ≈ 60**), ensuring scene readability.

---

### 2. Procedural Modeling from Code

---

###  3. Custom Shaders and Effects

* **Description:** Explored artistic and dynamic rendering by creating three custom shaders using Unity's Shader Graph.
    * **`ColorDinamico_Shader` (Unlit):** A dynamic shader that changes the object's color based on its **UV coordinates** (a vertical gradient) and **Time** (a pulsing sine wave).
    * **`Toon_Shader` (Unlit):** A non-photorealistic (NPR) shader that creates a cel-shaded "cartoon" look. It calculates light manually using `Dot Product` and a `Step` node to create hard bands of light and shadow.
    * **`Distortion_Shader` (Unlit):** An effect shader that creates a "mirage" or "underwater" effect. It uses animated `Simple Noise` to dynamically displace the texture's UV coordinates over time.


---

###  4. Dynamic Texturing and Particles
---

### 5. 360° Image and Video Visualization
---

### 6. Input and Interaction (UI, Input, Collisions)

---

### 7. Gestures with Webcam (MediaPipe Hands)

---

###  8. Voice Recognition and Command Control

---

###  9. Multimodal Interfaces (Voice + Gestures)
---

### 10. BCI Simulation (Synthetic EEG and Control)

---

### 11. Projective Spaces and Projection Matrices
* **Description:** This module was split into two parts: theory and practice, demonstrating how 3D is projected onto a 2D screen.
    * **Theory (Python):** Implemented orthographic and perspective projection matrices from scratch using NumPy. This demonstrated mathematically how homogeneous coordinates (specifically, dividing by the `w` component) create perspective, causing distant objects to appear smaller.
    * **Practice (Unity):** Created a "Depth Visualizer" shader (`Depth_Shader`) using Shader Graph. This `Unlit` shader uses the `Scene Depth` node to map distance (from near=black to far=white), visually demonstrating the Z-buffer.
    * **Integration:** The camera toggle script (from Point 1) was used to switch between perspective and orthographic cameras, showing how the depth visualization changes, which visually confirms the mathematical differences implemented in the Python script.

---

## 4. Key Code Snippets

### Camera Controller (Point 1)

```csharp
// File: ControlCamaras.cs
// Toggles between two cameras (perspective and orthographic) when the 'C' key is pressed.

using UnityEngine;

public class ControlCamaras : MonoBehaviour
{
    public Camera camaraPerspectiva;
    public Camera camaraOrtografica;

    void Start()
    {
        camaraPerspectiva.enabled = true;
        camaraOrtografica.enabled = false;
    }

    void Update()
    {
        // Check if the 'C' key was pressed
        if (Input.GetKeyDown(KeyCode.C))
        {
            // Invert the 'enabled' state of both cameras
            camaraPerspectiva.enabled = !camaraPerspectiva.enabled;
            camaraOrtografica.enabled = !camaraOrtografica.enabled;
        }
    }
}
````

### Custom Shaders (Point 3)
![Evidence point 3](./media/ColorDinamico.png)
---
![Evidence point 3](./media/DynamicTexture.png)
---
![Evidence point 3](./media/Toon.png)

### Projection Matrices (Point 11 - Python)
```python
# File: python/projection_matrices.py
# Implements perspective projection matrix from scratch.

import numpy as np

# ... (parameter setup) ...

# Fórmula de la matriz de Perspectiva
M_persp = np.array([
    [t_calc/aspecto, 0, 0,                               0],
    [0,              t_calc, 0,                               0],
    [0,              0,      (f_persp+n_persp)/(n_persp-f_persp), (2*f_persp*n_persp)/(n_persp-f_persp)],
    [0,              0,      -1,                              0] # ¡El truco! Pone -Z en el valor W
])

# Aplicamos la matriz
p_clip_persp = M_persp @ p_mundo

# La "División de Perspectiva" es dividir (x, y, z) por 'w'.
w = p_clip_persp[3]
p_ndc_persp = p_clip_persp[:3] / w
```
### Projection Matrices (Point 11 - Unity)
![Evidence point 11](./media/Punto11.png)
-----

## 5\. Graphic Evidence (Renders)

### PBR & Lighting (Point 1)
![Evidence point 1](./media/point1.gif)

### Custom Shaders (Point 3)
![Evidence point 3](./media/point3-colors.gif)
---
![Evidence point 3](./media/point3-texture.gif)
---
![Evidence point 3](./media/point3-toon.gif)

### Projection Matrices (Point 11)
![Evidence point 11](./media/point11.gif)

## 6\. Reflection

  * **Learnings:**
  * **Technical Challenges:**
  * **Possible Improvements:**



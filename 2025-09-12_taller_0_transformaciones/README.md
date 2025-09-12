# Taller 0 - Transformaciones Básicas en Computación Visual

Este repositorio contiene las implementaciones del taller Transformaciones Básicas en Computación Visual, cuyo objetivo es explorar los conceptos fundamentales de transformaciones geométricas (traslación, rotación y escala) en cuatro entornos de programación visual diferentes. Cada implementación muestra un objeto animado en función del tiempo.

---

## 1. Python con Matplotlib y NumPy

### Explicación
Esta implementación se enfoca en el enfoque matemático de las transformaciones. Se define un cuadrado 2D a través de sus vértices en coordenadas homogéneas y se aplican transformaciones mediante la construcción y multiplicación de matrices 3x3. La animación se genera en un bucle donde, en cada frame, se calcula una matriz de transformación combinada (`M = T @ R @ S`) basada en una variable de tiempo `t`. `Matplotlib` se encarga de renderizar cada frame, y `Imageio` los une para crear el GIF final.

### Resultado
![Animación en Python](python/output_python/pythonGIF.gif)

### Código Relevante
La lógica principal reside en el bucle de animación, donde los parámetros de las matrices de Escala, Rotación y Traslación se calculan dinámicamente.

```python
# 't' es nuestro factor de tiempo, va de 0.0 a 1.0
t = i / (num_frames - 1)

# Calcular parámetros de transformación basados en 't'
S = get_scale_matrix(1 + 0.4 * np.sin(t * 2 * np.pi), 1 + 0.4 * np.sin(t * 2 * np.pi))
R = get_rotation_matrix(t * 360)
T = get_translation_matrix(200 * np.cos(t * 2 * np.pi), 200 * np.sin(t * 2 * np.pi))

# Combinar matrices: Escala -> Rotación -> Traslación
M = T @ R @ S

# Aplicar la transformación a los vértices originales
transformed_square = M @ original_square
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generar_rejilla(tamaño=10, espaciado=1.0):
    """Genera una rejilla 3D usando BUCLES"""
    vertices = []
    for i in range(tamaño):
        for j in range(tamaño):
            x = i * espaciado - tamaño * espaciado / 2
            y = j * espaciado - tamaño * espaciado / 2
            z = np.sin(x * 0.5) * np.cos(y * 0.5)
            vertices.append([x, y, z])
    return np.array(vertices)

def generar_espiral(n_puntos=200, vueltas=8):
    """Genera espiral 3D usando BUCLE y modificación de vértices"""
    vertices = []
    for i in range(n_puntos):
        t = i / n_puntos
        theta = vueltas * 2 * np.pi * t
        z = 4 * t - 2  # rango [-2, 2]
        r = z**2 + 1 
        
        x = r * np.sin(theta)
        y = r * np.cos(theta)
        vertices.append([x, y, z])
    
    return np.array(vertices)

def arbol_pitagoras(ax, x, y, angulo, longitud, profundidad):
    """Genera árbol fractal usando RECURSIÓN"""
    if profundidad == 0:
        return
    
    x_fin = x + longitud * np.cos(angulo)
    y_fin = y + longitud * np.sin(angulo)
    
    ax.plot([x, x_fin], [y, y_fin], 'brown', linewidth=profundidad)
    
    nueva_longitud = longitud * 0.7
    arbol_pitagoras(ax, x_fin, y_fin, angulo - np.pi/6, nueva_longitud, profundidad - 1)
    arbol_pitagoras(ax, x_fin, y_fin, angulo + np.pi/6, nueva_longitud, profundidad - 1)

def cubo_recursivo(ax, x, y, z, tamaño, profundidad):
    if profundidad == 0 or tamaño < 0.1:
        vertices = [
            [x, y, z], [x+tamaño, y, z], [x+tamaño, y+tamaño, z], [x, y+tamaño, z],
            [x, y, z+tamaño], [x+tamaño, y, z+tamaño], 
            [x+tamaño, y+tamaño, z+tamaño], [x, y+tamaño, z+tamaño]
        ]
        vertices = np.array(vertices)
        ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], 
                  c='cyan', s=20, alpha=0.6)
        return

    nuevo_tamaño = tamaño / 3
    for i in range(2):
        for j in range(2):
            for k in range(2):
                cubo_recursivo(ax, 
                             x + i * nuevo_tamaño * 2, 
                             y + j * nuevo_tamaño * 2, 
                             z + k * nuevo_tamaño * 2, 
                             nuevo_tamaño, profundidad - 1)

fig = plt.figure(figsize=(16, 10))
fig.suptitle('MODELADO PROCEDURAL: Geometría Generada por Algoritmos', 
             fontsize=16, fontweight='bold')

# --- SUBPLOT 1: REJILLA ---
ax1 = fig.add_subplot(2, 3, 1, projection='3d')
rejilla = generar_rejilla(tamaño=15, espaciado=0.5)
ax1.scatter(rejilla[:, 0], rejilla[:, 1], rejilla[:, 2], 
           c=rejilla[:, 2], cmap='viridis', s=10)
ax1.set_title('1. Rejilla (Bucle doble)\nSuperficie ondulada generada', fontsize=10)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')

# --- SUBPLOT 2: ESPIRAL ---
ax2 = fig.add_subplot(2, 3, 2, projection='3d')
espiral = generar_espiral(n_puntos=300, vueltas=8)
ax2.plot(espiral[:, 0], espiral[:, 1], espiral[:, 2], 
        color='purple', linewidth=2)
ax2.set_title('2. Espiral 3D (Bucle)\nRadio variable dinámico', fontsize=10)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')

# --- SUBPLOT 3: ÁRBOL FRACTAL 2D ---
ax3 = fig.add_subplot(2, 3, 3)
arbol_pitagoras(ax3, 0, 0, np.pi/2, 2, 8)
ax3.set_title('3. Árbol de Pitágoras (Recursión)\nFractal 2D', fontsize=10)
ax3.set_xlim(-4, 4)
ax3.set_ylim(-1, 8)
ax3.set_aspect('equal')
ax3.grid(True, alpha=0.3)

# --- SUBPLOT 4: CUBO FRACTAL 3D ---
ax4 = fig.add_subplot(2, 3, 4, projection='3d')
cubo_recursivo(ax4, 0, 0, 0, 3, 2)
ax4.set_title('4. Estructura Cúbica (Recursión)\nFractal 3D simplificado', fontsize=10)
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.set_zlabel('Z')

# --- SUBPLOT 5: COMPARATIVA VISUAL ---
ax5 = fig.add_subplot(2, 3, 5)
ax5.axis('off')
comparativa = """
COMPARATIVA: Código vs Manual

MODELADO POR CÓDIGO:
✓ Precisión matemática exacta
✓ Fácil de modificar parámetros
✓ Genera variaciones infinitas
✓ Ideal para patrones repetitivos
✓ Reproducible y versionable
✗ Curva de aprendizaje técnica
✗ Menos libertad artística

MODELADO MANUAL (3D):
✓ Control artístico intuitivo
✓ Formas orgánicas complejas
✓ Feedback visual inmediato
✗ Difícil de reproducir
✗ Lento para formas complejas
✗ Cambios requieren rehacer
"""
ax5.text(0.1, 0.5, comparativa, fontsize=9, family='monospace',
        verticalalignment='center')

ax6 = fig.add_subplot(2, 3, 6, projection='3d')
n = 200
theta = np.linspace(0, 6 * np.pi, n)
z = np.linspace(-2, 2, n)
r = 1 + 0.5 * np.sin(5 * theta) + 0.3 * np.cos(z * 2)
x = r * np.sin(theta)
y = r * np.cos(theta)
ax6.plot(x, y, z, color='orange', linewidth=2)
ax6.set_title('5. Transformación Dinámica\nRadio modulado por funciones', fontsize=10)
ax6.set_xlabel('X')
ax6.set_ylabel('Y')
ax6.set_zlabel('Z')

plt.tight_layout()
plt.show()
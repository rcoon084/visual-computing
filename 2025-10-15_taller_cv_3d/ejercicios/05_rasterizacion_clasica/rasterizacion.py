import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


# --------------------------------------------
# 1. Algoritmo de Bresenham (Línea)
# --------------------------------------------
def bresenham_line(img, x0, y0, x1, y1, color = 1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if 0 <= x0 < img.shape[1] and 0 <= y0 < img.shape[0]:
            img[y0, x0] = color
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


# --------------------------------------------
# 2. Algoritmo de Punto Medio (Círculo)
# --------------------------------------------
def midpoint_circle(img, xc, yc, r, color = 1):
    x = 0
    y = r
    p = 1 - r

    def draw_circle_points(xc, yc, x, y):
        points = [
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x)
        ]
        for px, py in points:
            if 0 <= px < img.shape[1] and 0 <= py < img.shape[0]:
                img[py, px] = color

    draw_circle_points(xc, yc, x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2*x + 1
        else:
            y -= 1
            p += 2*(x - y) + 1
        draw_circle_points(xc, yc, x, y)


# --------------------------------------------
# 3. Algoritmo Scanline (Relleno de Triángulo)
# --------------------------------------------
def scanline_triangle(img, p1, p2, p3, color=1):
    # Ordenar vértices por coordenada y (de menor a mayor)
    v1, v2, v3 = sorted([p1, p2, p3], key=lambda v: v[1])
    x1, y1 = v1
    x2, y2 = v2
    x3, y3 = v3

    if y2 == y3:
        fill_flat_bottom(img, v1, v2, v3, color)
    elif y1 == y2:
        fill_flat_top(img, v1, v2, v3, color)
    else:
        # Calcular punto de división en el borde v1-v3
        x4 = x1 + ( (y2 - y1) / (y3 - y1) ) * (x3 - x1)
        v4 = (int(x4), y2)

        fill_flat_bottom(img, v1, v2, v4, color)
        fill_flat_top(img, v2, v4, v3, color)


def fill_flat_bottom(img, v1, v2, v3, color=1):
    x1, y1 = v1
    x2, y2 = v2
    x3, y3 = v3

    invslope1 = (x2 - x1) / (y2 - y1) if y2 != y1 else 0
    invslope2 = (x3 - x1) / (y3 - y1) if y3 != y1 else 0

    curx1 = x1
    curx2 = x1

    for y in range(y1, y2 + 1):
        draw_scanline(img, int(curx1), int(curx2), y, color)
        curx1 += invslope1
        curx2 += invslope2


def fill_flat_top(img, v1, v2, v3, color=1):
    x1, y1 = v1
    x2, y2 = v2
    x3, y3 = v3

    invslope1 = (x3 - x1) / (y3 - y1) if y3 != y1 else 0
    invslope2 = (x3 - x2) / (y3 - y2) if y3 != y2 else 0

    curx1 = x3
    curx2 = x3

    for y in range(y3, y1 - 1, -1):
        draw_scanline(img, int(curx1), int(curx2), y, color)
        curx1 -= invslope1
        curx2 -= invslope2


def draw_scanline(img, x_start, x_end, y, color = 1):
    if y < 0 or y >= img.shape[0]:
        return
    if x_start > x_end:
        x_start, x_end = x_end, x_start
    x_start = max(0, x_start)
    x_end = min(img.shape[1]-1, x_end)
    img[y, x_start:x_end + 1] = color


# --------------------------------------------
# Pruebas individuales por algoritmo
# --------------------------------------------
if __name__ == "__main__":
    width, height = 300, 300

    # 1. Línea Bresenham
    img_line = np.zeros((height, width), dtype = np.uint8)
    bresenham_line(img_line, 20, 20, 250, 200, color = 255)
    Image.fromarray(img_line).save("../../assets/raster_linea.png")

    plt.imshow(img_line, cmap = 'gray')
    plt.title("Bresenham - Línea")
    plt.axis('off')
    plt.show()

    # 2. Círculo punto medio
    img_circle = np.zeros((height, width), dtype = np.uint8)
    midpoint_circle(img_circle, 150, 150, 50, color = 255)
    Image.fromarray(img_circle).save("../../assets/raster_circulo.png")

    plt.imshow(img_circle, cmap = 'gray')
    plt.title("Punto Medio - Círculo")
    plt.axis('off')
    plt.show()

    # 3. Triángulo scanline
    img_triangle = np.zeros((height, width), dtype = np.uint8)
    scanline_triangle(img_triangle, (50, 220), (250, 220), (150, 100), color = 255)
    Image.fromarray(img_triangle).save("../../assets/raster_triangulo.png")

    plt.imshow(img_triangle, cmap = 'gray')
    plt.title("Scanline - Triángulo Relleno")
    plt.axis('off')
    plt.show()

from PIL import Image
import numpy as np
import cv2

# -----------------------
# Función de convolución manual mejorada
# -----------------------
def convolucion_manual(img, kernel):
    # Obtener dimensiones
    k_height, k_width = kernel.shape
    pad_h = k_height // 2
    pad_w = k_width // 2
    
    # Padding de la imagen con modo reflect para bordes
    img_padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode = 'reflect')
    
    # Imagen de salida como float32 para evitar overflow
    output = np.zeros_like(img, dtype = np.float32)
    
    # Convolución
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = img_padded[i:i + k_height, j:j + k_width].astype(np.float32)
            output[i, j] = np.sum(region * kernel.astype(np.float32))
    
    # Limitar valores a rango [0, 255]
    output = np.clip(output, 0, 255)
    return output.astype(np.uint8)


# -----------------------
# Cargar imagen
# -----------------------
img = cv2.imread('../../assets/input.jpg', cv2.IMREAD_GRAYSCALE)


# -----------------------
# Definir kernels (3 ejemplos)
# -----------------------
kernel_sharpen = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype = np.float32)

kernel_blur = np.ones((3,3), dtype = np.float32) / 9

kernel_edge = np.array([[-1, -1, -1],
                        [-1, 8, -1],
                        [-1, -1, -1]], dtype = np.float32)


# -----------------------
# Aplicar convoluciones manual
# -----------------------
img_sharpen_manual = convolucion_manual(img, kernel_sharpen)
img_blur_manual = convolucion_manual(img, kernel_blur)
img_edge_manual = convolucion_manual(img, kernel_edge)


# -----------------------
# Aplicar convoluciones con OpenCV (para comparación)
# -----------------------
img_sharpen_cv = cv2.filter2D(img, -1, kernel_sharpen)
img_blur_cv = cv2.filter2D(img, -1, kernel_blur)
img_edge_cv = cv2.filter2D(img, -1, kernel_edge)


# -----------------------
# Mostrar resultados
# -----------------------
cv2.imshow("Original", img)
cv2.imshow("Sharpen Manual", img_sharpen_manual)
cv2.imshow("Sharpen OpenCV", img_sharpen_cv)
cv2.imshow("Blur Manual", img_blur_manual)
cv2.imshow("Blur OpenCV", img_blur_cv)
cv2.imshow("Edge Manual", img_edge_manual)
cv2.imshow("Edge OpenCV", img_edge_cv)

Image.fromarray(img).save("../../assets/original.png")
Image.fromarray(img_sharpen_manual).save("../../assets/sharpen_manual.png")
Image.fromarray(img_sharpen_cv).save("../../assets/sharpen_opencv.png")
Image.fromarray(img_blur_manual).save("../../assets/blur_manual.png")
Image.fromarray(img_blur_cv).save("../../assets/blur_opencv.png")
Image.fromarray(img_edge_manual).save("../../assets/edge_manual.png")
Image.fromarray(img_edge_cv).save("../../assets/edge_opencv.png")

cv2.waitKey(0)
cv2.destroyAllWindows()

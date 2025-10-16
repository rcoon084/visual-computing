import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

img = cv2.imread('input.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
print("Dimensiones:", img_rgb.shape)

r, g, b = cv2.split(img_rgb)
img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
h, s, v = cv2.split(img_hsv)

edited = img_rgb.copy()

edited[50:150, 50:150] = [255, 0, 0] 

region = img_rgb[150:250, 200:400].copy()

region_resized = cv2.resize(region, (200, 200))
edited[50:250, 400:600] = region_resized

bright_contrast = cv2.convertScaleAbs(edited, alpha=1.2, beta=40)

titles = ['Original', 'Editada', 'Brillo+Contraste']
images = [img_rgb, edited, bright_contrast]

plt.figure(figsize=(15, 6))
for i in range(3):
    plt.subplot(1, 3, i+1)
    plt.imshow(images[i])
    plt.title(titles[i])
    plt.axis('off')
plt.tight_layout()
plt.savefig('before_after.png')
plt.show()

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(r, cmap='Reds')
plt.title('Canal R')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(g, cmap='Greens')
plt.title('Canal G')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(b, cmap='Blues')
plt.title('Canal B')
plt.axis('off')

plt.tight_layout()
plt.savefig('channels_rgb.png')
plt.show()

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(h, cmap='hsv')
plt.title('Canal H (Tono)')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(s, cmap='gray')
plt.title('Canal S (Saturación)')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(v, cmap='gray')
plt.title('Canal V (Valor)')
plt.axis('off')

plt.tight_layout()
plt.savefig('channels_hsv.png')
plt.show()


plt.figure(figsize=(12, 4))
colors = ('r', 'g', 'b')
for i, col in enumerate(colors):
    plt.subplot(1, 3, i+1)
    plt.hist(img_rgb[:, :, i].ravel(), bins=256, color=col, alpha=0.6, label='Original')
    plt.hist(bright_contrast[:, :, i].ravel(), bins=256, color=col, alpha=0.3, label='Editada')
    plt.title(f'Histograma canal {col.upper()}')
    plt.legend()
plt.tight_layout()
plt.savefig('histograms.png')
plt.show()

import numpy as np
from scipy.signal import butter, filtfilt
import pygame
import time

duracion = 1.0 
n_samples = int(fs * duracion)

b_alpha, a_alpha = butter(4, [8/(fs/2), 13/(fs/2)], btype='band')
b_beta, a_beta = butter(4, [13/(fs/2), 30/(fs/2)], btype='band')

def generar_senal_eeg():
    """Genera señal EEG sintética con ondas alfa, beta y ruido"""
    t = np.linspace(0, duracion, n_samples)
    alfa1 = np.sin(2 * np.pi * 10 * t)  
    alfa2 = 0.5 * np.sin(2 * np.pi * 12 * t)
    beta1 = 0.7 * np.sin(2 * np.pi * 20 * t)
    beta2 = 0.4 * np.sin(2 * np.pi * 25 * t)
    # Ruido
    ruido = 0.3 * np.random.randn(len(t))
    return alfa1 + alfa2 + beta1 + beta2 + ruido

def filtrar_alfa(signal):
    """Aplica filtro pasa-banda para extraer ondas alfa (8-13 Hz)"""
    return filtfilt(b_alpha, a_alpha, signal)

def filtrar_beta(signal):
    """Aplica filtro pasa-banda para extraer ondas beta (13-30 Hz)"""
    return filtfilt(b_beta, a_beta, signal)

# --- PyGame setup ---
pygame.init()
ancho, alto = 900, 600
screen = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Simulación BCI - EEG Control Visual (Alpha/Beta)")
font = pygame.font.SysFont("Arial", 24)
font_small = pygame.font.SysFont("Arial", 18)

color_bajo = (20, 20, 60)
color_alto_alfa = (180, 50, 255)
color_alto_beta = (255, 150, 50)
COLOR_TEXTO = (255, 255, 255)
COLOR_INFO = (200, 200, 200)

# Variables de control
running = True
clock = pygame.time.Clock()
historial_alfa = []
historial_beta = []
max_historial = 5

# Umbrales adaptativos para AMBAS bandas
umbral_alfa_bajo = 0.0
umbral_alfa_alto = 0.0
umbral_beta_bajo = 0.0
umbral_beta_alto = 0.0
contador_calibracion = 0
MUESTRAS_CALIBRACION = 30

modo_banda = "ALPHA"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                historial_alfa.clear()
                historial_beta.clear()
                contador_calibracion = 0
                umbral_alfa_bajo = 0.0
                umbral_alfa_alto = 0.0
                umbral_beta_bajo = 0.0
                umbral_beta_alto = 0.0
            elif event.key == pygame.K_TAB:
                modo_banda = "BETA" if modo_banda == "ALPHA" else "ALPHA"

    eeg = generar_senal_eeg()
    eeg_alpha = filtrar_alfa(eeg)
    eeg_beta = filtrar_beta(eeg)
    
    energia_alfa = np.mean(eeg_alpha**2)
    energia_beta = np.mean(eeg_beta**2)

    historial_alfa.append(energia_alfa)
    historial_beta.append(energia_beta)
    
    if len(historial_alfa) > max_historial:
        historial_alfa.pop(0)
    if len(historial_beta) > max_historial:
        historial_beta.pop(0)
    
    energia_alfa_suavizada = np.mean(historial_alfa)
    energia_beta_suavizada = np.mean(historial_beta)

    if contador_calibracion < MUESTRAS_CALIBRACION:
        contador_calibracion += 1
        if contador_calibracion == MUESTRAS_CALIBRACION:
            umbral_alfa_bajo = np.percentile(historial_alfa, 20)
            umbral_alfa_alto = np.percentile(historial_alfa, 80)
            umbral_beta_bajo = np.percentile(historial_beta, 20)
            umbral_beta_alto = np.percentile(historial_beta, 80)

    if umbral_alfa_alto > umbral_alfa_bajo:
        intensidad_alfa = (energia_alfa_suavizada - umbral_alfa_bajo) / (umbral_alfa_alto - umbral_alfa_bajo)
    else:
        intensidad_alfa = min(1.0, energia_alfa_suavizada * 50)
    intensidad_alfa = np.clip(intensidad_alfa, 0.0, 1.0)
    
    if umbral_beta_alto > umbral_beta_bajo:
        intensidad_beta = (energia_beta_suavizada - umbral_beta_bajo) / (umbral_beta_alto - umbral_beta_bajo)
    else:
        intensidad_beta = min(1.0, energia_beta_suavizada * 50)
    intensidad_beta = np.clip(intensidad_beta, 0.0, 1.0)
    
    if modo_banda == "ALPHA":
        intensidad_actual = intensidad_alfa
        color_alto = color_alto_alfa
        energia_actual = energia_alfa_suavizada
        banda_texto = "ALPHA (8-13 Hz) - Relajación"
    else:
        intensidad_actual = intensidad_beta
        color_alto = color_alto_beta
        energia_actual = energia_beta_suavizada
        banda_texto = "BETA (13-30 Hz) - Concentración"
    
    color = tuple(
        int(color_bajo[i] + intensidad_actual * (color_alto[i] - color_bajo[i]))
        for i in range(3)
    )
    
    screen.fill(color)
    
    texto_banda = font.render(f"Banda: {banda_texto}", True, COLOR_TEXTO)
    screen.blit(texto_banda, (20, 20))
    
    texto_energia = font_small.render(
        f"Potencia: {energia_actual:.4f}", 
        True, COLOR_TEXTO
    )
    screen.blit(texto_energia, (20, 60))

    barra_ancho = 350
    barra_alto = 25
    barra_x = 20
    barra_y_alfa = 100
    barra_y_beta = 150
    
    texto_alfa = font_small.render("ALPHA:", True, (180, 50, 255))
    screen.blit(texto_alfa, (barra_x, barra_y_alfa - 20))
    
    pygame.draw.rect(screen, (50, 50, 50), 
                    (barra_x, barra_y_alfa, barra_ancho, barra_alto))
    pygame.draw.rect(screen, (180, 50, 255), 
                    (barra_x, barra_y_alfa, int(barra_ancho * intensidad_alfa), barra_alto))
    pygame.draw.rect(screen, COLOR_TEXTO, 
                    (barra_x, barra_y_alfa, barra_ancho, barra_alto), 2)
    
    texto_beta = font_small.render("BETA:", True, (255, 150, 50))
    screen.blit(texto_beta, (barra_x, barra_y_beta - 20))
    
    pygame.draw.rect(screen, (50, 50, 50), 
                    (barra_x, barra_y_beta, barra_ancho, barra_alto))
    pygame.draw.rect(screen, (255, 150, 50), 
                    (barra_x, barra_y_beta, int(barra_ancho * intensidad_beta), barra_alto))
    pygame.draw.rect(screen, COLOR_TEXTO, 
                    (barra_x, barra_y_beta, barra_ancho, barra_alto), 2)
    
    if contador_calibracion < MUESTRAS_CALIBRACION:
        texto_cal = font_small.render(
            f"Calibrando... {contador_calibracion}/{MUESTRAS_CALIBRACION}", 
            True, (255, 255, 100)
        )
        screen.blit(texto_cal, (20, 200))

    radio_alfa = int(40 + intensidad_alfa * 80)
    pygame.draw.circle(screen, color_alto_alfa, 
                      (ancho // 3, alto // 2 + 50), 
                      radio_alfa, 3)
    texto_c_alfa = font_small.render("ALPHA", True, COLOR_TEXTO)
    screen.blit(texto_c_alfa, (ancho // 3 - 30, alto // 2 + 150))
    
    radio_beta = int(40 + intensidad_beta * 80)
    pygame.draw.circle(screen, color_alto_beta, 
                      (2 * ancho // 3, alto // 2 + 50), 
                      radio_beta, 3)
    texto_c_beta = font_small.render("BETA", True, COLOR_TEXTO)
    screen.blit(texto_c_beta, (2 * ancho // 3 - 25, alto // 2 + 150))
    
    # Instrucciones
    texto_info1 = font_small.render(
        "ESC: Salir | R: Recalibrar | TAB: Cambiar banda", 
        True, COLOR_INFO
    )
    screen.blit(texto_info1, (20, alto - 40))
    
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
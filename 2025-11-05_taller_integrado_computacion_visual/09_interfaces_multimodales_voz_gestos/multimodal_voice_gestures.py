from vosk import Model, KaldiRecognizer
import sounddevice as sd
import mediapipe as mp
import numpy as np
import threading
import random
import queue
import json
import cv2


# --------------------------------------------
# Configuración del modelo VOSK y cola de audio
# --------------------------------------------
vosk_model_path = "model-es"
model = Model(vosk_model_path)
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()


# --------------------------------------------
# Callback de audio
# --------------------------------------------
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_data = (indata * 32767).astype(np.int16)
    audio_queue.put(audio_data.tobytes())


# --------------------------------------------
# Configuración de MediaPipe para detección de manos
# --------------------------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 1)
mp_draw = mp.solutions.drawing_utils
gesture_detected = None


# --------------------------------------------
# Función de detección de gestos simples
# --------------------------------------------
def detect_gesture(landmarks):
    if landmarks.landmark[8].y < landmarks.landmark[6].y and \
       landmarks.landmark[12].y < landmarks.landmark[10].y and \
       landmarks.landmark[16].y > landmarks.landmark[14].y and \
       landmarks.landmark[20].y > landmarks.landmark[18].y:
        return "PEACE"
    return None


# --------------------------------------------
# Variables globales para efectos visuales y comandos
# --------------------------------------------
current_command = None
confetti_active = False
stop_display_counter = 0
peace_display_counter = 0
combined_effect_active = False
screen_color = (0, 0, 0)
confetti_particles = []


# --------------------------------------------
# Función para dibujar cajas de texto con fondo semi-transparente
# --------------------------------------------
def draw_text_box(frame, text, pos, font_scale = 1, color = (255,255,255), bg_color = (0,0,0,150), thickness = 2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    (w, h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = pos
    overlay = frame.copy()
    cv2.rectangle(overlay, (x-5, y-h-5), (x+w+5, y+5), bg_color[:3], -1)
    alpha = bg_color[3]/255 if len(bg_color) == 4 else 0.6
    cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0, frame)
    cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)


# --------------------------------------------
# Función para procesar efectos visuales
# --------------------------------------------
def process_effects(frame):
    global confetti_active, gesture_detected, peace_display_counter
    global combined_effect_active, screen_color, stop_display_counter, confetti_particles

    h, w, _ = frame.shape

    # Overlay de color si confetti activo y gesto PEACE
    if confetti_active and gesture_detected == "PEACE":
        combined_effect_active = True
    else:
        combined_effect_active = False

    if combined_effect_active:
        screen_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        overlay = np.full(frame.shape, screen_color, dtype=np.uint8)
        alpha = 0.4
        frame[:] = cv2.addWeighted(frame, 1-alpha, overlay, alpha, 0)

    # Mostrar mensaje PEACE
    if gesture_detected == "PEACE":
        peace_display_counter = 30
    if peace_display_counter > 0:
        draw_text_box(frame, "MAKE THE PEACE", (w//2 - 150, h//2), font_scale=1, color=(255,255,255), bg_color=(0,0,0,150))
        peace_display_counter -= 1

    # Generación de partículas confetti
    if confetti_active and not combined_effect_active:
        for _ in range(10):
            x = random.randint(0, w)
            y = 0
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            confetti_particles.append([x, y, color])

    # Actualización y dibujo de partículas
    new_particles = []
    for p in confetti_particles:
        x, y, color = p
        cv2.circle(frame, (x, y), 5, color, -1)
        y += 8
        if y < h:
            new_particles.append([x, y, color])
    confetti_particles[:] = new_particles

    # Mostrar mensaje de parada
    if stop_display_counter > 0:
        draw_text_box(frame, "NO MORE PARTY", (w//2 - 150, h//2 - 50), font_scale=1, color=(255,0,0), bg_color=(0,0,0,150))
        stop_display_counter -= 1


# --------------------------------------------
# Captura de video
# --------------------------------------------
cap = cv2.VideoCapture(0)


# --------------------------------------------
# Hilo de video: detección de gestos y dibujo en pantalla
# --------------------------------------------
def video_thread():
    global gesture_detected
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        gesture_detected = None
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture_detected = detect_gesture(hand_landmarks)

        draw_text_box(frame, f"Command: {current_command or ''} | Gesture: {gesture_detected or ''}", (10,40), font_scale=0.8, color=(0,255,0), bg_color=(0,0,0,120))
        process_effects(frame)
        cv2.imshow("Multimodal", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break


# --------------------------------------------
# Hilo de voz: procesamiento de comandos de audio
# --------------------------------------------
def voice_thread():
    global current_command, confetti_active, stop_display_counter
    while True:
        data = audio_queue.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
        else:
            partial = json.loads(recognizer.PartialResult())
            text = partial.get("partial", "")

        # Comandos de voz para activar/desactivar efectos
        if "fiesta" in text.lower():
            current_command = "fiesta"
            confetti_active = True
        elif "apagar" in text.lower():
            current_command = "parar"
            confetti_active = False
            stop_display_counter = 30
        else:
            current_command = None


# --------------------------------------------
# Inicialización del stream de audio
# --------------------------------------------
audio_stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=16000)
audio_stream.start()


# --------------------------------------------
# Inicialización de hilos
# --------------------------------------------
threads = [
    threading.Thread(target=voice_thread, daemon=True),
    threading.Thread(target=video_thread)
]

for t in threads:
    t.start()

threads[-1].join()
cap.release()
cv2.destroyAllWindows()

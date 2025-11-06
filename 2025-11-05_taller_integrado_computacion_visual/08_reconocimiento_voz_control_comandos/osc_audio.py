from pythonosc.udp_client import SimpleUDPClient
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import pyttsx3
import json
import time


# --------------------------------------------
# Configuración del modelo de reconocimiento de voz y OSC
# --------------------------------------------
MODEL_PATH = "model-es"
OSC_IP = "127.0.0.1"
OSC_PORT = 9000


# Inicialización de VOSK
print("[Loading VOSK model...]")
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Inicialización de pyttsx3 para retroalimentación por voz
engine = pyttsx3.init()

# Cliente OSC para enviar comandos
client = SimpleUDPClient(OSC_IP, OSC_PORT)


# --------------------------------------------
# Diccionario de comandos de voz → mensajes OSC
# --------------------------------------------
# Cada palabra clave está asociada a una ruta OSC y sus valores
COMMANDS = {
    "arriba":   ("/move", [0, 1]),
    "abajo":    ("/move", [0, -1]),
    "izquierda":("/move", [-1, 0]),
    "derecha":  ("/move", [1, 0]),
    "rojo":     ("/color", [1, 0, 0]),
    "verde":    ("/color", [0, 1, 0]),
    "azul":     ("/color", [0, 0, 1]),
}


# Variables de control de audio para evitar repetición de comandos
ignore_audio = False
last_response = 0
lock_time = 1.2


# --------------------------------------------
# Función principal de ejecución de comandos
# --------------------------------------------
def execute_command(text):
    global ignore_audio, last_response
    text = text.lower()

    for key in COMMANDS:
        if key in text:
            path, values = COMMANDS[key]
            client.send_message(path, values)

            ignore_audio = True
            engine.say(f"Ejecutando comando {key}")
            engine.runAndWait()
            last_response = time.time()

            print(f"[OSC] → {path} {values}")
            return

    # Si no se reconoce el comando
    ignore_audio = True
    engine.say("Comando no encontrado. Por favor repitalo")
    engine.runAndWait()
    last_response = time.time()
    print("[!!] Command not found", text)


# --------------------------------------------
# Callback de audio para procesar flujo en tiempo real
# --------------------------------------------
def callback(indata, frames, time_data, status):
    global ignore_audio, last_response

    # Evitar repetición de comandos mientras lock_time no ha pasado
    if ignore_audio and time.time() - last_response < lock_time:
        return
    else:
        ignore_audio = False

    data = bytes(indata)

    # Reconocimiento de voz con VOSK
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        texto = result.get("text", "")
        
        if texto.strip():
            print("You say:", texto)
            execute_command(texto)


# --------------------------------------------
# Bloque principal
# --------------------------------------------
if __name__ == "__main__":
    print("\nListen mode (Ctrl+C to exit)")
    print("Allowed commands: arriba / abajo / izquierda / derecha / rojo / verde / azul\n")

    with sd.RawInputStream(samplerate = 16000, blocksize = 8000, channels = 1, dtype = "int16", callback = callback):
        while True:
            time.sleep(0.1)

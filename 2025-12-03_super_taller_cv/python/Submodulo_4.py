import speech_recognition as sr
import pyttsx3
import json
import os
import time
import threading
import tkinter as tk
from tkinter import ttk

os.makedirs("results", exist_ok=True)

r = sr.Recognizer()
mic = sr.Microphone()
engine = pyttsx3.init()

COMANDOS_VALIDOS = {
    "luz": "change_light",
    "iluminar": "change_light",
    "rotar": "rotate_model",
    "girar": "rotate_model",
    "escala": "scale_model",
    "aumentar": "scale_up",
    "disminuir": "scale_down",
    "color": "change_color",
}


root = tk.Tk()
root.title("Subsistema 4 - Control por Voz")
root.geometry("480x350")
root.config(bg="#1e1e1e")

style = ttk.Style()
style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 10))

label_title = ttk.Label(root, text="🎤 Control por Voz", font=("Segoe UI", 16))
label_title.pack(pady=10)

label_status = ttk.Label(root, text="Estado: Inactivo", foreground="#cccccc")
label_status.pack(pady=10)

label_command = ttk.Label(root, text="Último comando: ---", foreground="#00ffcc", font=("Segoe UI", 12))
label_command.pack(pady=10)

history_label = ttk.Label(root, text="Historial:", foreground="white")
history_label.pack()

history_box = tk.Listbox(root, width=50, height=8, bg="#2d2d2d", fg="white")
history_box.pack(pady=5)

running = False

def speak(text):
    engine.say(text)
    engine.runAndWait()

def exportar_json(comando_detectado):
    data = {
        "timestamp": time.time(),
        "command": comando_detectado
    }
    with open("results/last_command.json", "w") as f:
        json.dump(data, f, indent=4)

def escuchar():
    global running
    running = True
    label_status.config(text="Estado: Escuchando...", foreground="#00ff00")

    with mic as source:
        r.adjust_for_ambient_noise(source)

    while running:
        try:
            with mic as source:
                audio = r.listen(source)

            try:
                texto = r.recognize_google(audio, language="es-ES").lower()
            except:
                continue

            comando_detectado = None
            for palabra, comando in COMANDOS_VALIDOS.items():
                if palabra in texto:
                    comando_detectado = comando
                    break

            if comando_detectado:
                label_command.config(text=f"Último comando: {comando_detectado}")
                history_box.insert(0, f"{time.strftime('%H:%M:%S')}  →  {comando_detectado}")
                speak(f"Comando {comando_detectado} recibido")
                exportar_json(comando_detectado)
            else:
                history_box.insert(0, f"{time.strftime('%H:%M:%S')}  →  Sin coincidencia")

        except Exception:
            continue

def iniciar_escucha():
    thread = threading.Thread(target=escuchar)
    thread.daemon = True
    thread.start()

def detener_escucha():
    global running
    running = False
    label_status.config(text="Estado: Inactivo", foreground="#cccccc")

btn_start = ttk.Button(root, text="Iniciar", command=iniciar_escucha)
btn_start.pack(pady=5)

btn_stop = ttk.Button(root, text="Detener", command=detener_escucha)
btn_stop.pack(pady=5)

root.mainloop()

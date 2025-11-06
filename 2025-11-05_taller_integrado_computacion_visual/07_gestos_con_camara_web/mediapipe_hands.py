from collections import deque
import mediapipe as mp
import numpy as np
import random
import cv2


# --------------------------------------------
# Configuración de MediaPipe y constantes
# --------------------------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
FINGER_TIPS = [4,8,12,16,20]


# --------------------------------------------
# Funciones de utilidad
# --------------------------------------------

# Convierte coordenadas normalizadas de MediaPipe a píxeles
def landmark_to_pixel(lm, w, h): 
    return int(lm.x * w), int(lm.y * h)

# Calcula distancia euclidiana entre dos puntos
def euclidean(a, b): 
    return np.hypot(a[0] - b[0], a[1] - b[1])

# Detecta qué dedos están levantados
def fingers_up(hand):
    lm = hand.landmark
    up = [False] * 5
    for i,tp in enumerate([8, 12, 16, 20], start = 1): 
        up[i] = (lm[tp].y < lm[tp - 2].y)
    up[0] = lm[4].x < lm[2].x
    return up


# --------------------------------------------
# Clase Bubble para el minijuego
# --------------------------------------------
class Bubble:
    def __init__(self, w, h):
        # Radio, posición X y Y, color
        self.r = random.randint(25,45) 
        self.x = random.randint(self.r,w-self.r)
        self.y = random.randint(self.r,h-self.r)
        self.c = (random.randint(50,255),random.randint(50,255),random.randint(50,255))


# --------------------------------------------
# Modo 1: Detección de manos
# --------------------------------------------
def mode_1():
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands()
    
    while True:
        r, frame = cap.read()
        frame = cv2.flip(frame, 1)
        res = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if res.multi_hand_landmarks:
            for hand in res.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        cv2.putText(frame, "MODE 1: HAND DETECTION", (10,30),1,1,(0,255,0),2)
        cv2.imshow("MODE 1",frame)

        if cv2.waitKey(1) & 0xFF==27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return


# --------------------------------------------
# Modo 2: Conteo de dedos y reconocimiento de gestos
# --------------------------------------------
def mode_2():
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands()
    
    while True:
        r, frame = cap.read()
        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        res = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if res.multi_hand_landmarks:
            hand = res.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            up = fingers_up(hand)
            count = sum(up)

            if count == 0: g = "Fist"
            elif count == 5: g = "Open Hand"
            elif up[1] and up[2] and not up[3]: g = "Peace"
            elif up[0] and not any(up[1:]): g = "Thumb Up"
            else:g = ""

            cv2.putText(frame,f"Fingers: {count} | Gesture: {g}", (10,50),1,1,(0,255,0),2)

        cv2.putText(frame,"MODE 2: COUNT + GESTURES", (10,30),1,1,(0,255,0),2)
        cv2.imshow("MODE 2",frame)

        if cv2.waitKey(1) & 0xFF==27:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return


# --------------------------------------------
# Modo 3: Acciones según gestos
# --------------------------------------------
def mode_3():
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands()

    zoom = 1.0   
    confetti = []  

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)

        action_txt = ""

        if res.multi_hand_landmarks:
            hand = res.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            up = fingers_up(hand)
            count = sum(up)

            if count == 5:
                action_txt = "GESTURE: OPEN HAND"
                cv2.putText(frame, "HI!", (150,200), 2, 2, (0,255,0), 4)

            elif count == 0:
                action_txt = "GESTURE: FIST (ZOOM)"
                zoom = min(zoom + 0.02, 1.8)
                nh,nw = int(h/zoom), int(w/zoom)
                cropped = frame[(h-nh)//2:(h+nh)//2, (w-nw)//2:(w+nw)//2]
                frame = cv2.resize(cropped, (w,h))

            elif up[0] and not any(up[1:]):
                action_txt = "GESTURE: THUMB UP (CONFETTI)"
                for _ in range(8):
                    confetti.append([random.randint(0,w), random.randint(0,h), random.randint(5,12), (random.randint(0,255),random.randint(0,255),random.randint(0,255))])
            
            for c in confetti[:]:
                cv2.circle(frame, (c[0],c[1]), c[2], c[3], -1)
                c[1] += 5
                if c[1] > h: confetti.remove(c)

            if up[1] and up[2] and not up[3] and not up[4]:
                action_txt = "GESTURE: PEACE (TRACKING)"
                lm = hand.landmark[8]
                x,y = int(lm.x*w), int(lm.y*h)
                cv2.circle(frame,(x,y),25,(255,0,200),3)

        cv2.putText(frame,"MODE 3: ACTIONS BY GESTURE",(10,30),1,1,(0,255,0),2)
        cv2.putText(frame,action_txt,(10,70),1,1,(0,255,0),2)
        cv2.imshow("MODE 3", frame)

        if cv2.waitKey(1) & 0xFF==27: 
            break

    cap.release()
    cv2.destroyAllWindows()
    return


# --------------------------------------------
# Modo 4: Mini-juego Bubble Pop
# --------------------------------------------
def mode_4():
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands()
    score = 0 
    bubbles = []
    w = int(cap.get(3))
    h = int(cap.get(4))
    pts = deque(maxlen = 8)
    for _ in range(4): 
        bubbles.append(Bubble(w, h))

    while True:
        r, frame = cap.read()
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)
        h2, w2 = frame.shape[:2]

        if res.multi_hand_landmarks:
            hand = res.multi_hand_landmarks[0]
            lm = hand.landmark
            ix, iy = landmark_to_pixel(lm[8], w2, h2) 
            px, py = landmark_to_pixel(lm[4], w2, h2) 

            dist = euclidean((ix,iy),(px,py))  

            cv2.line(frame,(ix,iy),(px,py),(255,0,0),2)
            cv2.circle(frame,(ix,iy),10,(0,255,0),-1)
            cv2.circle(frame,(px,py),10,(0,255,0),-1)

            # Si pellizco está cerca, eliminar burbuja y sumar puntos
            PINCH_THRESHOLD = 35  
            if dist < PINCH_THRESHOLD:
                for b in bubbles[:]:
                    if euclidean((ix,iy),(b.x,b.y)) < b.r:
                        score += 1
                        bubbles.remove(b)
                        bubbles.append(Bubble(w2,h2))

        for b in bubbles: 
            cv2.circle(frame,(b.x,b.y),b.r,b.c,-1)

        cv2.putText(frame,f"SCORE: {score}",(20,40),1,1,(0,255,0),2)
        cv2.putText(frame,"MODE 4: BUBBLE POP",(20,75),1,1,(0,255,0),2)
        cv2.imshow("MODE 4",frame)

        if cv2.waitKey(1) & 0xFF==27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return


# --------------------------------------------
# Menú principal
# --------------------------------------------
while True:
    print("""
================= MENU =================
[1] Hand Detection
[2] Fingers Count + Gesture
[3] Action by Gesture
[4] BubblePop Minigame
[0] Exit
========================================
""")

    op = input("Choose an option: ")
    if op=="1": mode_1()
    elif op=="2": mode_2()
    elif op=="3": mode_3()
    elif op=="4": mode_4()
    elif op=="0": break
    else: print("Invalid Option")

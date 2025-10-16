import cv2
import mediapipe as mp
import numpy as np
import math
import random
import time
from enum import Enum
from typing import Tuple, List, Optional

class Scene(Enum):
    MENU = 0
    COLOR_CONTROL = 1
    GAME = 2

class GestureController:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 500

    STATIC_IMAGE_MODE = False
    MAX_NUM_HANDS = 1 
    MIN_DETECTION_CONFIDENCE = 0.7
    MIN_TRACKING_CONFIDENCE = 0.5

    SCENE_CHANGE_COOLDOWN = 1.0
    COLOR_CHANGE_COOLDOWN = 0.5
    GESTURE_HOLD_THRESHOLD = 0.3

    THUMB_TIP = 4
    INDEX_FINGER_TIP = 8
    MIDDLE_FINGER_TIP = 12
    RING_FINGER_TIP = 16
    PINKY_TIP = 20
    FINGER_TIP_IDS = [THUMB_TIP, INDEX_FINGER_TIP, MIDDLE_FINGER_TIP, RING_FINGER_TIP, PINKY_TIP]
    WRIST = 0
    INDEX_FINGER_MCP = 5
    PINKY_MCP = 17

    TEXT_COLOR_INFO = (240, 240, 240) 
    TEXT_COLOR_MAIN = (240, 240, 240) 
    PLAYER_COLOR = (0, 255, 0)
    PLAYER_BORDER_COLOR = (255, 255, 255)

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.STATIC_IMAGE_MODE,
            max_num_hands=self.MAX_NUM_HANDS,
            min_detection_confidence=self.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=self.MIN_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.current_scene = Scene.MENU
        self.background_color = (50, 50, 50)
        self.finger_count = 0
        self.gesture_name = "Ninguno"

        self.last_gesture_time = 0
        self.last_scene_change_time = 0
        self.last_color_change_time = 0
        self.last_detected_gesture = ""
        self.gesture_hold_time = 0

        self.player_pos = [self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2]
        self.targets = []
        self.score = 0
        self.game_active = False

        self.gesture_to_color_map = {
            "Paz": (0, 255, 255),
            "Apuntando": (255, 255, 255),
            "Puño": (255, 0, 255),
            "Tres Dedos": (0, 165, 255), 
        }

        self.generate_targets()


    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.WINDOW_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.WINDOW_HEIGHT)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            processed_frame = self._process_frame(frame)
            cv2.imshow('Gestos Webcam Mediapipe', processed_frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def _process_frame(self, frame: np.ndarray) -> np.ndarray:
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        hand_pos = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                landmarks = hand_landmarks.landmark
                hand_pos = [int(landmarks[self.INDEX_FINGER_MCP].x * w), int(landmarks[self.INDEX_FINGER_MCP].y * h)]

                self.gesture_name, self.finger_count = self._detect_gesture(landmarks)
                self._update_scene(self.gesture_name, hand_pos, landmarks)

        frame = self._draw_scene(frame)
        frame = self._draw_info(frame)
        return frame

    def _count_fingers(self, landmarks) -> int:
        fingers = []
        is_right_hand = landmarks[self.INDEX_FINGER_MCP].x < landmarks[self.PINKY_MCP].x

        is_thumb_open = (landmarks[self.THUMB_TIP].x < landmarks[self.INDEX_FINGER_MCP].x) if is_right_hand else \
                        (landmarks[self.THUMB_TIP].x > landmarks[self.INDEX_FINGER_MCP].x)
        if is_thumb_open:
            fingers.append(1)
        else:
            fingers.append(0)

        for tip_id in self.FINGER_TIP_IDS[1:]:
            if landmarks[tip_id].y < landmarks[tip_id - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers.count(1)

    def _get_distance(self, p1, p2) -> float:
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def _detect_gesture(self, landmarks) -> Tuple[str, int]:
        fingers = self._count_fingers(landmarks)
        
        thumb_tip = landmarks[self.THUMB_TIP]
        index_tip = landmarks[self.INDEX_FINGER_TIP]
        distance = self._get_distance(thumb_tip, index_tip)

        if fingers == 0:
            return "Puno", fingers
        elif fingers == 1 and landmarks[self.INDEX_FINGER_TIP].y < landmarks[self.INDEX_FINGER_TIP - 2].y:
            return "Apuntando", fingers
        elif fingers == 2 and distance < 0.05:
            return "Pellizco", fingers
        elif fingers == 5:
            return "Palma Abierta", fingers
        elif fingers == 2 and landmarks[self.INDEX_FINGER_TIP].y < landmarks[self.INDEX_FINGER_TIP - 2].y and \
             landmarks[self.MIDDLE_FINGER_TIP].y < landmarks[self.MIDDLE_FINGER_TIP - 2].y:
            return "Paz", fingers
        elif fingers == 3:
            return "Tres Dedos", fingers
        else:
            return f"{fingers} Dedos", fingers
    

    def _update_scene(self, gesture: str, hand_pos: Optional[List[int]], landmarks):
        current_time = time.time()

        if not self._is_gesture_stable(gesture):
            return

        if gesture == "Palma Abierta" and self._can_change_scene():
            next_scene_index = (self.current_scene.value + 1) % len(Scene)
            self.current_scene = Scene(next_scene_index)
            self.last_scene_change_time = current_time

        scene_updaters = {
            Scene.COLOR_CONTROL: self._update_color_control,
            Scene.GAME: self._update_game,
        }

        updater = scene_updaters.get(self.current_scene)
        if updater:
            updater(gesture, hand_pos)
        else:
            self.game_active = False

    def _update_color_control(self, gesture: str, hand_pos: Optional[List[int]]):
        if self._can_change_color() and gesture in self.gesture_to_color_map:
            self.background_color = self.gesture_to_color_map[gesture]
            self.last_color_change_time = time.time()

    def _update_game(self, gesture: str, hand_pos: Optional[List[int]]):
        self.game_active = True
        if hand_pos:
            self.player_pos = hand_pos
            for target in self.targets[:]:
                dist = math.hypot(self.player_pos[0] - target['pos'][0], self.player_pos[1] - target['pos'][1])
                if dist < target['radius'] + 25: # 25 es el radio del jugador
                    self.targets.remove(target)
                    self.score += 10

            if not self.targets:
                self.generate_targets()


    def _draw_scene(self, frame: np.ndarray) -> np.ndarray:
        h, w, _ = frame.shape
        overlay = np.full((h, w, 3), self.background_color, dtype=np.uint8)
        frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)

        scene_drawers = {
            Scene.MENU: self._draw_menu,
            Scene.COLOR_CONTROL: self._draw_color_control,
            Scene.GAME: self._draw_game,
        }
        
        drawer = scene_drawers.get(self.current_scene)
        if drawer:
            drawer(frame)
        
        return frame

    def _draw_menu(self, frame: np.ndarray):
        h, w, _ = frame.shape
        cv2.putText(frame, "Palma Abierta: Cambiar Escena", (50, h-150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.TEXT_COLOR_MAIN, 2)
        cv2.putText(frame, "Control de Colores", (50, h-110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.TEXT_COLOR_MAIN, 2)
        cv2.putText(frame, "Juego Interactivo", (50, h-70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.TEXT_COLOR_MAIN, 2)
        cv2.putText(frame, "Pulsa Esc para salir", (50, h-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.TEXT_COLOR_MAIN, 2)

    def _draw_color_control(self, frame: np.ndarray):
        h, w, _ = frame.shape
        instructions = " | ".join([f"{gesto}: {color_name}" for gesto, color_name in zip(self.gesture_to_color_map.keys(), ["Amarillo", "Blanco", "Magenta", "Naranja"])])
        cv2.putText(frame, instructions, (50, h-50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.TEXT_COLOR_MAIN, 2)

    def _draw_game(self, frame: np.ndarray):
        h, w, _ = frame.shape
        cv2.putText(frame, f"PUNTUACION: {self.score}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, self.TEXT_COLOR_MAIN, 2)
        cv2.putText(frame, "Mueve tu mano para recoger objetivos", (50, h-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.TEXT_COLOR_MAIN, 2)

        for target in self.targets:
            cv2.circle(frame, tuple(target['pos']), target['radius'], target['color'], -1)
            cv2.circle(frame, tuple(target['pos']), target['radius'], self.PLAYER_BORDER_COLOR, 2)

        if hasattr(self, 'player_pos'):
            cv2.circle(frame, tuple(self.player_pos), 25, self.PLAYER_COLOR, -1)
            cv2.circle(frame, tuple(self.player_pos), 25, self.PLAYER_BORDER_COLOR, 3)


    def generate_targets(self):
        self.targets = []
        for _ in range(5):
            target = {
                'pos': [random.randint(50, self.WINDOW_WIDTH - 50), random.randint(50, self.WINDOW_HEIGHT - 50)],
                'color': (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                'radius': random.randint(20, 40)
            }
            self.targets.append(target)

    def _can_change_scene(self) -> bool:
        return time.time() - self.last_scene_change_time > self.SCENE_CHANGE_COOLDOWN

    def _can_change_color(self) -> bool:
        return time.time() - self.last_color_change_time > self.COLOR_CHANGE_COOLDOWN

    def _is_gesture_stable(self, gesture: str) -> bool:
        current_time = time.time()

        if gesture == self.last_detected_gesture:
            self.gesture_hold_time = current_time - self.last_gesture_time
        else:
            self.last_detected_gesture = gesture
            self.last_gesture_time = current_time
            self.gesture_hold_time = 0

        return self.gesture_hold_time >= self.GESTURE_HOLD_THRESHOLD

    def update_scene(self, gesture, hand_pos):
        self._update_scene(gesture, hand_pos, None)

    def _draw_info(self, frame: np.ndarray) -> np.ndarray:
        cv2.putText(frame, f"Escena: {self.current_scene.name}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.TEXT_COLOR_INFO, 2)
        cv2.putText(frame, f"Gesto: {self.gesture_name}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.TEXT_COLOR_INFO, 2)

        if self.gesture_hold_time > 0:
            self._draw_progress_bar(frame, "Mantener gesto", self.gesture_hold_time, self.GESTURE_HOLD_THRESHOLD, (10, 110))

        return frame

    def _draw_progress_bar(self, frame, label, current_time, max_time, position, width=200, height=10):
        x, y = position
        progress = min(current_time / max_time, 1.0)
        
        cv2.rectangle(frame, (x, y), (x + width, y + height), (50, 50, 50), -1)
        fill_width = int(width * progress)
        color = (0, 255, 0) if progress >= 1.0 else (0, 255, 255)
        cv2.rectangle(frame, (x, y), (x + fill_width, y + height), color, -1)
        cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.TEXT_COLOR_MAIN, 1)


if __name__ == "__main__":
    controller = GestureController()
    controller.run()
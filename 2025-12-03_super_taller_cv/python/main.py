from ultralytics import YOLO
import cv2
import json
import time
import os
import numpy as np

os.makedirs("results/detections", exist_ok=True)
os.makedirs("results/json", exist_ok=True)

model = YOLO("yolov8n-seg.pt")

cap = cv2.VideoCapture(0)
frame_id = 0


def draw_transparent_box(img, x, y, w, h, alpha=0.4, color=(30, 30, 30)):
    overlay = img.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
    return cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

def draw_text(img, text, x, y, color=(255, 255, 255), scale=0.6, thickness=1):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    start = time.time()
    results = model(frame)
    end = time.time()
    fps = 1 / (end - start)

    annotated = results[0].plot()

    boxes = results[0].boxes if results[0].boxes is not None else []
    masks = results[0].masks.data if results[0].masks is not None else []

    detections_json = []
    num_objects = len(boxes)

    for i, box in enumerate(boxes):
        mask_data = masks[i].cpu().numpy().tolist() if i < len(masks) else None

        detections_json.append({
            "class": int(box.cls),
            "confidence": float(box.conf),
            "bbox": box.xyxy.tolist(),
            "mask": mask_data
        })

    cv2.imwrite(f"results/detections/frame_{frame_id}.jpg", annotated)
    with open(f"results/json/frame_{frame_id}.json", "w") as f:
        json.dump(detections_json, f, indent=4)

    annotated = draw_transparent_box(annotated, 10, 10, 260, 120, alpha=0.5, color=(20, 20, 20))

    draw_text(annotated, "SUBSISTEMA 1: DETECCION + SEGMENTACION", 20, 35, (0, 255, 255), 0.55)

    draw_text(annotated, f"FPS: {fps:.1f}", 20, 65, (0, 255, 0), 0.7)
    draw_text(annotated, f"Objetos detectados: {num_objects}", 20, 95, (255, 200, 0), 0.65)

    if num_objects > 0:
        class_name = model.names[int(boxes[0].cls)]
        confidence = float(boxes[0].conf)
        draw_text(annotated, f"Primer objeto: {class_name} ({confidence:.2f})", 20, 125, (255, 255, 255), 0.55)

    cv2.imshow("Vision System - Detection & Segmentation", annotated)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    frame_id += 1

cap.release()
cv2.destroyAllWindows()

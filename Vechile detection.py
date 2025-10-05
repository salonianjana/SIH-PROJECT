import cv2
import time
import os
import csv
from ultralytics import YOLO

# Load YOLO model (make sure yolov8n.pt is in same folder or installed via ultralytics)
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

# Parameters
window_seconds = 15   # collect counts per window
window_start = time.time()
counts_window = []

print("🚦 Vehicle detection started...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO inference
    results = model(frame, stream=True)

    vehicle_count = 0
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            # Detect vehicles only
            if label in ["car", "bus", "truck", "motorbike"]:
                vehicle_count += 1
                # Draw box
                x1, y1, x2, y2 = box.xyxy[0]
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display live count
    cv2.putText(frame, f"Vehicles: {vehicle_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Vehicle Detection", frame)

    # Save count for window
    counts_window.append(vehicle_count)

    # Every `window_seconds`, log avg count
    if time.time() - window_start >= window_seconds:
        avg_count = sum(counts_window) / len(counts_window)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Print to console
        print(f"[{timestamp}] Avg vehicles: {avg_count:.2f}")

        # Save to counts.csv
        file_exists = os.path.isfile("counts.csv")
        with open("counts.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "count"])
            writer.writerow([timestamp, avg_count])

        # Reset window
        counts_window = []
        window_start = time.time()

    # Exit with Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

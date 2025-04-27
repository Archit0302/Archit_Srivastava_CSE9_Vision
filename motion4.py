import cv2
import winsound
import datetime
import os
import threading

# Setup
cam = cv2.VideoCapture(0)
fps = cam.get(cv2.CAP_PROP_FPS)
frame_skip = int(fps // 10)  # Process about 10 frames per second

# Create folders
folders = ['Snapshots/Small', 'Snapshots/Medium', 'Snapshots/Big', 'Snapshots/Extreme']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Open log file
log_file = open('motion_log.txt', 'a')

snapshot_counter = {'Small': 0, 'Medium': 0, 'Big': 0, 'Extreme': 0}
motion_count = 0

frame_width = int(cam.get(3))
frame_height = int(cam.get(4))

frame_id = 0
motion_in_progress = False
save_frame = None
last_motion_type = "None"

def play_beep(frequency, duration):
    threading.Thread(target=winsound.Beep, args=(frequency, duration), daemon=True).start()

def detect_direction(prev_center, new_center):
    x1, y1 = prev_center
    x2, y2 = new_center
    dx = x2 - x1
    dy = y2 - y1
    direction = ""
    if abs(dx) > abs(dy):
        if dx > 20:
            direction = "Right"
        elif dx < -20:
            direction = "Left"
    else:
        if dy > 20:
            direction = "Down"
        elif dy < -20:
            direction = "Up"
    return direction

def detect_zone(x, y, w, h, frame_width, frame_height):
    center_x = x + w // 2
    center_y = y + h // 2
    col = center_x * 3 // frame_width
    row = center_y * 3 // frame_height
    zone = f"Zone-{row * 3 + col + 1}"
    return zone

prev_centers = []

while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
        break

    frame_id += 1
    if frame_id % frame_skip != 0:
        # Skip frame to save processing power
        continue

    frame_resized = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)  # Faster smaller kernel
    if 'prev_gray' not in locals():
        prev_gray = gray
        continue

    diff = cv2.absdiff(prev_gray, gray)
    _, thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=1)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    highest_intensity = "None"
    highest_area = 0
    highest_direction = "Unknown"
    highest_zone = "Unknown"

    centers = []

    for c in contours:
        area = cv2.contourArea(c)
        if area < 500:
            continue

        motion_detected = True
        x, y, w, h = cv2.boundingRect(c)
        center = (x + w // 2, y + h // 2)
        centers.append(center)

        if area < 1500:
            intensity = "Small"
            color = (0, 255, 0)
        elif area < 4000:
            intensity = "Medium"
            color = (255, 255, 0)
        elif area < 8000:
            intensity = "Big"
            color = (255, 0, 0)
        else:
            intensity = "Extreme"
            color = (0, 0, 255)

        cv2.rectangle(frame_resized, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame_resized, intensity, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        if area > highest_area:
            highest_area = area
            highest_intensity = intensity
            highest_center = center
            highest_zone = detect_zone(x, y, w, h, 640, 480)

    if motion_detected:
        motion_count += 1
        now = datetime.datetime.now()
        time_str = now.strftime('%Y-%m-%d %H:%M:%S')

        if prev_centers and centers:
            highest_direction = detect_direction(prev_centers[-1], centers[0])

        prev_centers = centers

        # Play sound without blocking
        # if highest_intensity == "Small":
        #     play_beep(500, 100)
        # elif highest_intensity == "Medium":
        #     play_beep(700, 150)
        # elif highest_intensity == "Big":
        #     play_beep(900, 200)
        # elif highest_intensity == "Extreme":
        #     play_beep(1200, 250)

        motion_in_progress = True
        save_frame = frame_resized.copy()
        last_motion_type = highest_intensity

        log_file.write(f"[{highest_intensity}] Motion #{motion_count} at {time_str} | Direction: {highest_direction} | {highest_zone}\n")
        log_file.flush()

    elif motion_in_progress:
        # Save snapshot only once after motion ends
        folder_map = {
            'Small': 'Snapshots/Small',
            'Medium': 'Snapshots/Medium',
            'Big': 'Snapshots/Big',
            'Extreme': 'Snapshots/Extreme'
        }
        snapshot_name = f"{folder_map[last_motion_type]}/motion_{snapshot_counter[last_motion_type]}.jpg"
        cv2.imwrite(snapshot_name, save_frame)
        snapshot_counter[last_motion_type] += 1
        motion_in_progress = False

    # GUI overlay
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    cv2.putText(frame_resized, f"Time: {timestamp}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame_resized, f"Motions: {motion_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    if motion_detected:
        cv2.putText(frame_resized, f"Intensity: {highest_intensity}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
        if highest_direction != "Unknown":
            cv2.putText(frame_resized, f"Direction: {highest_direction}", (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (138, 43, 226), 2)
        if highest_zone != "Unknown":
            cv2.putText(frame_resized, f"Zone: {highest_zone}", (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 191, 255), 2)

    # Display frame
    cv2.imshow('Optimized Motion Detector', frame_resized)

    if cv2.waitKey(10) == ord('q'):
        break

    prev_gray = gray

# Cleanup
cam.release()
cv2.destroyAllWindows()
log_file.close()


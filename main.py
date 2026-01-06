import cv2
import mediapipe as mp
import time
import paho.mqtt.client as mqtt
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# --- Configuration ---
MQTT_BROKER = "202.74.74.42"
MQTT_PORT = 1883
MQTT_TOPIC = "gesture/control"
CAMERA_INDEX = 0

# --- MQTT Setup ---
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

print(f"Connecting to MQTT Broker {MQTT_BROKER}...")
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"Error connecting to MQTT Broker: {e}")
    exit(1)

# --- MediaPipe Tasks Setup ---
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                       num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

# --- Helper Functions ---
def is_hand_closed(landmarks):
    """
    Check if hand is closed (fist).
    Landmarks is a list of NormalizedLandmark.
    """
    # Fingers tips and dip/pip joints
    tips = [8, 12, 16, 20]
    pip = [6, 10, 14, 18] 
    
    closed_fingers = 0
    for t, p in zip(tips, pip):
        if landmarks[t].y > landmarks[p].y:
            closed_fingers += 1
            
    return closed_fingers >= 3

def draw_landmarks_on_image(rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]

        # Draw the hand landmarks.
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])
        
        # Using mediapipe solutions drawing utils if available, 
        # but since 'solutions' is missing, we might need manual drawing or skip it.
        # Actually detection_result has raw coordinates.
        # Minimal drawing: just circles on tips.
        height, width, _ = annotated_image.shape
        for landmark in hand_landmarks:
             cv2.circle(annotated_image, (int(landmark.x * width), int(landmark.y * height)), 5, (0, 255, 0), -1)

    return annotated_image

# --- Main Loop ---
# --- Stability Configuration ---
DEBOUNCE_FRAMES = 5       # Must match for 5 consecutive frames
COOLDOWN_SECONDS = 2.0    # Seconds to wait after sending a command
LOCK_TIMEOUT_SECONDS = 5.0 # Seconds to stay active after unlock

# --- State Variables ---
cap = cv2.VideoCapture(CAMERA_INDEX)
previous_state = None     # Track immediate previous frame for debug/UI (optional)
valid_state = None        # The "stable" state we trust
consecutive_frames = 0    # Counter for debounce
last_action_time = 0      # Timer for cooldown

# --- Safety Lock Variables ---
system_mode = "LOCKED"    # LOCKED or ACTIVE
unlock_time = 0           # Time when system was last unlocked

print("Starting Camera...")

if not cap.isOpened():
    print("Error: Could not open camera.")
    print("Please check if your terminal has Camera permissions in System Settings -> Privacy & Security -> Camera.")
    print("You may need to restart your terminal after granting permission.")
    exit(1)
    
def is_victory_gesture(landmarks):
    """
    Check for Victory/Peace sign (Index and Middle fingers up, others down).
    """
    tips = [8, 12, 16, 20]
    pip = [6, 10, 14, 18]
    
    # 8 (Index) and 12 (Middle) should be UP (tip.y < pip.y)
    # 16 (Ring) and 20 (Pinky) should be DOWN (tip.y > pip.y)
    
    index_up = landmarks[8].y < landmarks[6].y
    middle_up = landmarks[12].y < landmarks[10].y
    ring_down = landmarks[16].y > landmarks[14].y
    pinky_down = landmarks[20].y > landmarks[18].y
    
    return index_up and middle_up and ring_down and pinky_down

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.flip(image, 1)
    # Convert to RGB directly for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Create mp.Image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    
    # Detect
    detection_result = detector.detect(mp_image)
    
    # Check Lock Timeout
    if system_mode == "ACTIVE":
        if (time.time() - unlock_time) > LOCK_TIMEOUT_SECONDS:
            system_mode = "LOCKED"
            print("Timeout: System LOCKED.")
            
    # Visualize
    current_detected_state = None
    
    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            h, w, _ = image.shape
            for lm in hand_landmarks:
                cv2.circle(image, (int(lm.x * w), int(lm.y * h)), 4, (255, 255, 0), -1)

            # Check for Unlock Gesture constantly
            if is_victory_gesture(hand_landmarks):
                unlock_time = time.time() # Reset timer if victory seen
                if system_mode == "LOCKED":
                    system_mode = "ACTIVE"
                    print("Gesture: VICTORY -> System UNLOCKED!")
            
            # Action Logic only if ACTIVE
            if system_mode == "ACTIVE":
                if is_hand_closed(hand_landmarks):
                    current_detected_state = "CLOSED"
                    cv2.putText(image, "Detected: CLOSED", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    current_detected_state = "OPEN"
                    cv2.putText(image, "Detected: OPEN", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
                # --- Stability Logic ---
                if current_detected_state == previous_state:
                    consecutive_frames += 1
                else:
                    consecutive_frames = 0
                    
                previous_state = current_detected_state
                
                # 2. Trigger Action if Stable
                if consecutive_frames >= DEBOUNCE_FRAMES:
                    # Check Cooldown
                    current_time = time.time()
                    if (current_time - last_action_time) > COOLDOWN_SECONDS:
                        
                        if valid_state is None:
                             valid_state = current_detected_state 
                        
                        if current_detected_state != valid_state:
                            if valid_state == "OPEN" and current_detected_state == "CLOSED":
                                print("Stable Gesture: Open -> Closed. Turning Light OFF (Sending 0)")
                                client.publish(MQTT_TOPIC, "0")
                                last_action_time = current_time
                            elif valid_state == "CLOSED" and current_detected_state == "OPEN":
                                print("Stable Gesture: Closed -> Open. Turning Light ON (Sending 1)")
                                client.publish(MQTT_TOPIC, "1")
                                last_action_time = current_time
                            
                            valid_state = current_detected_state
    
    # UI status for User
    
    # 1. Mode Status
    if system_mode == "LOCKED":
        cv2.putText(image, "STATUS: LOCKED (Show Peace Sign)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        # Show Countdown
        remaining = int(LOCK_TIMEOUT_SECONDS - (time.time() - unlock_time))
        cv2.putText(image, f"STATUS: ACTIVE ({remaining}s)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # 2. Light Status (Only show when active or recently active)
        if valid_state:
            status_text = "Light: ON" if valid_state == "OPEN" else "Light: OFF"
            color = (0, 255, 0) if valid_state == "OPEN" else (0, 0, 255)
            cv2.putText(image, status_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
        # 3. Cooldown
        if (time.time() - last_action_time) < COOLDOWN_SECONDS:
             cv2.putText(image, "COOLDOWN...", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)

    cv2.imshow('Hand Gesture MQTT - Safety Lock Mode', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
client.loop_stop()
client.disconnect()

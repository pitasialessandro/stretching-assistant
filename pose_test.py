import cv2
import mediapipe as mp

# Inizializza i moduli di MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Apri la webcam
cap = cv2.VideoCapture(0)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Errore: nessun frame dalla webcam.")
            break

        # Converte da BGR a RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Esegue il rilevamento della posa
        results = pose.process(image)

        # Torna a BGR per visualizzare con OpenCV
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            h, w, _ = image.shape

        # Disegna solo i punti del corpo (indice 11–32)
        for idx in range(11, 33):
            x, y = int(landmarks[idx].x * w), int(landmarks[idx].y * h)
            cv2.circle(image, (x, y), 4, (0, 255, 0), -1)

        # (Facoltativo) Disegna linee di connessione base (spalle, gomiti, ginocchia, ecc.)
        BODY_CONNECTIONS = [
            (11, 12),  # spalle
            (11, 13), (13, 15),  # braccio sinistro
            (12, 14), (14, 16),  # braccio destro
            (11, 23), (12, 24),  # tronco
            (23, 24),  # bacino
            (23, 25), (25, 27),  # gamba sinistra
            (24, 26), (26, 28),  # gamba destra
            (15, 17), (15, 19), (15, 21), # mano sx
            (16, 18), (16, 20), (16, 22) # mano sx
        ]
        for conn in BODY_CONNECTIONS:
            p1, p2 = landmarks[conn[0]], landmarks[conn[1]]
            x1, y1 = int(p1.x * w), int(p1.y * h)
            x2, y2 = int(p2.x * w), int(p2.y * h)
            cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), 2)

        cv2.imshow('Pose Tracker', image)

        if cv2.waitKey(5) & 0xFF == 27:  # ESC per uscire
            break

cap.release()
cv2.destroyAllWindows()

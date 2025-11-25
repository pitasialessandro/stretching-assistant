import cv2
import sys
import mediapipe as mp
# import numpy as np
import math

class PoseDetector:
    def __init__(self, mode=False, model_complexity=1, smooth_landmarks=True, enable_segmentation=False, smooth_segmentation=True, detection_confidence=0.5, tracking_confidence=0.5):
        """
        Inizializza Mediapipe Pose con i parametri scelti.
        """
        self.mode = mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        # Oggetti Mediapipe
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=self.mode,
            model_complexity=self.model_complexity,
            smooth_landmarks=self.smooth_landmarks,
            enable_segmentation=self.enable_segmentation,
            smooth_segmentation=self.smooth_segmentation,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )

        self.ANGLES = [
            { "name": "right_elbow",  "a": 12, "b": 14, "c": 16 },
            { "name": "left_elbow",   "a": 11, "b": 13, "c": 15 },
            { "name": "right_knee",   "a": 24, "b": 26, "c": 28 },
            { "name": "left_knee",    "a": 23, "b": 25, "c": 27 },
            { "name": "right_shoulder", "a": 14, "b": 12, "c": 24 },
            { "name": "left_shoulder",  "a": 13, "b": 11, "c": 23 }
        ]
    
    def detect(self, image):
        """
        Rileva i keypoints nel frame.
        INPUT:
            image: frame BGR da OpenCV
        OUTPUT:
            keypoints: lista di dizionari per ogni landmark
                       [{'id': 0, 'x': ..., 'y': ..., 'z': ...}, ...]
        """
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_rgb.flags.writeable = False

        # rileva i keypoints
        results = self.pose.process(img_rgb)

        # calcola le dimensioni dello schermo in px
        h, w, _ = image.shape

        keypoints = []
        if results.pose_landmarks:
            # enumerate converte una tupla in un array enumerato [(0, ´apple´), ...], qui viene subito decomposto in indice e landmark
            for idx, lm in enumerate(results.pose_landmarks.landmark):
                # normalizzazione delle coordinate rispetto all'immagine
                keypoints.append({
                    'id': idx,
                    'x': lm.x * w,
                    'y': lm.y * h,
                    'z': lm.z * w,  # z normalizzato in media width
                    'visibility': lm.visibility
                })
            return keypoints

    def compute_angle(self, A, B, C):
        """
        funzione che calcola un angolo tra 3 keypoints, dove B rappresenta il vertice
        INPUT:
        Keypoints (dizionari) A, B, C
        OUTPUT:
        angolo ABC in gradi
        """
        # calcolo le componenti dei vettori AB, CB
        AB = (A["x"] - B["x"], A["y"] - B["y"])
        CB = (C["x"] - B["x"], C["y"] - B["y"])

        # calcolo del prodotto scalare e modulo dei vettori
        scalar_product = AB[0]*CB[0] + AB[1]*CB[1]
        modAB = math.sqrt(AB[0]**2 + AB[1]**2)
        modCB = math.sqrt(CB[0]**2 + CB[1]**2)

        if modAB == 0 or modCB == 0:
            sys.stderr.write("error, vector mod = 0")
            return None

        # calcolo dell'angolo
        cos_angle = scalar_product / (modAB * modCB)
        cos_angle = max(-1, min(1, cos_angle))
        angle = math.degrees(math.acos(cos_angle))

        return angle

    def compute_angles(self, keypoints):
        """
        OUTPUT:
        angles = [
            {'points': (id_A, id_B, id_C), 'angle': valore},
            ...
        ]
        """
        angles = []

        # skippa se non ha trovato i keypoints in quel frame
        if keypoints is None:
            return angles
        
        for obj in self.ANGLES:
            # TODO

            A = keypoints[obj["a"]]
            B = keypoints[obj["b"]]
            C = keypoints[obj["c"]]

            angle_val = self.compute_angle(A, B, C)
            angles.append({
                'points' : (obj['a'], obj['b'], obj['c']),
                'angle' : angle_val
            })

        return angles
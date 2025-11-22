import cv2
import mediapipe as mp
import numpy as np
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

        results = self.pose.process(img_rgb)

        keypoints = []
        if results.pose_landmarks:
            # enumerate converte una tupla in un array enumerato [(0, ´apple´), ...], qui viene subito decomposto in indice e landmark
            for idx, lm in enumerate(results.pose_landmarks.landmark):
                # normalizzazione delle coordinate rispetto all'immagine
                h, w, _ = image.shape
                keypoints.append({
                    'id': idx,
                    'x': lm.x * w,
                    'y': lm.y * h,
                    'z': lm.z * w,  # z normalizzato in media width
                    'visibility': lm.visibility
                })
            return keypoints
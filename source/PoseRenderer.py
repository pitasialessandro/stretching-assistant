import cv2

EXCLUDED_LANDMARKS = {1, 2, 3, 4, 5, 6, 9, 10}

class PoseRenderer:
    def __init__ (
        self,
        point_color=(0, 255, 0),
        line_color=(0, 255, 0),
        point_radius=5,
        line_thickness=2
    ):
        self.point_color = point_color
        self.line_color = line_color
        self.point_radius = point_radius
        self.line_thickness = line_thickness

    # descrivo 1 a 1 tutte le connessioni che mi interessa disegnare
        self.body_connections = [
                # Torso
                (11, 12),  # spalle
                (23, 24),  # anche
                (11, 23),  # lato sinistro
                (12, 24),  # lato destro

                # Braccio sinistro
                (11, 13),
                (13, 15),

                # Braccio destro
                (12, 14),
                (14, 16),

                # Gamba sinistra
                (23, 25),
                (25, 27),

                # Gamba destra
                (24, 26),
                (26, 28),

                # Avambracci + polsi (senza dita)
                (15, 21),  # lato sinistro wrist → extra points
                (15, 19),
                (15, 17),

                (16, 22),  # lato destro wrist → extra points
                (16, 20),
                (16, 18),
        ]

        self.ANGLES = [
            { "name": "right_elbow",  "a": 12, "b": 14, "c": 16 },
            { "name": "left_elbow",   "a": 11, "b": 13, "c": 15 },
            { "name": "right_knee",   "a": 24, "b": 26, "c": 28 },
            { "name": "left_knee",    "a": 23, "b": 25, "c": 27 },
            { "name": "right_shoulder", "a": 14, "b": 12, "c": 24 },
            { "name": "left_shoulder",  "a": 13, "b": 11, "c": 23 }
        ]

    def draw(self, frame, keypoints, angles = None):
        if not keypoints:
            return frame
        
        # parte di disegno dei keypoints
        for idx, kp in enumerate(keypoints):
            if idx in EXCLUDED_LANDMARKS:
                continue

            x, y = int(kp['x']), int(kp['y'])

            if (kp['visibility'] < 0.5):
                continue

            cv2.circle(frame, (x,y), self.point_radius, self.point_color, -1)

        # disegna linee rilevanti tra i punti
        for (a, b) in self.body_connections:
            # keypoints é un array indicizzato, quindi il keypoint con id = 5 si troverá in posizione keypoints[5]
            kp1 = keypoints[a]
            kp2 = keypoints[b]

            # check visibility
            # ...

            x1, y1 = int(kp1['x']), int(kp1['y'])
            x2, y2 = int(kp2['x']), int(kp2['y'])

            cv2.line(frame, (x1, y1), (x2, y2), self.line_color, self.line_thickness)

        # disegna a schermo gli angoli calcolati
        if angles:
            for a in angles:
                _, id_vertice, _ = a['points']
                angle_val = a['angle']
                print(angle_val)
                kp_vertice = keypoints[id_vertice]
                x, y = int(kp_vertice['x']), int(kp_vertice['y'])
                cv2.putText(frame, f"{int(angle_val)}", (x+10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, self.point_color, 1)

        return frame
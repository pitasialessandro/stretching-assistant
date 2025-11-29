import cv2

EXCLUDED_LANDMARKS = {1, 3, 4, 6, 9, 10}
VISIBILITY_THRESHOLD = 0.6

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

    def draw(self, frame, keypoints, angles = None, fps = 0):
        if not keypoints:
            return frame
        
        # parte di disegno dei keypoints
        for idx, kp in enumerate(keypoints):
            if idx in EXCLUDED_LANDMARKS:
                continue

            x, y = int(kp['x']), int(kp['y'])

            if (kp['visibility'] < VISIBILITY_THRESHOLD):
                continue

            cv2.circle(frame, (x,y), self.point_radius, self.point_color, -1)

        # disegna linee rilevanti tra i punti
        for (a, b) in self.body_connections:
            # keypoints é un array indicizzato, quindi il keypoint con id = 5 si troverá in posizione keypoints[5]
            kp1 = keypoints[a]
            kp2 = keypoints[b]

            # check visibility
            if kp1['visibility'] < VISIBILITY_THRESHOLD or kp2['visibility'] < VISIBILITY_THRESHOLD:
                continue

            x1, y1 = int(kp1['x']), int(kp1['y'])
            x2, y2 = int(kp2['x']), int(kp2['y'])

            cv2.line(frame, (x1, y1), (x2, y2), self.line_color, self.line_thickness)

        # disegna a schermo gli angoli calcolati
        if angles:
            for a in angles:
                _, id_vertice, _ = a['points']
                angle_val = a['angle']
                # print(angle_val)
                kp_vertice = keypoints[id_vertice]
                x, y = int(kp_vertice['x']), int(kp_vertice['y'])
                cv2.putText(frame, f"{int(angle_val)}", (x+10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, self.point_color, 1)

        # disegna gli fps
        if (fps != 0):
            cv2.putText(frame, f"FPS: {int(fps)}", (7, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, self.point_color, 2)

        return frame
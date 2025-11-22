import cv2
import numpy as np
import PoseModule as pm

def setup_camera():
    """Initializes the video capture object."""
    return cv2.VideoCapture(0)

def update_feedback_and_count(elbow, shoulder, hip, direction, count, form):
    """Determines the feedback message and updates the count based on the angles."""
    feedback = "Fix Form"
    if elbow > 160 and shoulder > 40 and hip > 160:
        form = 1
    if form == 1:
        if elbow <= 90 and hip > 160:
            feedback = "Up"
            if direction == 0:
                count += 0.5
                direction = 1
        elif elbow > 160 and shoulder > 40 and hip > 160:
            feedback = "Down"
            if direction == 1:
                count += 0.5
                direction = 0
        else:
            feedback = "Fix Form"
    return feedback, count, direction, form

def draw_ui(img, per, bar, count, feedback, form):
    """Draws the UI elements on the image."""
    if form == 1:
        # Barra progresso push-up
        cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
        cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    # Contatore push-up
    cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    
    # Feedback
    cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

def main():
    cap = setup_camera()
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            # Angoli principali per push-up
            elbow = detector.findAngle(img, 11, 13, 15)
            shoulder = detector.findAngle(img, 13, 11, 23)
            hip = detector.findAngle(img, 11, 23, 25)

            # Percentuale progresso push-up
            per = np.interp(elbow, (90, 160), (0, 100))
            bar = np.interp(elbow, (90, 160), (380, 50))

            # Aggiorna feedback e conteggio
            feedback, count, direction, form = update_feedback_and_count(
                elbow, shoulder, hip, direction, count, form
            )

            # Disegna UI
            draw_ui(img, per, bar, count, feedback, form)

            # Stampa contatore su terminale
            #print(count)
        
        # Mostra frame
        cv2.imshow('Pushup Counter', img)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
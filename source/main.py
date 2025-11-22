# 3 classi : 
# PoseDetector -> applica MediaPipe, prende keypoints e calcola gli angoli
# PoseRenderer -> disegna a schermo i keypoints e gli angoli
# JsonEmitter -> genera il JSON 

# main loop orchestra: apre la videocamera e si occupa di chiamare i metodi, scrive nella pipe

import cv2
# import JsonEmitter as je
import PoseDetector as pd
# import PoseRenderer as pr

def main():
    detector = pd.PoseDetector()
    # renderer = pr.PoseRenderer()
    # emitter = je.JsonEmitter()

    # avvia videocamera
    cap = cv2.VideoCapture(0)

    i = 0
    while cap.isOpened() :
        success, frame = cap.read()
        if not success:
            print("errore webcam")
            break

        # prepara immagine per MediaPipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        keypoints = detector.detect(image)
        # angles = detector.compute_angles(keypoints)
        # frame = renderer.draw(frame, keypoints)
        # emitter.emit(keypoints, angles)
        if (i == 180):
            print(keypoints)
        # ----------------------------------------------
        # image.flags.writeable = True
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        cv2.imshow('Pose Tracker', frame)
        i += 1
        if (cv2.waitKey(5) & 0xFF) == 27: # ESC per uscire
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
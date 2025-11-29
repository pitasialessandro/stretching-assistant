# 3 classi : 
# PoseDetector -> applica MediaPipe, prende keypoints e calcola gli angoli
# PoseRenderer -> disegna a schermo i keypoints e gli angoli
# JsonEmitter -> genera il JSON 

# main loop orchestra: apre la videocamera e si occupa di chiamare i metodi, scrive nella pipe

import cv2
import time
import zmq
import JsonEmitter as je
import PoseDetector as pd
import PoseRenderer as pr

def main():
    # configurazione ZMQ
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")
    print("Server ZMQ Avviato sulla porta 5555")

    detector = pd.PoseDetector()
    renderer = pr.PoseRenderer()
    emitter = je.JsonEmitter()

    # avvia videocamera
    cap = cv2.VideoCapture(0)

    # acquisisce numero frame
    num_fps = cap.get(cv2.CAP_PROP_FPS)
    if (num_fps == 0):
        num_fps = 30

    # variabili per il calcolo degli fps
    prev_frame_time = 0
    new_frame_time = 0

    i = 0
    while cap.isOpened() :
        success, frame = cap.read()
        timestamp = time.time()
        if not success:
            printf("errore webcam")
            break

        new_frame_time = timestamp
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time

        keypoints = detector.detect(frame)
        angles = detector.compute_angles(keypoints)
        frame = renderer.draw(frame, keypoints, angles, fps)

        # stampa a schermo
        cv2.imshow('Pose Tracker', frame)
        if (cv2.waitKey(5) & 0xFF) == 27: # ESC per uscire
            break

        # debug print
        if (i % (int(num_fps/9)) == 0):
            # print(keypoints)
            # print(angles)
            # print(json_str)
            # print(amount_of_frames)
            json_str = emitter.emit(keypoints, angles, timestamp)
            #  flags=zmq.NOBLOCK
            print(f"Sending packet {i}...    \n")
            try:
                socket.send_string(json_str, zmq.NOBLOCK)
            except zmq.Again:
                print("packet dropped (buffer full)\n")

        i += 1
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
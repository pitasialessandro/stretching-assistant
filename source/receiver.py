# schema publish - subscriber dove il receiver ogni 1 secondo prende il messaggio (sarebbe il clock), quando prende il messaggio prende solamente il piú recente inviato, gli altri precedenti vengono scartati.

import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")   # sottoscrivi tutto
socket.setsockopt(zmq.CONFLATE, 1)      # mantieni solo ultimo

socket.connect("tcp://localhost:5555")

print("Subscriber started")

while True:
    time.sleep(1)    # ricevo solo quando voglio
    msg = socket.recv_string()  # ottengo sempre L'ULTIMO
    print("Got:", msg)

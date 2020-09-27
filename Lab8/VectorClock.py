from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime

                                               
def calc_recv_vector(v1, v2):
    for id  in range(len(v1)):
        v1[id] = max(v1[id], v2[id])
    return v1

def event(pid, vector):
    vector[pid] += 1
    print(f'Something happened in {pid}. Vector: {vector}')
    return vector

def send_message(pipe, pid, vector):
    vector[pid] += 1
    pipe.send((pid, vector))
    print(f'Message sent from {pid}. Vector: {vector}')
    return vector

def recv_message(pipe, pid, vector):
    vector[pid] += 1
    message, v_recived = pipe.recv()
    vector = calc_recv_vector(v_recived, vector)
    print(f'Message received at {pid}. Vector: {vector}')
    return vector

def process_one(pipe12):
    pid = 0
    vector = [0,0,0]
    vector = send_message(pipe12, pid, vector)
    vector = send_message(pipe12, pid, vector)
    vector = event(pid, vector)
    vector = recv_message(pipe12, pid, vector)
    vector = event(pid, vector)
    vector = event(pid, vector)
    vector = recv_message(pipe12, pid, vector)

def process_two(pipe21, pipe23):
    pid = 1
    vector = [0,0,0]
    vector = recv_message(pipe21, pid, vector)
    vector = recv_message(pipe21, pid, vector)
    vector = send_message(pipe21, pid, vector)
    vector = recv_message(pipe23, pid, vector)
    vector = event(pid, vector)
    vector = send_message(pipe21, pid, vector)
    vector = send_message(pipe23, pid, vector)
    vector = send_message(pipe23, pid, vector)
    
def process_three(pipe32):
    pid = 2
    vector = [0,0,0]
    vector = send_message(pipe32, pid, vector)
    vector = recv_message(pipe32, pid, vector)
    vector = event(pid, vector)
    vector = recv_message(pipe32, pid, vector)
    

if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_one, args=(oneandtwo,))
    process2 = Process(target=process_two, args=(twoandone, twoandthree))
    process3 = Process(target=process_three, args=(threeandtwo,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
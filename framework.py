from threading import Thread
import time
import random
import numpy as np


class Agent:
    def __init__(self):
        self.value = np.random.randint(1, 10)
        print(self.value)


    def send_message(self, id):
        t = random.random()
        time.sleep(t)
        for k in range(numAgent):
            if k == id:
                continue
            received_message[k].append(self.value)

    def update_value(self, id):
        trust_message = received_message[id][:2]

        self.value = (sum(trust_message) + self.value) / (len(trust_message) + 1)
        print(self.value)


if __name__ == '__main__':
    numAgent = 5
    iteration = 10
    Agents = [Agent() for k in range(numAgent)]

    start_time = time.time()

    for i in range(iteration):
        received_message = [[] for k in range(numAgent)]
        Threads = [Thread(target=Agents[k].send_message, args=(k,)) for k in range(numAgent)]
        for t_k in Threads:
            t_k.start()
        for t_k in Threads:
            t_k.join()

        Threads2 = [Thread(target=Agents[k].update_value, args=(k,)) for k in range(numAgent)]
        for t_k in Threads2:
            t_k.start()
        for t_k in Threads2:
            t_k.join()
        print("receive_message:", received_message)

        print("time spent:", time.time() - start_time)
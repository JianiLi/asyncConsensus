import time

from TverbergPoint.TverbergPoint import *
from centerpoint.Centerpoint import *


class NormalAgent:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.stop = False
        # print(self.value)

    def send_message(self, numAgent, received_message):
        t = random.random()
        time.sleep(t)
        for k in range(numAgent):
            if k == id:
                continue
            received_message[k].append(self.value)

    def update_value(self, id, numAgent, received_message, method, alpha, velMax, delta, box, step):
        # received_message = received_message
        # if self.value in received_message:
        #     received_message.remove(self.value)
        trust_message = received_message[id][: numAgent - (math.ceil(numAgent / (2 + 2)) - 1) - 1]
        all_message = deepcopy(trust_message)
        all_message.append(self.value)

        if method == "tver":
            sp = self.getTvbSafePoint(all_message)
        elif method == "center":
            sp = self.getCenterSafePoint(all_message)
        elif method == "wc":
            sp = self.getWeightedCP(all_message)
        elif method == "median":
            sp = self.getMedian(all_message)
        else:
            raise Exception("No such method, please enter either 'tver' or 'center'.")

        u = alpha * (math.sqrt((self.value.x - sp.x) ** 2 + (self.value.y - sp.y) ** 2))
        if u > velMax:
            u = velMax

        if abs(u) < delta:
            self.stop = True
        else:
            if sp.x > self.value.x:
                theta = math.atan((sp.y - self.value.y) / (sp.x - self.value.x))
                x = self.value.x + u * math.cos(theta)
                y = self.value.y + u * math.sin(theta)
                newPos = Point(x, y)
            elif sp.x < self.value.x:
                theta = math.atan((sp.y - self.value.y) / (sp.x - self.value.x)) - math.pi
                x = self.value.x + u * math.cos(theta)
                y = self.value.y + u * math.sin(theta)
                newPos = Point(x, y)
            else:
                if sp.y >= self.value.y:
                    y = self.value.y + u
                else:
                    y = self.value.y + u
                newPos = Point(self.value.x, y)
            self.value = newPos

    def getCenterSafePoint(self, all_message):
        centerPoint = Centerpoint()
        # cp = centerPoint.reduce_then_get_centerpoint(self.neighborsPos)
        try:
            # cp = centerPoint.getSafeCenterPoint(self.neighborsPos)
            cp = centerPoint.reduce_then_get_centerpoint(all_message)
            if cp:
                return cp
            else:
                return self.value
        except:
            return self.value

    def getTvbSafePoint(self, all_message):
        Tverp = TverbergPoint()
        # sp = Tverp.getTvbPoint(all_message)
        sp = Tverp.getSafePoint(all_message)
        return sp


class FaultyAgent:
    def __init__(self, box, value):
        self.id = id
        self.value = value
        # self.value = Point(box / 2 + random.random() * 0.5 * box, box / 2 + random.random() * 0.5 * box)
        # print(self.value)

    def send_message(self, numAgent, received_message):
        # t = random.random()
        # time.sleep(t)
        for k in range(numAgent):
            if k == id:
                continue
            received_message[k].append(self.value)

    def update_value(self, id, numAgent, received_message, method, alpha, velMax, delta, box, step):
        # self.value = Point(box / 2 + random.random() * 0.5 * box, box / 2 + random.random() * 0.5 * box)
        dict = {1: [1, 0], 2: [0, -1], 3: [-1, 0], 0: [0, 1]}
        self.value = Point(self.value.x + dict[step % 4][0] * 0.2, self.value.y + dict[step % 4][1] * 0.2)

import time
from copy import deepcopy
from threading import Thread

from agent import NormalAgent, FaultyAgent
from centerpoint.utils.GeoUtils import *
from utils import *

if __name__ == '__main__':
    random.seed(1)

    numAgent = 17  # 13  # number of robot
    n_faulty = 4  # 3  # number of faulty robots
    n_fault_free = numAgent - n_faulty  # number of fault-free robots
    method = "tver"  # "tver" for Tverberg point or "center" for centerpoint, or "wc" for weighted centerpoint
    box = 1
    delta = 1e-7 * box  # halt parameter
    # sensDist = 3  # sensing range
    alpha = 1  # velocity parameter
    velMax = 0.1 * box  # max velocity
    iteration = 30
    fixNeighbor = True

    start_time = time.time()

    p_fault_free = random_point_set(n_fault_free, lower=-box, upper=box * 0.7)  # robot coordinates
    # p_fault_free = p[:n_fault_free]  # fault-free robot coordinates
    # p_faulty = p[n_fault_free:]  # faulty robot coordinates
    p_faulty = random_point_set(n_faulty, lower=box / 2, upper=box)
    p_init = deepcopy(p_fault_free)

    fig = plt.figure(figsize=(2, 2))

    normalAgents = [NormalAgent(k, p_fault_free[k]) for k in range(n_fault_free)]
    faultyAgents = [FaultyAgent(box, p_faulty[k]) for k in range(n_faulty)]
    Agents = normalAgents + faultyAgents

    position_x_along_time = []
    position_y_along_time = []
    diff_nf_and_nf_approx = []

    t = 0

    while t < iteration:
        plot2D(box, p_init, [p.value for p in faultyAgents], [p.value for p in normalAgents], method, t)

        stop = True
        # diff_nf_and_nf_approx_t = []

        t += 1
        print("iteration %d" % t)

        position_x_along_time.append([agent.value.x for agent in normalAgents])
        position_y_along_time.append([agent.value.y for agent in normalAgents])

        received_message = [[] for k in range(numAgent)]
        Threads = [Thread(target=Agents[k].send_message, args=(numAgent, received_message)) for k in range(numAgent)]
        for t_k in Threads:
            t_k.start()
        for t_k in Threads:
            t_k.join()

        Threads2 = [Thread(target=Agents[k].update_value,
                           args=(k, numAgent, received_message, method, alpha, velMax, delta, box, t)) for k in
                    range(numAgent)]
        for t_k in Threads2:
            t_k.start()
        for t_k in Threads2:
            t_k.join()

        # for i in range(0, n_fault_free):
        #     if method == "tver":
        #         nf_approx_t = math.ceil(len(rob_fault_free[i].neighbors) / 4) - 1
        #     elif method == "center":
        #         nf_approx_t = math.ceil(len(rob_fault_free[i].neighbors) / 3) - 1
        #     elif method == "wc":
        #         nf_approx_t = math.floor(len(rob_fault_free[i].neighbors) / 2) - 1
        #     else:
        #         nf_approx_t = 0
        #     nf_t = len([p for p in rob_fault_free[i].neighbors if p in range(numAgent - n_faulty, numAgent)])
        #     diff_nf_and_nf_approx_t.append(nf_approx_t - nf_t)

        for agent in normalAgents:
            stop = stop and agent.stop

        # diff_nf_and_nf_approx.append(diff_nf_and_nf_approx_t)

        # if stop:
        #     break
        print("Total time used: %.2f s" % (time.time() - start_time))

    plotValueChange(method, position_x_along_time, position_y_along_time)

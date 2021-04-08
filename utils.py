from matplotlib.ticker import MaxNLocator
from shapely.geometry import Polygon

from centerpoint.utils.PlotUtils import *


def plot2D(box, p_init, p_faulty, p_fault_free, method, t):
    plt.clf()
    # plt.grid(True, which='major')
    ax = plt.gca()
    ax.set_xlim(-box - 0.1, box + 0.1)
    ax.set_ylim(-box - 0.1, box + 0.1)
    # plt.xticks([0.3*i for i in range(-5,5, 1)])
    # plt.yticks([0.3*i for i in range(-5,5, 1)])
    plt.gca().set_aspect('equal', adjustable='box')
    # ax.grid(True)
    for tic in ax.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    for tic in ax.yaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
        tic.label1On = tic.label2On = False
    start, end = ax.get_xlim()
    # ax.xaxis.set_ticks(np.arange(start, end + 0.01, 0.2))
    # ax.yaxis.set_ticks(np.arange(start, end + 0.01, 0.2))
    plt.xticks([])
    plt.yticks([])

    # ax.set_xticks([0, 0.3, 0.4, 1.0, 1.5])
    # ax.set_xticklabels([-1, "", "", "", "", 0, "", "", "", "", 1])
    # ax.set_yticklabels([-1, "", "", "", "", 0, "", "", "", "", 1])

    # for i in range(0, n_fault_free):
    #     for j in range(0, n_fault_free):
    #         plt.plot([p_init[i].x, p_init[j].x], [p_init[i].y, p_init[j].y], linewidth=0.2,
    #                  color='gray')

    polygon = Polygon([p for p in p_init]).convex_hull
    x, y = polygon.exterior.xy
    plt.plot(x, y, linewidth=1, color='gray')

    plot_point_set(p_faulty, color='r')  # faulty robots are plotted in red
    plot_point_set(p_fault_free, color='b')  # fault-free robots are plotted in blue
    plt.pause(1)
    plt.savefig('./result/%s%d_async.eps' % (method, t))


def plotResiBound(method, fixNeighbor, diff_nf_and_nf_approx_t, diff_nf_and_nf_approx):
    plt.figure(figsize=(5, 5))
    ax = plt.gca()
    if fixNeighbor:
        diff_set = set(diff_nf_and_nf_approx_t)
        diff_dict = {}
        for i in diff_set:
            diff_dict[i] = 0
            for j in diff_nf_and_nf_approx_t:
                if i == j:
                    diff_dict[i] += 1
        for i in diff_dict.keys():
            ax.vlines(x=i, ymin=0, ymax=diff_dict[i], color='firebrick', alpha=0.7, linewidth=2)
            plt.draw()
        plt.xlabel(r'$\tilde{n}_{f_i} - n_{f_i}$', fontsize=24)
        plt.ylabel("Number", fontsize=24)
    else:
        plt.plot(diff_nf_and_nf_approx)
        plt.draw()
        plt.xlabel("Iteration", fontsize=24)
        plt.ylabel(r'$\tilde{n}_{f_i} - n_{f_i}$', fontsize=24)
    # ax.xaxis.set_ticks(np.arange(-5, 15, 5))
    # ax.set_xticklabels(np.arange(-5, 15, 5))
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()
    plt.savefig('./result/diff_nf_%s_async.eps' % (method))


def plotValueChange(method, position_x_along_time, position_y_along_time):

    plt.figure(figsize=(5, 9))
    plt.subplot(2, 1, 1)
    plt.plot(position_x_along_time)
    plt.draw()
    plt.ylabel("Position (X)", fontsize=24)
    ax = plt.gca()
    # ax.xaxis.set_ticks(np.arange(-5, 55, 5))
    # ax.set_xticklabels(np.arange(-5, 55, 5))
    # ax.set_xticklabels([0, 5, 10, 15, 20])
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.subplot(2, 1, 2)
    plt.plot(position_y_along_time)
    plt.draw()
    plt.xlabel("Iteration", fontsize=24)
    plt.ylabel("Position (Y)", fontsize=24)
    ax = plt.gca()
    # ax.xaxis.set_ticks(np.arange(-5, 55, 5))
    # ax.set_xticklabels(np.arange(-5, 55, 5))
    # ax.set_xticklabels([0, 5, 10, 15, 20])
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()
    plt.savefig('./result/positionChange_%s_async.eps' % (method))
    plt.show()
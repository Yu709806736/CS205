from Proj1.Astar import *
import matplotlib.pyplot as plt

depths = [0, 2, 4, 8, 12, 16, 20, 24]
puzzles = {0: [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
           2: [[1, 2, 0], [4, 5, 3], [7, 8, 6]],
           4: [[1, 2, 3], [5, 0, 6], [4, 7, 8]],
           8: [[1, 3, 6], [5, 0, 2], [4, 7, 8]],
           12: [[1, 3, 6], [5, 0, 7], [4, 8, 2]],
           16: [[1, 6, 7], [5, 0, 3], [4, 8, 2]],
           20: [[7, 1, 2], [4, 8, 5], [6, 3, 0]],
           24: [[0, 7, 2], [4, 6, 1], [3, 5, 8]]}
goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

if __name__ == '__main__':
    depths_UC = []
    nodes_UC = []
    time_UC = []
    depths_MisP = []
    nodes_MisP = []
    time_MisP = []
    nodes_ManHat = []
    time_ManHat = []
    for i in depths:
        _, node, _, t = a_star(puzzles[i], 1, 1000, 5, False, False)
        if node != -1:
            depths_UC.append(i)
            nodes_UC.append(node)
            time_UC.append(t)
        _, node, _, t = a_star(puzzles[i], 2, 1000, 5, False, False)
        if node != -1:
            depths_MisP.append(i)
            nodes_MisP.append(node)
            time_MisP.append(t)
        _, node, _, t = a_star(puzzles[i], 3, 1000, 5, False, False)
        if node != -1:
            nodes_ManHat.append(node)
            time_ManHat.append(t)

    plt.plot(depths_UC, nodes_UC, label='UC')
    plt.plot(depths_MisP, nodes_MisP, label='MisP')
    plt.plot(depths, nodes_ManHat, label='ManHat')
    plt.title('Nodes Expanded vs Solution Depth')
    plt.legend()
    plt.savefig('nodes_expanded_depth.jpg')
    plt.show()

    plt.plot(depths_UC, time_UC, label='UC')
    plt.plot(depths_MisP, time_MisP, label='MisP')
    plt.plot(depths, time_ManHat, label='ManHat')
    plt.title('Running Time vs Solution Depth')
    plt.legend()
    plt.savefig('time_depth.jpg')
    plt.show()

import numpy as np
from queue import PriorityQueue


class DataPoint:
    """
        for data point objects
    """
    def __init__(self, idx: int, label: float, dis: float):
        """
        :param idx: index of this data point in the whole dataset
        :param label: class labels, 1.0 or 2.0
        :param dis: distance to the test input data point
        """
        self.idx = idx
        self.label = label
        self.dis = dis

    """
        The following four methods can be used for priority queue
    """
    def __lt__(self, other):
        return self.dis < other.dis

    def __gt__(self, other):
        return self.dis > other.dis

    def __le__(self, other):
        return self.dis <= other.dis

    def __ge__(self, other):
        return self.dis >= other.dis

    def __eq__(self, other):
        return self.idx == other.idx and self.label == other.label


class NearestNeighbor:
    def __init__(self, data, k=1):
        """
            create a k-Nearest Neighbor model
        :param data: input data without the data point being tested
        :param k: number of nearest neighbors needed, default: 1
        """
        self.data = data[:, 1:]
        self.labels = data[:, 0]
        self.k = k

    def clf(self, x):
        """
            classify
        :param x: input data point without label
        :return: predicted value
        """
        # only for k = 1 - find the nearest neighbor
        if self.k == 1:
            min = np.linalg.norm(self.data[0] - x)
            min_idx = 0
            for i, data in enumerate(self.data):
                dis = np.linalg.norm(data - x)
                if dis <= min:
                    min = dis
                    min_idx = i
            return self.labels[min_idx]

        # for k > 1 - use priority queue to find k nearest neighbors
        pq = PriorityQueue(self.k)
        cnt = [0, 0]
        for i, data in enumerate(self.data):
            pt = DataPoint(i, self.labels[i], np.linalg.norm(data - x))
            if pq.full():
                if pq.queue[0][1] > pt:
                    pq.get()
                    pq.put((-pt.dis, pt))
            else:
                pq.put((-pt.dis, pt))
        for i, (_, pt) in enumerate(pq.queue):
            if pt.label == 1.0:
                cnt[0] += 1
            else:
                cnt[1] += 1
        if cnt[0] > cnt[1]:
            return 1.0
        else:
            return 2.0

    def acc(self, data_pt):
        """
            return whether the classification is correct
        :param data_pt: input data point (with label)
        :return:
        """
        pred = self.clf(data_pt[1:])
        if data_pt[0] == pred:
            return 1
        else:
            return 0


def leave_one_out(data: np.ndarray, string=False):
    """
        leave-one-out strategy
    :param data: whole dataset
    :param string: whether to return a string form of accuracy, i.e., "xx.xx%". default: False
    :return: accuracy. "xx.xx%" format if string=True, otherwise return the float value
    """
    cor = 0
    for i in range(len(data)):
        if i == len(data) - 1:
            new_data = data[:-1]
        else:
            new_data = np.concatenate((data[:i], data[i + 1:]), axis=0)
        nn = NearestNeighbor(new_data)
        cor += nn.acc(data[i])
    acc = cor / len(data)
    if string:
        return acc_str(acc)
    else:
        return acc


def acc_str(accuracy):
    """
        convert accuracy to string
    :param accuracy: accuracy (float)
    :return: string representation of accuracy (xx.xx%)
    """
    return '{}%'.format(round(accuracy * 100, 2))

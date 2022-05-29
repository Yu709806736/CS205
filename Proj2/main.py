import numpy as np
from Proj2.feature_selection import forward_selection, backward_elimination
# from .feature_selection import forward_selection, backward_elimination
from sklearn.preprocessing import normalize
import os
import time
import matplotlib.pyplot as plt

data_path = './data'
files = [os.path.join(data_path, i) for i in os.listdir(data_path)]
dif = 0.01

if __name__ == '__main__':
    print('Welcome to Michael Yu\'s Feature Selection Algorithm')
    print('Please choose data files or enter the path')
    for i, file_path in enumerate(files):
        print('\t{0}) {1}'.format(i+1, file_path))
    file = input('Enter the path directly if your file is not in the list\n')
    dataset = file
    try:
        select = int(file)
        if select <= len(files):
            file = files[select-1]
        if select == 1:
            dataset = 'small'
        else:
            dataset = 'large'
    except Exception:
        pass
    algo = int(input('Type the number of the algorithm you want to run.\n'
                     '\t 1) Forward Selection\n'
                     '\t 2) Backward Elimination\n'))
    data = np.loadtxt(file)
    data[:, 1:] = normalize(data[:, 1:], axis=0)
    # print(data.shape)
    start = time.time()
    feat_sets = []
    accs = []
    end = 0.0
    if algo == 1:
        feat_sets, accs = forward_selection(data, dif)
        end = time.time()
        algo = 'forward'
    elif algo == 2:
        feat_sets, accs = backward_elimination(data, dif)
        end = time.time()
        algo = 'backward'
    else:
        exit(0)
    plt.bar(feat_sets, accs)
    plt.savefig('{0}_{1}_{2}.jpg'.format(dataset, algo, round(end-start, 3)))

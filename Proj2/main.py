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
    # get all data files in the data directory
    if os.path.exists(data_path):
        for i, file_path in enumerate(files):
            print('\t{0}) {1}'.format(i+1, file_path))
    file = input('Enter the path directly if your file is not in the list\n')
    dataset = os.path.splitext(file.split('\\')[-1])[0]
    try:
        # if input is a number - read file from the data directory
        select = int(file)
        if select <= len(files):
            file = files[select-1]
        if file.lower().find('large') != -1:
            dataset = 'large'
        elif file.lower().find('small') != -1:
            dataset = 'small'
    except Exception:
        pass
    algo = int(input('Type the number of the algorithm you want to run.\n'
                     '\t 1) Forward Selection\n'
                     '\t 2) Backward Elimination\n'))
    # read file
    data = np.loadtxt(file)
    print('The dataset has {0} features (not including the class attribute), with {1} instances.'
          .format(data.shape[1]-1, data.shape[0]))
    # normalize
    data[:, 1:] = normalize(data[:, 1:], axis=0)
    # timer start
    start = time.time()
    # list of feature subsets for each iteration in the algorithm
    feat_sets = []
    # list of accuracies for each iteration in the algorithm
    accs = []
    end = 0.0
    if algo == 1:
        feat_sets, accs = forward_selection(data, dif)
        # timer end
        end = time.time()
        algo = 'forward'
    elif algo == 2:
        feat_sets, accs = backward_elimination(data, dif)
        # timer end
        end = time.time()
        algo = 'backward'
    else:
        exit(0)

    # visualization
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.bar(feat_sets, accs)
    # modify x-ticks to make it look better
    # refer to https://blog.csdn.net/Poul_henry/article/details/82590392
    new_feat_sets = ['' for _ in range(len(feat_sets))]
    for i in range(len(feat_sets)):
        if len(feat_sets[i].split(',')) == (data.shape[1] + 3) // 2:
            new_feat_sets[i] = '{omit for space}'
            # tick.set_text('{omit for space}')
        elif len(feat_sets[i].split(',')) <= 4:
            new_feat_sets[i] = feat_sets[i]
    plt.xticks(feat_sets, new_feat_sets)
    fig.set_size_inches(20, 4)
    for i, tick in enumerate(ax.get_xticklabels()):
        s = new_feat_sets[i]
        if not s == '{omit for space}' and not s == '' and not s == '{All features}':
            tick.set_rotation(30)
    plt.savefig('output/{0}_{1}_{2}.jpg'.format(dataset, algo, round(end-start, 3)), bbox_inches='tight')
    print(round(end-start, 3))
    plt.show()

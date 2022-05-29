import numpy as np
import copy
from typing import List
from Proj2.nearest_neighbor import *


def forward_selection(data: np.ndarray, dif=0.01):
    features = {}
    new_data: np.ndarray = data[:, 0].reshape(-1, 1)
    total_best_acc = 0
    total_best_features = {}
    print('Beginning search.\n')
    features_str = '{'
    feature_sets = []
    accs = []
    while len(features) < data.shape[1] - 1:
        if not features_str == '{':
            features_str += ','
        best_acc = 0
        best_i = -1
        for i in range(1, data.shape[1]):
            if i in features.keys():
                continue
            # print(new_data.shape)
            # print(data[:, i].shape)
            test_data = np.concatenate((new_data, data[:, i].reshape(-1, 1)), axis=1)
            acc = leave_one_out(test_data)
            temp_str = features_str + str(i) + '}'
            print('\tUsing feature(s) {0} accuracy is {1}'.format(temp_str, acc_str(acc)))
            if acc > best_acc:
                best_i = i
                best_acc = acc
        features_str += str(best_i)
        features[best_i] = 1
        temp_str = features_str + '}'
        if total_best_acc < best_acc - dif:
            total_best_acc = best_acc
            total_best_features = copy.deepcopy(features)
            feature_sets.append(feat_str(features))
            accs.append(best_acc)
            print('\n')
        else:
            print('\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)')
        print('Feature set {0} was best, accuracy is {1}\n'.format(temp_str, acc_str(best_acc)))
        new_data = np.hstack((new_data, data[:, best_i].reshape(-1, 1)))
    features_str = feat_str(total_best_features)
    # print(total_best_features)
    print('\nFinished search!! The best feature subset is {0}, which has an accuracy of {1}'
          .format(features_str, acc_str(total_best_acc)))
    return feature_sets, accs


def backward_elimination(data: np.ndarray, dif=0.01):
    # features = dict([(key, 1) for key in range(1, data.shape[1])])
    # features_rm = [True for i in range(1, data.shape[1])]
    features = dict([(i, 1) for i in range(1, data.shape[1])])
    new_data = copy.deepcopy(data)
    total_best_acc = 0
    total_best_rm = []
    total_best_features = copy.deepcopy(features)
    print('Beginning search.\n')
    features_str = feat_str(features)
    feature_sets = []
    accs = []
    while len(features) > 1:
        features_str = features_str.strip('}')
        best_acc = 0
        best_key = -1
        best_i = -1
        for i, key in enumerate(features.keys()):
            if features[key] == 1:
                features[key] = 0
                temp_str = feat_str(features)
                # print(new_data[:, :i].shape)
                # print(new_data[:, i+1:].shape)
                test_data = np.concatenate((new_data[:, :i], new_data[:, i+1:]), axis=1)
                acc = leave_one_out(test_data)
                print('\tUsing feature(s) {0} accuracy is {1}'.format(temp_str, acc_str(acc)))
                if acc > best_acc:
                    best_key = key
                    best_i = i
                    best_acc = acc
                features[key] = 1
        features.pop(best_key)
        if total_best_acc - dif < best_acc:
            total_best_acc = best_acc
            total_best_features = copy.deepcopy(features)
            feature_sets.append(feat_str(features))
            accs.append(best_acc)
            # print(total_best_features)
            print('\n')
        else:
            print('\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)')
        temp_str = feat_str(features)
        print('Feature set {0} was best, accuracy is {1}\n'.format(temp_str, acc_str(best_acc)))
        new_data = np.concatenate((new_data[:, :best_i], new_data[:, best_i+1:]), axis=1)
    features_str = feat_str(total_best_features)
    # print(features_str)
    print('\nFinished search!! The best feature subset is {0}, which has an accuracy of {1}'
          .format(features_str, acc_str(total_best_acc)))
    return feature_sets, accs


def feat_str(features: dict):
    result = '{'
    for i, key in enumerate(features.keys()):
        if features[key] == 1:
            result += str(key)
            result += ','
    result = result.strip(',')
    result += '}'
    return result

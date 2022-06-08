import numpy as np
import copy
from typing import List
from Proj2.nearest_neighbor import *


def forward_selection(data: np.ndarray, dif=0.01):
    """
        forward selection method
    :param data: whole dataset
    :param dif: if the difference of accuracies of two feature subsets is
            under $dif$, choose the subset with fewer features
    :return: list of the best feature subsets for each iteration, list of the best accuracies for each iteration
    """
    # current feature subset
    features = {}
    # put the labels into the dataset to be tested
    new_data: np.ndarray = data[:, 0].reshape(-1, 1)
    # record the best performance
    total_best_acc = 0
    total_best_features = {}
    print('Beginning search.\n')
    # for generating the string of feature subset
    features_str = '{'
    # list of the best feature subsets for each iteration
    feature_sets = []
    # list of the highest accuracies for each iteration
    accs = []
    # loop when still have features that are not in the current dataset
    while len(features) < data.shape[1] - 1:
        # generate string of feature subset
        if not features_str == '{':
            features_str += ','
        # store the best performance in the current iteration
        best_acc = 0
        best_i = -1
        # try adding each feature that is not in the current subset
        for i in range(1, data.shape[1]):
            # if it is in the current feature subset
            if i in features.keys():
                continue
            # concatenate the new feature with the test data
            test_data = np.concatenate((new_data, data[:, i].reshape(-1, 1)), axis=1)
            # get the accuracy following leave-one-out strategy
            acc = leave_one_out(test_data)
            # features string for output
            temp_str = features_str + str(i) + '}'
            print('\tUsing feature(s) {0} accuracy is {1}'.format(temp_str, acc_str(acc)))
            # record best performance
            if acc > best_acc:
                best_i = i
                best_acc = acc
        # record the best feature into the test data
        features_str += str(best_i)
        features[best_i] = 1
        temp_str = features_str + '}'
        # record the best accuracy in this iteration (this number of features)
        accs.append(best_acc)
        # record the best feature subset in this iteration
        feature_sets.append(temp_str)
        # record the best of the whole set
        if total_best_acc < best_acc - dif:
            total_best_acc = best_acc
            total_best_features = copy.deepcopy(features)
            print('\n')
        else:
            print('\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)')
        print('Feature set {0} was best, accuracy is {1}\n'.format(temp_str, acc_str(best_acc)))
        # add the best feature into the test data
        new_data = np.hstack((new_data, data[:, best_i].reshape(-1, 1)))
    # generate string of feature subset for output
    features_str = feat_str(total_best_features)
    print('\nFinished search!! The best feature subset is {0}, which has an accuracy of {1}'
          .format(features_str, acc_str(total_best_acc)))
    feature_sets[-1] = '{All features}'
    return feature_sets, accs


def backward_elimination(data: np.ndarray, dif=0.01):
    # current feature subset
    features = dict([(i, 1) for i in range(1, data.shape[1])])
    # put the whole dataset into the test data
    new_data = copy.deepcopy(data)
    print('Beginning search.\n')
    # for generating the strings of feature subset
    features_str = feat_str(features)
    temp_str = feat_str(features)
    # list of the best feature subsets for each iteration
    feature_sets = []
    # list of the highest accuracies for each iteration
    accs = []
    # record the best performance
    total_best_features = copy.deepcopy(features)
    total_best_acc = leave_one_out(data)
    print('\tUsing feature(s) {0} accuracy is {1}'.format(temp_str, acc_str(total_best_acc)))
    accs.append(total_best_acc)
    feature_sets.append(copy.deepcopy(features))
    # loop when still have features that are not in the current dataset
    while len(features) > 1:
        # generate string of feature subset
        features_str = features_str.strip('}')
        # store the best performance in the current iteration
        best_acc = 0
        best_key = -1
        best_i = -1
        # try removing each feature that is in the current subset
        for i, key in enumerate(features.keys()):
            if features[key] == 1:
                # remove the feature from the current feature subset
                features[key] = 0
                # generate string of feature subset for output
                temp_str = feat_str(features)
                # remove the selected feature from the test data
                test_data = np.concatenate((new_data[:, :i+1], new_data[:, i+2:]), axis=1)
                # get the accuracy following leave-one-out strategy
                acc = leave_one_out(test_data)
                print('\tUsing feature(s) {0} accuracy is {1}'.format(temp_str, acc_str(acc)))
                # record best performance
                if acc > best_acc:
                    best_key = key
                    best_i = i
                    best_acc = acc
                # add the feature back into the current feature subset
                features[key] = 1
        # record the best feature into the test data
        features.pop(best_key)
        # record the best accuracy in this iteration (this number of features)
        accs.append(best_acc)
        # record the best feature subset in this iteration
        feature_sets.append(feat_str(features))
        # record the best of the whole set
        if total_best_acc - dif < best_acc:
            total_best_acc = best_acc
            total_best_features = copy.deepcopy(features)
            print('\n')
        else:
            print('\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)')
        # generate string of feature subset for output
        temp_str = feat_str(features)
        print('Feature set {0} was best, accuracy is {1}\n'.format(temp_str, acc_str(best_acc)))
        # remove the best feature from the test data
        new_data = np.concatenate((new_data[:, :best_i+1], new_data[:, best_i+2:]), axis=1)
    # generate string of feature subset for output
    features_str = feat_str(total_best_features)
    # print(features_str)
    feature_sets[0] = '{All features}'
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

# coding=utf-8
import csv
import math
import random

random.seed(1234)  # fix randomness


def kNN(k, train_set, test_set):
    """
    the unweighted k-NN algorithm using Euclidean distance as the metric

    :param k: the k value, i.e, how many neighbors to consider
    :param train_set: training set, a list of lists where each nested list is a training instance
    :param test_set: test set, a list of lists where each nested list is a test instance
    :return: percent accuracy for the test set, e.g., 78.42
    """
    
    """
    rows = []
    with open(pathOfInput) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            row.append(altitude_value)
            rows.append(row)
        # print(rows)
    csv_file.close()

    """

    train_instances = []
    with open(train_set) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            train_instances.append(row)

    test_instances = []
    with open(test_set) as csv_file_2:
        csv_reader_2 = csv.reader(csv_file_2, delimiter=',')
        for row in csv_reader_2:
            test_instances.append(row)

    neighbors_distance_list = []  # sublist - first element = index, second = distance, third = label
    for line in train_instances:
        # print(line)
        line_length = len(line)
        # print("length = {}".format(line_length))
        label = line[line_length - 1]
        # print("label of instance = {}".format(label))
        for feature in line[:line_length - 1]:
            tmp_distance = 0.0
            for index, feature_2 in enumerate(line[:line_length - 1]):
                if feature == feature_2:
                    continue
                else:
                    tmp_distance += euclidean_distance(float(feature), float(feature_2))
            # calculate one line with all others
            # when calculating chech each features
    pass


def find_best_k(train_set, test_set, num_folds):
    """
    finds the best k value by using K-fold cross validation. Try at least 10 different k values. Possible choices
    can be: 1, 3, 5, 7, 9, 11, 13, 15, 17, 19. Besides the return value, as a side effect, print each k value and
    the corresponding validation accuracy to the screen as a tuple. As an example,
    (1, 78.65)
    (3, 79.12)
    ...
    (19, 76.99)

    :param train_set: training set, a list of lists where each nested list is a training instance
    :param test_set: test set, a list of lists where each nested list is a test instance
    :param num_folds: the K value in K-fold cross validation
    :return: a tuple, best k value and percent accuracy for the test set using the best k value, e.g., (3, 80.06)
    """
    pass


def euclidean_distance(value1, value2):
    return (value1 ** 2 + value2 ** 2) ** 0.5


kNN(3, "task1_test.txt", "task1_train.txt")

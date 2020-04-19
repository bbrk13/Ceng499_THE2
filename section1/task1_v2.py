# Example of making predictions
import csv
import math
from math import sqrt


def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1) - 1):
        distance += (row1[i] - row2[i]) ** 2
    return sqrt(distance)


def get_neighbors(train, test_row, num_neighbors):
    distances = list()
    for train_row in train:
        dist = euclidean_distance(test_row, train_row)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append(distances[i][0])
    return neighbors


# Make a classification prediction with neighbors
def predict_classification(train, test_row, num_neighbors):
    neighbors = get_neighbors(train, test_row, num_neighbors)
    output_values = [row[-1] for row in neighbors]
    prediction = max(set(output_values), key=output_values.count)
    return prediction


def get_test_instances_from_file(path_of_test_set):
    test_instances_local = []

    with open(path_of_test_set) as csv_file_2:
        csv_reader_2 = csv.reader(csv_file_2, delimiter=',')
        for row in csv_reader_2:
            tmp_row = []
            length_of_row = len(row)
            for index in range(length_of_row - 1):
                tmp_row.append(float(row[index]))
            tmp_row.append(row[length_of_row - 1])
            # print("new row = {}".format(tmp_row))
            test_instances_local.append(tmp_row)
    return test_instances_local


def get_train_instances_from_file(path_of_train_set):
    train_instances_local = []

    with open(path_of_train_set) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            tmp_row = []
            length_of_row = len(row)
            for index in range(length_of_row - 1):
                tmp_row.append(float(row[index]))
            tmp_row.append(row[length_of_row - 1])
            train_instances_local.append(tmp_row)
    return train_instances_local


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def find_best_k(train_instances, test_instances, number_of_folds):
    best_k = -1
    best_accuracy = -1
    for i in range(1, 20, 2):
        test_number = 0.0
        true_classification_number = 0.0
        for line_i in test_instances:
            test_number += 1.0
            prediction = predict_classification(train_instances, line_i, i)
            if line_i[-1] == prediction:
                true_classification_number += 1.0
                # print('Expected {}, Got {} TRUE'.format(line_i[-1], prediction))
            # else:
            # print('Expected {}, Got {} FALSE'.format(line_i[-1], prediction))
        test_accuracy = (true_classification_number * 100) / test_number
        # test_accuracy = test_accuracy * 100
        # test_accuracy = truncate(test_accuracy, 3)
        if test_accuracy > best_accuracy:
            best_accuracy = test_accuracy
            best_k = i
        print("k = {}, test accuracy = {}".format(i, test_accuracy))
    print("best k = {}, best accuracy = {}".format(best_k, best_accuracy))


train_instances = get_train_instances_from_file("task1_train.txt")
test_instances = get_test_instances_from_file("task1_test.txt")

find_best_k(train_instances, test_instances, 5)

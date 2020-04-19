import csv
import random
from statistics import mode

random.seed(1234)  # fix randomness


def kNN(k, train_set, test_set):
    """
    the unweighted k-NN algorithm using Euclidean distance as the metric

    :param k: the k value, i.e, how many neighbors to consider
    :param train_set: training set, a list of lists where each nested list is a training instance
    :param test_set: test set, a list of lists where each nested list is a test instance
    :return: percent accuracy for the test set, e.g., 78.42
    """

    true_positives_and_negatives = 0.0
    total_number_of_test_instances = 0.0

    for line_index, line in enumerate(test_set):
        total_number_of_test_instances += 1.0
        neighbors_distance_list = []  # sublist - first element = index, second = distance, third = label
        line_length = len(line)
        real_label = line[line_length - 1]

        for index1, line2 in enumerate(train_set):
            total_distance = 0.0
            line_length2 = len(line2)
            label2 = line2[line_length2 - 1]

            """for index2, feature in enumerate(line2[:line_length2 - 1]):
                tmp_distance = euclidean_distance(float(feature), float(line[index2]))
                total_distance += tmp_distance"""
            # print("line = {}".format(line))
            # print("line2 = {}".format(line2))
            total_distance = euclidean_distance(line, line2)

            tmp_list = []
            tmp_list.append(index1)
            tmp_list.append(total_distance)
            tmp_list.append(label2)
            neighbors_distance_list.append(tmp_list)

        neighbors_distance_list.sort(key=get_its_distance)
        label_list = []
        for index3 in range(k):
            label_list.append(neighbors_distance_list[index3][2])

        predicted_label = mode(label_list)
        if predicted_label == real_label:
            true_positives_and_negatives += 1.0

    test_accuracy = true_positives_and_negatives / total_number_of_test_instances
    return test_accuracy

    pass


def get_its_distance(list_parameter):
    return list_parameter[1]


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

    total_data = train_set
    length_of_total_data = len(total_data)
    batch_size = length_of_total_data / num_folds
    batch_size = round(batch_size)
    new_train_data = []
    new_test_data = []

    for index1 in range(num_folds):
        tmp_train_list = []
        tmp_test_list = []

        for index2, entry in enumerate(total_data):
            if (index1 * batch_size) <= index2 < (index1 + 1) * batch_size:
                tmp_test_list.append(entry)
            else:
                tmp_train_list.append(entry)

        new_train_data.append(tmp_train_list)
        new_test_data.append(tmp_test_list)

    result_list = []

    random.shuffle(new_test_data)
    random.shuffle(new_train_data)

    for index4 in range(1, 20, 2):
        total_test_accuracy = 0.0

        for index3 in range(num_folds):
            partial_test_accuracy = kNN(index4, new_train_data[index3], new_test_data[index3])
            total_test_accuracy += partial_test_accuracy

        tmp_tuple = (index4, total_test_accuracy / num_folds)
        print(tmp_tuple)
        result_list.append(tmp_tuple)

    result_list.sort(key=get_tuple_second, reverse=True)
    return result_list[0]
    pass


def get_tuple_second(tuple_parameter):
    return tuple_parameter[1]


def euclidean_distance(vector1, vector2):
    # return (value1 ** 2 + value2 ** 2) ** 0.5
    distance = 0.0
    for i in range(len(vector1) - 1):
        distance += (vector1[i] - vector2[i]) ** 2
    return distance ** 0.5


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


train_instances = get_train_instances_from_file("task1_train.txt")
test_instances = get_test_instances_from_file("task1_test.txt")
# k = 3
# test_accuracy = kNN(k, train_instances, test_instances)
# print("k = {}, test accuracy = {}".format(k, test_accuracy))

result = find_best_k(train_instances, test_instances, 5)
print("best k is {} | test accuracy: {} ".format(result[0], result[1]))

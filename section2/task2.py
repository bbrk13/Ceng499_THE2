import csv
import math
import matplotlib.pyplot as plt
import random
from statistics import mode


def read_dataset(file_path):
    file = open(file_path, 'r')
    lines = file.readlines()
    tmp_list = []
    for line in lines:
        tmp_line = line.split(" ")
        tmp_line[1] = tmp_line[1][:len(tmp_line[1]) - 2]
        tmp_line[0] = float(tmp_line[0])
        tmp_line[1] = float(tmp_line[1])
        tmp_list.append(tmp_line)
    return tmp_list


def hac(dataset, cluster_number, critarion_type):
    initial_matrix_dataset = initial_matrix(dataset)
    current_number_of_clusters = len(initial_matrix_dataset)
    current_clusters = make_deep_copy(initial_matrix_dataset)
    # print_matrix(current_clusters)
    while current_number_of_clusters > cluster_number:
        if critarion_type == 1:
            indexes_of_the_mergable_clusters = find_clusters_single_link(current_clusters)
            # print(
            #    "single linkage, indexes of mergable clusters is {} and {}".format(indexes_of_the_mergable_clusters[0],
            #                                                                       indexes_of_the_mergable_clusters[1]))
            new_cluster = merge_two_cluster(current_clusters[indexes_of_the_mergable_clusters[0]],
                                            current_clusters[indexes_of_the_mergable_clusters[1]])
            # print("cluster which will be deleted {}".format(indexes_of_the_mergable_clusters[0]))
            # print("cluster which will be deleted {}".format(indexes_of_the_mergable_clusters[1]))
            current_clusters.remove(current_clusters[indexes_of_the_mergable_clusters[0]])
            if indexes_of_the_mergable_clusters[0] < indexes_of_the_mergable_clusters[1]:
                indexes_of_the_mergable_clusters[1] -= 1
            current_clusters.remove(current_clusters[indexes_of_the_mergable_clusters[1]])
            current_clusters.append(new_cluster)
            current_number_of_clusters -= 1
        elif critarion_type == 2:
            # print("complete linkage")
            indexes_of_the_mergable_clusters = find_clusters_complete_link(current_clusters)

            # print(
            #    "single linkage, indexes of mergable clusters is {} and {}".format(indexes_of_the_mergable_clusters[0],
            #                                                                       indexes_of_the_mergable_clusters[1]))

            new_cluster = merge_two_cluster(current_clusters[indexes_of_the_mergable_clusters[0]],
                                            current_clusters[indexes_of_the_mergable_clusters[1]])
            current_clusters.remove(current_clusters[indexes_of_the_mergable_clusters[0]])
            if indexes_of_the_mergable_clusters[0] < indexes_of_the_mergable_clusters[1]:
                indexes_of_the_mergable_clusters[1] -= 1
            current_clusters.remove(current_clusters[indexes_of_the_mergable_clusters[1]])
            current_clusters.append(new_cluster)
            current_number_of_clusters -= 1
        elif critarion_type == 3:
            # print("average linkage")
            indexes_of_the_mergable_clusters = find_clusters_avg_link(current_clusters)

            # print(
            #    "single linkage, indexes of mergable clusters is {} and {}".format(indexes_of_the_mergable_clusters[0],
            #                                                                       indexes_of_the_mergable_clusters[1]))

            new_cluster = merge_two_cluster(current_clusters[indexes_of_the_mergable_clusters[0]],
                                            current_clusters[indexes_of_the_mergable_clusters[1]])
            current_clusters.remove(current_clusters[indexes_of_the_mergable_clusters[0]])
            if indexes_of_the_mergable_clusters[0] < indexes_of_the_mergable_clusters[1]:
                indexes_of_the_mergable_clusters[1] -= 1
            current_clusters.remove(current_clusters[indexes_of_the_mergable_clusters[1]])
            current_clusters.append(new_cluster)
            current_number_of_clusters -= 1
        elif critarion_type == 4:
            # print("centroid linkage")
            indexes_of_the_mergable_clusters = find_clusters_centroid_link(current_clusters)

            # print(
            #    "single linkage, indexes of mergable clusters is {} and {}".format(indexes_of_the_mergable_clusters[0],
            #                                                                       indexes_of_the_mergable_clusters[1]))

            new_cluster = merge_two_cluster(current_clusters[indexes_of_the_mergable_clusters[0]],
                                            current_clusters[indexes_of_the_mergable_clusters[1]])
            current_clusters.remove(current_clusters[indexes_of_the_mergable_clusters[0]])
            if indexes_of_the_mergable_clusters[0] < indexes_of_the_mergable_clusters[1]:
                indexes_of_the_mergable_clusters[1] -= 1
            current_clusters.remove(current_clusters[indexes_of_the_mergable_clusters[1]])
            current_clusters.append(new_cluster)
            current_number_of_clusters -= 1
        else:
            print("wrong critarion type!")
            current_number_of_clusters -= 1

    # print_matrix(current_clusters)
    return current_clusters


def find_clusters_avg_link(current_clusters):
    minimum_avg_distance = math.inf
    min_x = 0
    min_y = 0

    for index_x, each_cluster_x in enumerate(current_clusters):
        for index_y, each_cluster_y in enumerate(current_clusters):
            total_distance = 0.0
            for each_tuple_point_x in each_cluster_x:
                for each_tuple_point_y in each_cluster_y:
                    total_distance += calculate_euclidean_distance(each_tuple_point_x, each_tuple_point_y)
            tmp_avg = total_distance / (len(each_cluster_x) * len(each_cluster_y))
            if tmp_avg < minimum_avg_distance and index_x != index_y:
                minimum_avg_distance = tmp_avg
                min_x = index_x
                min_y = index_y
    return [min_x, min_y]


def find_clusters_centroid_link(current_clusters):
    min_x = 0
    min_y = 0
    total_x_coord = [0, 0]
    total_y_coord = [0, 0]

    minimum_distance = math.inf
    for index_x, each_cluster_x in enumerate(current_clusters):
        for index_y, each_cluster_y in enumerate(current_clusters):

            for each_tuple_point_x in each_cluster_x:
                # print("each_tuple_point_x[1] = {}".format(each_tuple_point_x[1]))
                total_x_coord[0] += each_tuple_point_x[0]
                total_x_coord[1] += each_tuple_point_x[1]
            total_x_coord[0] = total_x_coord[0] / len(each_cluster_x)
            total_x_coord[1] = total_x_coord[1] / len(each_cluster_x)

            for each_tuple_point_y in each_cluster_y:
                total_y_coord[0] += each_tuple_point_y[0]
                total_y_coord[1] += each_tuple_point_y[1]
            total_y_coord[0] = total_y_coord[0] / len(each_cluster_y)
            total_y_coord[1] = total_y_coord[1] / len(each_cluster_y)

            tmp_avg = calculate_euclidean_distance(total_x_coord, total_y_coord)

            if tmp_avg < minimum_distance and index_x != index_y:
                minimum_distance = tmp_avg
                min_y = index_y
                min_x = index_x

    return [min_x, min_y]


def find_clusters_single_link(current_clusters):
    minimum_x = 0
    minimum_y = 0
    minimum_distance = math.inf
    for index_x, each_cluster_x in enumerate(current_clusters):
        for index_y, each_cluster_y in enumerate(current_clusters):
            for each_tuple_point_x in each_cluster_x:
                for each_tuple_point_y in each_cluster_y:
                    if calculate_euclidean_distance(each_tuple_point_x, each_tuple_point_y) < minimum_distance and \
                            calculate_euclidean_distance(each_tuple_point_x,
                                                         each_tuple_point_y) != 0.0 and index_x != index_y:
                        minimum_distance = calculate_euclidean_distance(each_tuple_point_x, each_tuple_point_y)
                        minimum_x = index_x
                        minimum_y = index_y
    return [minimum_x, minimum_y]


def find_clusters_complete_link(current_clusters):
    result_index_1 = 0
    result_index_2 = 0
    global_minimum_distance = math.inf

    for index_x, each_cluster_x in enumerate(current_clusters):
        for index_y, each_cluster_y in enumerate(current_clusters):
            local_maximum_distance = -1
            for each_tuple_point_x in each_cluster_x:
                for each_tuple_point_y in each_cluster_y:
                    if calculate_euclidean_distance(each_tuple_point_x, each_tuple_point_y) > local_maximum_distance:
                        local_maximum_distance = calculate_euclidean_distance(each_tuple_point_x, each_tuple_point_y)

            if local_maximum_distance < global_minimum_distance and local_maximum_distance != 0 and index_x != index_y:
                result_index_1 = index_x
                result_index_2 = index_y
                global_minimum_distance = local_maximum_distance

    return [result_index_1, result_index_2]


def make_deep_copy(cluster_list):
    tmp_list = []

    for line in cluster_list:
        tmp_cluster = []
        for element in line:
            tmp_cluster.append(element)
        tmp_list.append(tmp_cluster)

    return tmp_list


def calculate_euclidean_distance(tuple_x, tuple_y):
    x1 = tuple_x[0]
    x2 = tuple_y[0]
    y1 = tuple_x[1]
    y2 = tuple_y[1]
    result = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    # result = round(result, 2)
    return result


def print_matrix(matrix):
    for row in matrix:
        print(row)
        print("new row -------------")


def initial_matrix(dataset):
    result = []
    for line in dataset:
        tmp_cluster = []
        tmp_cluster.append(line)
        result.append(tmp_cluster)
    return result


def merge_two_cluster(cluster1, cluster2):
    new_merged_cluster = []
    for each_point in cluster1:
        new_merged_cluster.append(each_point)

    for each_point2 in cluster2:
        if each_point2 not in new_merged_cluster:
            new_merged_cluster.append(each_point2)

    return new_merged_cluster


def plot_graph(list_of_clusters):
    number_of_clusters = len(list_of_clusters)
    if number_of_clusters == 2:
        first_cluster = list_of_clusters[0]
        second_cluster = list_of_clusters[1]
        for i in first_cluster:
            plt.plot(i[0], i[1], 'bo')
        for i in second_cluster:
            plt.plot(i[0], i[1], 'ro')
        plt.show()
    elif number_of_clusters == 4:
        first_cluster = list_of_clusters[0]
        second_cluster = list_of_clusters[1]
        third_cluster = list_of_cluster[2]
        fourth_cluster = list_of_cluster[3]
        for i in first_cluster:
            plt.plot(i[0], i[1], 'bo')
        for i in second_cluster:
            plt.plot(i[0], i[1], 'ro')
        for i in third_cluster:
            plt.plot(i[0], i[1], 'go')
        for i in fourth_cluster:
            plt.plot(i[0], i[1], 'yo')
        plt.show()


dataset_1_path = "dataset1.txt"
dataset_2_path = "dataset2.txt"
dataset_3_path = "dataset3.txt"
dataset_4_path = "dataset4.txt"

dataset_1 = read_dataset(dataset_1_path)
dataset_2 = read_dataset(dataset_2_path)
dataset_3 = read_dataset(dataset_3_path)
dataset_4 = read_dataset(dataset_4_path)

list_of_cluster = hac(dataset_1, 2, 4)
plot_graph(list_of_cluster)


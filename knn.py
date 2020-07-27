import random
import math


def make_data(data_list):
    f = open("HC_Body_Temperature.txt", "r")
    x = list(f.read().splitlines())
    for i in range(len(x)):
        if x[i][8] + x[i][9] == "-1":
            temper = float(x[i][0] + x[i][1] + x[i][2] + x[i][3] + x[i][4])
            gender = int(x[i][8] + x[i][9])
            heart = int(x[i][14] + x[i][15])
        else:
            temper = float(x[i][0] + x[i][1] + x[i][2] + x[i][3] + x[i][4])
            gender = int(x[i][8] + x[i][9])
            heart = int(x[i][13] + x[i][14])
        data_list.append((temper, heart, gender))


def p_(p, x1, y1, x2, y2):
    if p == 1:
        dist = abs((x1 - x2) + (y1 - y2))
    elif p == 2:
        dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    else:
        dist = max(abs(x1 - x2), abs(y1 - y2))

    return dist


def p_func(p, k, test_set, train_set):
    result = 0
    for i in range(0, 65):
        dictionary_points = list()
        x1 = test_set[i][0]
        y1 = test_set[i][1]
        for j in range(0, 65):
            x2 = train_set[j][0]
            y2 = train_set[j][1]
            dist = p_(p, x1, y1, x2, y2)
            dictionary_points.append((j, dist))

        dictionary_points.sort(key=lambda x: x[1])
        sum = 0
        for neighbor in range(k):
            sum += train_set[dictionary_points[neighbor][0]][2]

        if sum > 0 and test_set[i][2] == 1:
            result += 1
        if sum < 0 and test_set[i][2] == -1:
            result += 1
    result /= 65
    return result


def knn(itr):
    print("Start the KNN algorithm: ",'\n')
    data_set = list()
    make_data(data_set)
    list_of_p_1 = list()
    list_of_p_2 = list()
    list_of_p_in = list()
    for j in range(0, 11):
        list_of_p_in.append(0)
        list_of_p_2.append(0)
        list_of_p_1.append(0)

    for i in range(0, itr):
        random.shuffle(data_set)
        for k in range(1, 10, 2):
            #  Test
            list_of_p_1[k] += p_func(1, k, data_set[0:65], data_set[65:130])
            list_of_p_2[k] += p_func(2, k, data_set[0:65], data_set[65:130])
            list_of_p_in[k] += p_func(0, k, data_set[0:65], data_set[65:130])
            #  Train
            list_of_p_1[k+1] += p_func(1, k, data_set[65:130], data_set[65:130])
            list_of_p_2[k+1] += p_func(2, k, data_set[65:130], data_set[65:130])
            list_of_p_in[k+1] += p_func(0, k, data_set[65:130], data_set[65:130])

    print("For p_1 distance the prediction results are: ")
    print("Test: when k=1: " + str(list_of_p_1[1] / itr))
    print("Train: when k=1: " + str(list_of_p_1[2] / itr))
    print("Test: when k=3: " + str(list_of_p_1[3] / itr))
    print("Train: when k=3: " + str(list_of_p_1[4] / itr))
    print("Test: when k=5: " + str(list_of_p_1[5] / itr))
    print("Train: when k=5: " + str(list_of_p_1[6] / itr))
    print("Test: when k=7: " + str(list_of_p_1[7] / itr))
    print("Train: when k=7: " + str(list_of_p_1[8] / itr))
    print("Test: when k=9: " + str(list_of_p_1[9] / itr))
    print("Train: when k=9: " + str(list_of_p_1[10] / itr))
    print("")
    print("For p_2 distance the prediction results are: ")
    print("Test: when k=1: " + str(list_of_p_2[1] / itr))
    print("Train: when k=1: " + str(list_of_p_2[2] / itr))
    print("Test: when k=3: " + str(list_of_p_2[3] / itr))
    print("Train: when k=3: " + str(list_of_p_2[4] / itr))
    print("Test: when k=5: " + str(list_of_p_2[5] / itr))
    print("Train: when k=5: " + str(list_of_p_2[6] / itr))
    print("Test: when k=7: " + str(list_of_p_2[7] / itr))
    print("Train: when k=7: " + str(list_of_p_2[8] / itr))
    print("Test: when k=9: " + str(list_of_p_2[9] / itr))
    print("Train: when k=9: " + str(list_of_p_2[10] / itr))
    print("")
    print("For p_infinite distance the prediction results are:")
    print("Test: when k=1: " + str(list_of_p_in[1] / itr))
    print("Train: when k=1: " + str(list_of_p_in[2] / itr))
    print("Test: when k=3: " + str(list_of_p_in[3] / itr))
    print("Train: when k=3: " + str(list_of_p_in[4] / itr))
    print("Test: when k=5: " + str(list_of_p_in[5] / itr))
    print("Train: when k=5: " + str(list_of_p_in[6] / itr))
    print("Test: when k=7: " + str(list_of_p_in[7] / itr))
    print("Train: when k=7: " + str(list_of_p_in[8] / itr))
    print("Test: when k=9: " + str(list_of_p_in[9] / itr))
    print("Train: when k=9: " + str(list_of_p_in[10] / itr))


knn(500)

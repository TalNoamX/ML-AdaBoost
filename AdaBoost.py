import random
import math
from itertools import combinations


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


def check_in_rec(rect, point, direction):
    if rect[0][0] < rect[1][0]:
        x1 = rect[0][0]
        x2 = rect[1][0]
    else:
        x1 = rect[1][0]
        x2 = rect[0][0]
    if rect[0][1] < rect[1][1]:
        y1 = rect[0][1]
        y2 = rect[1][1]
    else:
        y1 = rect[1][1]
        y2 = rect[0][1]
    if x1 == x2:
        x1 = 0
    if y1 == y2:
        y1 = 0
    if direction == "+":
        if point[2] == 1:
            if x1 <= point[0] <= x2:
                if y1 <= point[1] <= y2:
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            if x1 <= point[0] <= x2:
                if y1 <= point[1] <= y2:
                    return 0
                else:
                    return 1
            else:
                return 1
    else:
        if point[2] == -1:
            if x1 <= point[0] <= x2:
                if y1 <= point[1] <= y2:
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            if x1 <= point[0] <= x2:
                if y1 <= point[1] <= y2:
                    return 0
                else:
                    return 1
            else:
                return 1


def Rectangle(data_set, weights):
    train_list = list()
    point_position = list()

    for p in range(0, 65):
        train_list.append(data_set[p])

    comb_list = list(combinations(train_list, 2))
    error = 1
    direction = ""
    best_rect = tuple()

    for i in comb_list:
        temp_rect = ((i[0][0], i[0][1]), (i[1][0], i[1][1]))
        temp_error1 = 0
        temp_error2 = 0
        point_position1 = list()
        point_position2 = list()
        for p in range(0, 65):
            if check_in_rec(temp_rect, train_list[p], "+") == 0:
                temp_error1 = temp_error1 + weights[p]
                point_position1.append(0)
            else:
                point_position1.append(1)

            if check_in_rec(temp_rect, train_list[p], "-") == 0:
                temp_error2 = temp_error2 + weights[p]
                point_position2.append(0)
            else:
                point_position2.append(1)

        if temp_error1 <= temp_error2:
            temp_error = temp_error1
            temp_direction = "+"
            temp_point_position = point_position1
        else:
            temp_error = temp_error2
            temp_direction = "-"
            temp_point_position = point_position2

        if temp_error < error:
            best_rect = temp_rect
            error = temp_error
            direction = temp_direction
            point_position = temp_point_position

    return (best_rect, error, direction, point_position)


def check_in_circle(circle, point, direction):
    dist = math.hypot(circle[0][0] - circle[1][0], circle[0][1] - circle[1][1])
    temp_dist = math.hypot(circle[0][0] - point[0], circle[0][1] - point[1])
    if direction == "+":
        if point[2] == 1:
            if temp_dist <= dist:
                return 1
            else:
                return 0
        else:
            if temp_dist <= dist:
                return 0
            else:
                return 1
    else:
        if point[2] == -1:
            if temp_dist <= dist:
                return 1
            else:
                return 0
        else:
            if temp_dist <= dist:
                return 0
            else:
                return 1


def Circle(data_set, weights):
    train_list = list()
    point_position = list()

    for p in range(0, 65):
        train_list.append(data_set[p])

    comb_list = list(combinations(train_list, 2))
    error = 1
    direction = ""
    best_circle = tuple()

    for i in comb_list:
        temp_circle = ((i[0][0], i[0][1]), (i[1][0], i[1][1]))
        temp_error1 = 0
        temp_error2 = 0
        point_position1 = list()
        point_position2 = list()
        for p in range(0, 65):
            if check_in_circle(temp_circle, train_list[p], "+") == 0:
                temp_error1 = temp_error1 + weights[p]
                point_position1.append(0)
            else:
                point_position1.append(1)

            if check_in_circle(temp_circle, train_list[p], "-") == 0:
                temp_error2 = temp_error2 + weights[p]
                point_position2.append(0)
            else:
                point_position2.append(1)

        if temp_error1 <= temp_error2:
            temp_error = temp_error1
            temp_direction = "+"
            temp_point_position = point_position1
        else:
            temp_error = temp_error2
            temp_direction = "-"
            temp_point_position = point_position2

        if temp_error < error:
            best_circle = temp_circle
            error = temp_error
            direction = temp_direction
            point_position = temp_point_position

    return (best_circle, error, direction, point_position)


def weights_calc(weights, point_position, alpha):
    sum_weights = 0
    for p in range(0, 65):
        if point_position[p] == 1:
            weights[p] = weights[p] * math.exp((-1) * alpha)
            sum_weights += weights[p]
        else:
            weights[p] = weights[p] * math.exp(alpha)
            sum_weights += weights[p]
    for p in range(0, 65):
        weights[p] /= sum_weights


def AdaBoost(shape, r, data_set):
    rules_set = list()
    weights = list()
    for i in range(0, 65):
        weights.append(1 / 65)
    for t in range(0, r + 1):
        if shape == "Rectangle":
            (h_i, eps, direction, point_position) = Rectangle(data_set, weights)
        else:
            (h_i, eps, direction, point_position) = Circle(data_set, weights)

        alpha = (1 / 2) * math.log((1 - eps) / eps)
        rules_set.append((h_i, alpha, direction))
        weights_calc(weights, point_position, alpha)
    return rules_set


def T(rules_set, data_set, shape):
    success_test = 0
    for p in range(65, 130):
        sum_test = 0
        for rule in rules_set:
            if shape == "Rectangle":
                if check_in_rec(rule[0], data_set[p], rule[2]) == 1:
                    sum_test += rule[1] * data_set[p][2]
                else:
                    sum_test += rule[1] * data_set[p][2] * (-1)
            else:
                if check_in_circle(rule[0], data_set[p], rule[2]) == 1:
                    sum_test += rule[1] * data_set[p][2]
                else:
                    sum_test += rule[1] * data_set[p][2] * (-1)

        if sum_test >= 0 and data_set[p][2] == 1:
            success_test += 1
        if sum_test < 0 and data_set[p][2] == -1:
            success_test += 1

    success_train = 0
    for p in range(0, 65):
        sum_train = 0
        for rule in rules_set:
            if shape == "Rectangle":
                if check_in_rec(rule[0], data_set[p], rule[2]) == 1:
                    sum_train += rule[1] * data_set[p][2]
                else:
                    sum_train += rule[1] * data_set[p][2] * (-1)
            else:
                if check_in_circle(rule[0], data_set[p], rule[2]) == 1:
                    sum_train += rule[1] * data_set[p][2]
                else:
                    sum_train += rule[1] * data_set[p][2] * (-1)

        if sum_train >= 0 and data_set[p][2] == 1:
            success_train += 1
        if sum_train < 0 and data_set[p][2] == -1:
            success_train += 1

    return (success_test / 65, success_train / 65)


def main(shape):
    print("Start the algorithm with:  " + str(shape))
    data_set = list()
    make_data(data_set)
    for r in range(0, 8):
        test_error_list = list()
        train_error_list = list()
        for i in range(0, 100):
            random.shuffle(data_set)
            rules_set = AdaBoost(shape, r, data_set)
            (error_test, error_train) = T(rules_set, data_set, shape)
            test_error_list.append(error_test)
            train_error_list.append(error_train)

        avg_test = 0
        avg_train = 0
        for e in range(0, 100):
            avg_test += test_error_list[e]
            avg_train += train_error_list[e]

        avg_test = avg_test / len(test_error_list)
        avg_train = avg_train / len(train_error_list)
        print("..")
        print("The average *train* accuracy for round: " + str(r + 1) + " is:  " + str(avg_train))
        print("The average *test* accuracy for round: " + str(r + 1) + " is:  " + str(avg_test))
    print("Finished")
    return 0

main("Rectangle")
main("Circle")

# flag = True
# while (flag):
#     shape = input("Enter Rectangle/Circle/Exit: ")
#     if shape == "Rectangle":
#         main(shape)
#     if shape == "Circle":
#         main(shape)
#     if shape == "Exit":
#         flag = False
#     else:
#         print("Wrong input try again.")


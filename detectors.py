from math import *


def deviation(sample_array):
    average_value = 0
    for element in sample_array:
        average_value = average_value + element
    average_value = average_value / (len(sample_array))
    deviation_sum = 0
    for element in sample_array:
        deviation_sum = deviation_sum + (pow((element - average_value), 2))
    standard_deviation = sqrt(deviation_sum / (len(sample_array) - 1))
    return standard_deviation, average_value


def detect_anomaly(old_data, new_data, measurements_per_second):
    # soll checken ob 1. array leer ist
    if old_data:
        deviation_array = []
        value = 0
        for i in range(measurements_per_second):
            if(i == 0):
                deviation_array = old_data
            else:
                deviation_array = old_data[i:measurements_per_second] + \
                    new_data[0:i]
            value = new_data[i]
            print(deviation_array)
            print(value)
            standard_deviation, average_value = deviation(deviation_array)
            max_accepted_value = 3 * standard_deviation + \
                sqrt(pow(average_value, 2))
            min_accepted_value = sqrt(
                pow(average_value, 2)) - 3 * standard_deviation
            if sqrt(pow(value, 2)) > max_accepted_value or sqrt(pow(value, 2)) < min_accepted_value:
                return(True)
    return(False)


def detect_fall(sample_array, measurements_per_second):
    max_acceleration = -6
    for i in range(measurements_per_second - 1):
        acceleration = (
            sample_array[i + 1] - sample_array[i]) / (1 / measurements_per_second)
        if (acceleration > max_acceleration):
            return(True)
    return(False)


def detect_fast_comeback_acceleration(sample_array, measurements_per_second):
    max_acceleration = -1
    average_acceleration = 0
    for i in range(measurements_per_second - 1):
        average_acceleration = average_acceleration + \
            (sample_array[i + 1] - sample_array[i]) / \
            (1 / measurements_per_second)
    average_acceleration = average_acceleration / (measurements_per_second - 1)
    if (average_acceleration < max_acceleration):
        return(True)
    return(False)


def detect_fast_comeback_speed(sample_array, measurements_per_second):
    max_speed = -2
    average_speed = 0
    for element in sample_array:
        average_speed = average_speed + element
    average_speed = average_speed / measurements_per_second
    if (average_speed < max_speed):
        return(True)
    return(False)


def detect_pause(sample_array, measurements_per_second):
    deviation = 0.1
    average_speed = 0
    for element in sample_array:
        average_speed = average_speed + element
    average_speed = average_speed / measurements_per_second
    if (average_speed < abs(deviation)):
        return(True)
    return(False)


def detect_finish(file):

    with open(file) as f:
        found_zero = False
        negative = False
        csv_reader = csv.reader(f, delimiter=';')
        print(csv_reader)
        for row in csv_reader:
            print(row[7])
            if int(row[7]) == 0:
                found_zero = True
                negative = False
            elif int(row[7]) < 0 and found_zero == True:
                negative = True
            elif int(row[7]) > 0:
                found_zero = False
                negative = False
        if negative == True and found_zero == True:
            return True
        else:
            return False

    def detect_lower_half(y_position):
        if(y_position < 3):
            return True
        return False

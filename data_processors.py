from numpy import float64

from statistics import median

from csv_processors import writecsv
import detectors
import data_class


def compress_buffer(long_array, accuracy):
    id = long_array[0].id
    data_array = []
    for i in range(9):
        data_array.append([])

    for element in long_array:
        data_array[0].append(element.position[0])
        data_array[1].append(element.position[1])
        data_array[2].append(element.position[2])
        data_array[3].append(element.velocity[0])
        data_array[4].append(element.velocity[1])
        data_array[5].append(element.velocity[2])
        data_array[6].append(element.dimensions[0])
        data_array[7].append(element.dimensions[1])
        data_array[8].append(element.dimensions[2])

    for i in range(len(data_array)):
        data_array[i] = compress_data(data_array[i], accuracy)

    short_array = []
    # this calc does not make sense
    for i in range(len(long_array) // accuracy):
        short_array.append(data_class.Data(id, data_array[0][i], data_array[1][i], data_array[2][i], data_array[3]
                                           [i], data_array[4][i], data_array[5][i], data_array[6][i], data_array[7][i], data_array[8][i]))
    return short_array


def compress_data(long_array, accuracy):
    average = []
    short_array = []
    for i in range(len(long_array)):
        if type(long_array[i]) is float64:
            print(long_array[i])
            average.append(long_array[i])
        if (i + 1) % accuracy == 0:
            print("AAAAAAAAAAAAA")
            short_array.append(median(average))
            average = []
    return short_array


# 'measurements_per_second' is 'measurements_per_second // accuracy' here
def process_data(measurements_per_second, accuracy, old_detector_average, detector_average, buffer_average):
    anomaly = False
    start = 'WIP'
    end = 'WIP'
    pause = detectors.detect_pause(detector_average, measurements_per_second)
    fast_comeback = detectors.detect_fast_comeback_speed(
        detector_average, measurements_per_second)
    fall = False
    if (detectors.detect_anomaly(old_detector_average, detector_average, measurements_per_second)):
        anomaly = True
        if (detectors.detect_fall(detector_average, measurements_per_second)):
            fall = True
        elif (detectors.detect_fast_comeback_acceleration(detector_average, measurements_per_second)):
            fast_comeback = True
    for i in range(measurements_per_second):
        id = buffer_average[i].id
        position = buffer_average[i].position
        velocity = buffer_average[i].velocity
        dimensions = buffer_average[i].dimensions
        writecsv(id, position[0], position[1], position[2], velocity[0], velocity[1], velocity[2],
                 dimensions[0], dimensions[1], dimensions[2], anomaly, start, end, pause, fast_comeback, fall, detector_average[i])


def to_csv(obj_array, accuracy, measurements_per_second, buffer_data, detector_data, old_detector_average):
    for i in range(len(obj_array)):
        if not 'buffer_data[i]' in locals():
            buffer_data.append([])
            detector_data.append([])
        buffer_data[i].append(obj_array[i])
        detector_data[i].append(obj_array[i].velocity[1])
        if (len(buffer_data[i]) >= measurements_per_second):
            print("buffer")
            buffer_average = compress_buffer(buffer_data[i], accuracy)
            print("detector")
            detector_average = compress_data(detector_data[i], accuracy)
            process_data(measurements_per_second // accuracy, accuracy, old_detector_average,
                         detector_average, buffer_average)
            old_detector_average = detector_average.copy()
            buffer_data[i] = []
            detector_data[i] = []
    return buffer_data, detector_data, old_detector_average


# This methode calculates the y_velocity instead of using the one from the camera
def to_csv_calc(obj_array, accuracy, measurements_per_second, buffer_data, old_detector_average):
    for i in range(len(obj_array)):
        if not 'buffer_data[i]' in locals():
            buffer_data.append([])
        buffer_data[i].append(obj_array[i])
        if (len(buffer_data[i]) >= measurements_per_second):
            buffer_average = compress_buffer(buffer_data[i], accuracy)
            detector_average = calc_y_velocity(
                old_detector_average, buffer_average, measurements_per_second, accuracy)
            process_data(measurements_per_second // accuracy, accuracy, old_detector_average,
                         detector_average, buffer_average)
            old_detector_average[i] = detector_average.copy()
            buffer_data[i] = []
    return buffer_data, old_detector_average


def calc_y_velocity(old_detector_average, buffer_data, measurements_per_second, accuracy):
    last_y = 0
    if old_detector_average:
        last_y = old_detector_average[measurements_per_second // accuracy - 1]
    y_velocity_calc = []
    for element in buffer_data:
        y_velocity_calc.append(
            (element.position[1] - last_y) / (1 / measurements_per_second))
        last_y = element.position[1]
    return y_velocity_calc

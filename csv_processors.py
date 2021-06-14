import csv
import datetime
import uuid
import os

import detectors

MAX_ENTRIES_PER_FILE = 90


def initialize():
    if not os.path.exists('data/count.txt'):
        f = open('data/count.txt', "w")
        f.write("0")
        f.close()
    f = open('data/count.txt', "r")
    save_file = 'data/'
    count = int(f.read())
    f.close()

    if(count < MAX_ENTRIES_PER_FILE):
        if not os.path.exists('data/lastid.txt'):
            f = open('data/lastid.txt', "w")
            f.close()
        last_uuid = open('data/lastid.txt', "r")
        last_used_file = last_uuid.read()
        if not last_used_file:
            create_new_file()
            last_used_file = last_uuid.read()
            count = 0
        save_file = save_file + last_used_file
        last_uuid.close()
        if not os.path.exists('data/' + last_used_file):
            count = 0
    else:
        create_new_file()
        count = 0
        last_uuid = open('data/lastid.txt', "r")
        save_file = save_file + last_uuid.read()
        last_uuid.close

    return count, save_file


def create_new_file():
    last_uuid = open('data/lastid.txt', "w")
    last_uuid.write(str(uuid.uuid4()) + '.csv')
    last_uuid.close()
    f = open('data/count.txt', "w")
    f.write(str(0))
    f.close()


def writecsv(id, x_position, y_position, z_position, x_velocity, y_velocity, z_velocity, x_dimensions, y_dimensions, z_dimensions, anomaly, start, end, pause, fast_comeback, fall, y_velocity_calc):
    if not os.path.exists('data'):
        os.mkdir('data')

    count, save_file = initialize()

    with open(save_file, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'id', 'x_position', 'y_position', 'z_position', 'x_velocity', 'y_velocity',
                      'z_velocity', 'x_dimensions', 'y_dimensions', 'z_dimensions', 'anomaly', 'start', 'finish', 'pause', 'to_fast', 'fall', 'y_velocity_calc']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writerow({'timestamp': datetime.datetime.now().timestamp(), 'id': str(id), 'x_position': str(x_position), 'y_position': str(y_position), 'z_position': str(z_position), 'x_velocity': str(x_velocity), 'y_velocity': str(y_velocity),
                         'z_velocity': str(z_velocity), 'x_dimensions': str(x_dimensions), 'y_dimensions': str(y_dimensions), 'z_dimensions': str(z_dimensions), 'anomaly': str(anomaly), 'start': str(start), 'finish': str(end), 'pause': str(pause), 'to_fast': str(fast_comeback), 'fall': str(fall), 'y_velocity_calc': str(y_velocity_calc)})
        count = count + 1
        f = open('data/count.txt', "w")
        f.write(str(count))
        f.close()


def selection_sort(file):
    arr = []
    with open(file) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        for row in csv_reader:
            arr.append(row)
            print(row[0])

        for i in range(len(arr)):
            min_element_index = i
            for j in range(i + 1, len(arr)):
                if arr[j][0] < arr[min_element_index][0]:
                    min_element_index = j
            arr[i][0], arr[min_element_index][0] = arr[min_element_index][0], arr[i][0]
            print('y0: ' + arr[i][0])

    with open(file, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'id', 'x_position', 'y_position',
                      'z_position', 'x_velocity', 'y_velocity', 'z_velocity', 'x_dimensions', 'y_dimensions', 'z_dimensions', 'anomaly', 'start', 'finish', 'pause', 'to_fast', 'fall', 'y_velocity_calc']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        for element in arr:
            writer.writerow({'timestamp': str(element[0]), 'id': str(element[1]), 'x_position': str(element[2]), 'y_position': str(element[3]), 'z_position': str(element[4]), 'x_velocity': str(element[5]), 'y_velocity': str(element[6]),
                             'z_velocity': str(element[7]), 'x_dimensions': str(element[8]), 'y_dimensions': str(element[9]), 'z_dimensions': str(element[10]), 'anomaly': str(element[11]), 'start': str(element[12]), 'finish': str(element[13]), 'pause': str(element[14]), 'to_fast': str(element[15]), 'fall': str(element[16]), 'y_velocity_calc': str(element[17])})


def summarize(folder):
    with open(folder + 'speicher.csv', 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'id', 'x_position', 'y_position',
                      'z_position', 'x_velocity', 'y_velocity', 'z_velocity', 'x_dimensions', 'y_dimensions', 'z_dimensions', 'anomaly', 'start', 'finish', 'pause', 'to_fast', 'fall', 'y_velocity_calc']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        for filename in os.listdir(folder):
            if filename.endswith('.csv'):
                print(filename)
                with open(folder + filename) as csvfile:
                    csv_reader = csv.reader(csvfile, delimiter=';')
                    for row in csv_reader:
                        print(row)
                        writer.writerow({'timestamp': row[0], 'id': row[1], 'x_position': row[2], 'y_position': row[3], 'z_position': row[4], 'x_velocity': row[5], 'y_velocity': row[6],
                                         'z_velocity': row[7], 'x_dimensions': row[8], 'y_dimensions': row[9], 'z_dimensions': row[10], 'anomaly': row[11], 'start': row[12], 'finish': row[13], 'pause': row[14], 'to_fast': row[15], 'fall': row[16], 'y_velocity_calc': row[17]})

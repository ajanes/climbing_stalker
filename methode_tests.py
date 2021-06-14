import csv
import os

import data_class


buffer_data = []
detector_data = []
old_data = []
MEASUREMENTS_PER_SECOND = 15
ACCURACY = 5


def stalker_test(folder):
    data_class = []
    csv_data = []
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            print(filename)
            with open(folder + filename) as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=';')
                for row in csv_reader:
                    data_class.append(data_class.Data(
                        row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))


if __name__ == "__main__":
    stalker_test("data/")

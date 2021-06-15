# data, älteste datei, letzten 17 records lesen und in json ausgeben

# https://stackoverflow.com/questions/47739262/find-remove-oldest-file-in-directory

# https://medium.com/@hannah15198/convert-csv-to-json-with-python-b8899c722f6d 
import os
import csv
import json
from flask import Flask, request, render_template


def get_json(): 
    list_of_files = os.listdir('data/')
    full_path = ["data/{0}".format(x) for x in list_of_files]
    newest_file = max(full_path, key=os.path.getctime)
    print(newest_file)
    with open(newest_file) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        #lines= len(list(csv_reader))
        #print("lines: "+str(lines))
        index=0
        array=[]
        lines=0
        for row in csv_reader:
            lines+=1
        csvfile.seek(0)
        print(str(lines))
        for row in csv_reader:
            obj={}
            print(str(index))
            if(index>lines-18):
                obj["velocity"]=(float(row[6]))
                #print(row[6])
                array.append(obj)
                index+=1     
            else:
                index+=1
                continue
            
        print(array)
    return json.dumps(array)

#app = Flask(__name__)
app = Flask(__name__, template_folder='')

@app.route('/data')
def data():
    return get_json()

@app.route("/")
def index():
    print("asdohsadousdhoaohds: "+os.getcwd())
    return render_template("/index.html")


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
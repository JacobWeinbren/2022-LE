from calendar import c
import csv, helper

#Checks missing wards
def check_maps1():

    new_results = helper.new_results()
    wards = []

    data_files = ['../maps1/eng.csv', '../maps1/sco.csv', '../maps1/lon.csv', '../maps1/wal.csv']

    #Collect wards that appear on maps
    for data_file in data_files:
        with open(data_file) as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            sheet_data = [row for row in reader]
            for row in sheet_data:
                #Shorthand
                wards.append(row[11])
    
    count = 0
    #Print missing wards
    for item in new_results:
        merger = (helper.clear(item['shorthand']) + '-' + item['council']).strip()

        if merger not in wards:
            count += 1 
            print(item['name'], item['council'])

    print(count)

check_maps1()


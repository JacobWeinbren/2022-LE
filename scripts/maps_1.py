import csv, re, fiona

regex = re.compile('[^a-zA-Z]')

#Read result values
with open("../sources/results/LE2022 RESULTS - RESULTS.csv") as f:
    reader = csv.reader(f, delimiter=",", quotechar='"')
    data_read = [row for row in reader]

    data = []

    for temp_data in data_read[5:]:

        #Clean data
        item = []
        for index, x in enumerate(temp_data):
            if index > 9:
                if x == '':
                    item.append(0)
                else:
                    item.append(int(x.replace(',','')))
            else:
                item.append(x)

        #Party vote tally
        info = {
            "con": item[10],
            "lab": item[11],
            "lib": item[12],
            "green": item[13],
            "snp": item[15],
            "plaid": item[16],
            #We  show ind in other maps
            "other": item[14] + sum(item[17:34])
        }

        total = sum(info.values())

        if total > 0:

            #Voteshare
            for key in info:
                info[key] = round(info[key] / total * 100, 1)

            info["code"] =  regex.sub('', item[3]).lower()
            info["name"] = item[3]

            data.append(info)

def create(infile, outfile, outcsv):

    #Read infile
    print("Processing", infile)
    meta = fiona.open(infile)

    #Write to csv
    with open(outcsv, "wt") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(list(data[0].keys()))

        #Write to geojson
        with fiona.open(infile) as source, fiona.open(outfile, 'w', driver=meta.driver, schema = meta.schema, crs=meta.crs) as dest:
            for index, feat in enumerate(source):

                name = re.sub(' Ward', '', feat['properties']['NAME'])
                name = re.sub(' ED', '', name)

                #Is it in thw 2022 records?
                for item in data:
                    if item['code'] == regex.sub('', name).lower():

                        #Write to csv
                        writer.writerow(list(item.values()))
                        
                        #Update name to match
                        feat['properties']['NAME'] = item['name']
                        #Write to file
                        dest.write(feat)

create('../sources/output/wards_lon_2022.geojson', '../maps1/lon_2022.geojson', '../maps1/lon.csv')
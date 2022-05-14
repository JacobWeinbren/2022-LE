import csv, re, fiona
from collections import OrderedDict
from bs4 import BeautifulSoup  
import helper

new_results = helper.new_results()

def writeward(shorthand, name, council, item, feat, writer):
    merger = (shorthand + '-' + council).strip()

    #Write to csv
    item['name'] = name
    item['id'] = merger
    writer.writerow(list(item.values()))
    
    #Update feature to match
    feat['properties'] = {}
    feat['properties']['id'] = merger

def getattrs(feat):
    if feat['properties']['content'] != None:

        html = feat['properties']['content']
        soup = BeautifulSoup(html, "html.parser")
        values = soup.select('span.atr-value')

        if len(values):

            name = values[0].text
            district = values[2].text

    elif feat['properties']['Name'] != None:

        name = feat['properties']['Name']
        district = feat['properties']['District']

    return name, district

def create(infile, outfile, outcsv):

    #Read infile
    print("Processing", infile)
    meta = fiona.open(infile)

    #Write to csv
    with open(outcsv, "wt") as f:
        writer = csv.writer(f, delimiter=",")
        headers = list(new_results[0].keys())
        headers.append('name')
        headers.append('id')
        writer.writerow(headers)

        schema = meta.schema
        schema['properties'] = OrderedDict([('id', 'str')])

        #Write to geojson
        with fiona.open(infile) as source, fiona.open(outfile, 'w', driver=meta.driver, schema = schema, crs=meta.crs) as dest:
            for index, feat in enumerate(source):

                name = False

                name, district = getattrs(feat)

                if name:
                    shorthand = helper.clear(helper.process_name(name))
                    district = helper.clear(helper.process_council(district))
                    found = False
                    #Is it in the 2022 records?
                    for item in new_results:
                        if item['shorthand'] == shorthand:
                            if item['council'] == district:
                                writeward(shorthand, name, district, item, feat, writer)
                                dest.write(feat)
                                found = True
                                break

if __name__ == "__main__":             
    create('../sources/output/lon_2022.geojson', '../maps1/lon_2022.geojson', '../maps1/lon.csv')
    create('../sources/output/eng_2022.geojson', '../maps1/eng_2022.geojson', '../maps1/eng.csv')
    create('../sources/output/wal_2022.geojson', '../maps1/wal_2022.geojson', '../maps1/wal.csv')
    create('../sources/output/sco_2022.geojson', '../maps1/sco_2022.geojson', '../maps1/sco.csv')
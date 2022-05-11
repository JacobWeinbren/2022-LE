import csv, re, fiona
from collections import OrderedDict
import helper

new_results = helper.new_results()

def create(infile, outfile, outcsv):

    #Read infile
    print("Processing", infile)
    meta = fiona.open(infile)

    #Write to csv
    with open(outcsv, "wt") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(list(new_results[0].keys()))

        schema = meta.schema
        schema['properties'] = OrderedDict([('name', 'str'),('council', 'str')])

        #Write to geojson
        with fiona.open(infile) as source, fiona.open(outfile, 'w', driver=meta.driver, schema = schema, crs=meta.crs) as dest:
            for index, feat in enumerate(source):
                
                name = re.sub(' Ward', '', feat['properties']['NAME'])
                name = re.sub(' ED', '', name)
                shorthand = helper.clear(name)

                council = helper.findcouncil(feat['properties']['CODE'])

                #Is it in the 2022 records?
                for item in new_results:
                    if council and item['shorthand'] == shorthand and item['council'] == helper.clear(council):

                        print(index, name)

                        #Write to csv
                        item['name'] = name
                        item['council'] = council
                        writer.writerow(list(item.values()))
                        
                        #Update feature to match
                        feat['properties'] = {}
                        feat['properties']['name'] = name
                        feat['properties']['council'] = council

                        #Write to file
                        dest.write(feat)

                        break

create('../sources/output/wards_lon_2022.geojson', '../maps1/lon_2022.geojson', '../maps1/lon.csv')
#create('../sources/output/wards_eng_2022.geojson', '../maps1/eng_2022.geojson', '../maps1/eng.csv')
#create('../sources/output/wards_wal_2022.geojson', '../maps1/wal_2022.geojson', '../maps1/wal.csv')
#create('../sources/output/wards_sco_2022.geojson', '../maps1/sco_2022.geojson', '../maps1/sco.csv')
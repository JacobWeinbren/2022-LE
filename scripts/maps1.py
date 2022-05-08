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
        writer.writerow(list(new_results[0].keys())[:-1])

        schema = meta.schema
        schema['properties'] = OrderedDict([('NAME', 'str')])

        #Write to geojson
        with fiona.open(infile) as source, fiona.open(outfile, 'w', driver=meta.driver, schema = schema, crs=meta.crs) as dest:
            for index, feat in enumerate(source):

                #print(feat['properties']['NAME'])
                name = re.sub(' Ward', '', feat['properties']['NAME'])
                name = re.sub(' ED', '', name)
                code = helper.clear(name)

                #Is it in thw 2022 records?
                for item in new_results:
                    if item['code'] == code:

                        #Write to csv
                        writer.writerow(list(item.values())[:-1])
                        
                        #Update name to match
                        feat['properties'] = {}
                        feat['properties']['NAME'] = code

                        #Write to file
                        dest.write(feat)

                        break

create('../sources/output/wards_lon_2022.geojson', '../maps1/lon_2022.geojson', '../maps1/lon.csv')
create('../sources/output/wards_eng_2022.geojson', '../maps1/eng_2022.geojson', '../maps1/eng.csv')
create('../sources/output/wards_wal_2022.geojson', '../maps1/wal_2022.geojson', '../maps1/wal.csv')
create('../sources/output/wards_sco_2022.geojson', '../maps1/sco_2022.geojson', '../maps1/sco.csv')
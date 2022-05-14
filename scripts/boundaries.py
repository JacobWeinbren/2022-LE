import fiona, helper
from shapely.geometry import shape
from collections import OrderedDict
import maps1

#Remove wards with changed boundaries
def compare(base_file, comp_file, output_file):

    remove_list = []
    
    #Read Base File
    print("Reading Base File")
    base_data = fiona.open(base_file)

    #Read Comparison File
    print("Reading Comparison File")
    comp_data = fiona.open(comp_file)
 
    matched_list = []
    changed_list = []

    #Load geometry
    base_geom = [shape(feat["geometry"]) for feat in base_data]
    comp_geom = [shape(feat["geometry"]) for feat in comp_data]

    #Compare features
    for i, base_feature in enumerate(base_geom):

        matched = False

        for j, comp_feature in enumerate(comp_geom):

            if base_feature.intersects(comp_feature):

                similarity1 = (base_feature.intersection(comp_feature).area/base_feature.area)*100
                similarity2 = (comp_feature.intersection(base_feature).area/comp_feature.area)*100

                if 90 <= similarity1 <= 110 and 95 <= similarity2 <= 105:
                    matched = True
                    matched_list.append(i)
                    break

        if not matched:
            changed_list.append(i)

    #Write to file
    print(len(matched_list), len(changed_list))
    print("Writing")

    schema = {'properties': OrderedDict([('name', 'str'), ('district', 'str')]), 'geometry': 'Polygon'}

    with fiona.open(base_file) as source, fiona.open(output_file, 'w', driver=base_data.driver, schema = schema, crs=base_data.crs) as dest:
        for index, feat in enumerate(source):

            name, district = maps1.getattrs(feat)

            feat['properties'] = {}
            feat['properties']['name'] = name
            feat['properties']['district'] = district

            if index not in changed_list:
                dest.write(feat)

compare(
    '../sources/output/lon_2022.geojson', 
    '../sources/output/lon_2018.geojson',
    '../sources/processed/wards_lon.geojson'
)

compare(
    '../sources/output/eng_2022.geojson', 
    '../sources/output/eng_2018.geojson',
    '../sources/processed/wards_eng.geojson'
)

compare(
    '../sources/output/sco_2022.geojson', 
    '../sources/output/sco_2017.geojson',
    '../sources/processed/wards_sco.geojson'
)

compare(
    '../sources/output/wal_2022.geojson', 
    '../sources/output/wal_2017.geojson',
    '../sources/processed/wards_wal.geojson'
)
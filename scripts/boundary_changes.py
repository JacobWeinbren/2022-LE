import fiona, re
from shapely.geometry import shape

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

                if 90 <= similarity1 <= 110 and 90 <= similarity2 <= 110:
                    matched = True
                    matched_list.append(i)
                    break

        if not matched:
            changed_list.append(i)

    #Write to file
    print(len(matched_list), len(changed_list))
    print("Writing")

    with fiona.open(base_file) as source, fiona.open(output_file, 'w', driver=base_data.driver, schema = base_data.schema, crs=base_data.crs) as dest:
        for index, feat in enumerate(source):
            feat['properties']['NAME'] = re.sub(' Ward', '', feat['properties']['NAME'])
            feat['properties']['NAME'] = re.sub(' ED', '', feat['properties']['NAME'])
            if index not in changed_list:
                dest.write(feat)

compare(
    '../sources/output/wards_lon_2022.geojson', 
    '../sources/output/wards_lon_2018.geojson',
    '../sources/processed/wards_lon.geojson'
)

compare(
    '../sources/output/wards_eng_2022.geojson', 
    '../sources/output/wards_eng_2018.geojson',
    '../sources/processed/wards_eng.geojson'
)

compare(
    '../sources/output/wards_sco_2022.geojson', 
    '../sources/output/wards_sco_2017.geojson',
    '../sources/processed/wards_sco.geojson'
)

compare(
    '../sources/output/wards_wal_2022.geojson', 
    '../sources/output/wards_wal_2017.geojson',
    '../sources/processed/wards_wal.geojson'
)

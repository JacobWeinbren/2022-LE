import re, csv

replacement_names = {
    "Bethnal Green East": ["St Peter's", "Tower Hamlets"],
    "Bethnal Green West": ["Bethnal Green", "Tower Hamlets"],
    "Swinton & Wardley": ["Swinton and Wardley", "Salford"],
    "Levans and Crooklands": ["Levens and Crooklands", "Westmorland & Furness"],
    "Old Barrow": ["Old Barrow and Hindpool", "Westmorland & Furness"],
    "George Street/Harbour": ["George St / Harbour", "Aberdeen"],
    "Sgìre an Rubha": ["SgÃ¯Â¿Â½re an Rubha (Point)", "Comhairle nan Eilean Siar"],
    "Sgìre nan Loch": ["SgÃ¯Â¿Â½re nan Loch", "Comhairle nan Eilean Siar"],
    "Steòrnabhagh a Deas": ["SteÃ¯Â¿Â½rnabhagh a Deas (Stornaway South)", "Comhairle nan Eilean Siar"],
    "Steòrnabhagh a Tuath": ["SteÃ¯Â¿Â½rnabhagh a Tuath (Stornaway North)", "Comhairle nan Eilean Siar"],
    "Uibhist a Deas Èirisgeigh agus Beinn na Faoghla": ["Uibhist a Deas, Ã¯Â¿Â½irisgeigh agus Beinn na Faoghla (South Uist)", "Comhairle nan Eilean Siar"],
    "Skye": ["Eilean Ã¯Â¿Â½ ChÃ¯Â¿Â½o (Skye)", "Highland"],
    "Burnham North": ["Burnham on Sea North", "Somerset"],
    "Bryntyrion Laleston and Merthyr Ma": ["Bryntirion, laleston and Merthyr Mawr ED", "Bridgend"],
    "Darran Valley": ["Darren Valley ED", "Caerphilly"],
    "St Clears with Llansteffan": ["St. Clears and Llansteffan ED", "Carmarthenshire"],
    "Llansantffraid": ["Llansanffraid ED", "Ceredigion"],
    "New Quay with Llanllwchaiarn": ["New Quay and Llanllwchaearn ED", "Ceredigion"],
    "Edernion": ["Edeirnion ED", "Denbighshire"],
    "Efenechtyd": ["Efenechdyd ED", "Denbighshire"],
    "Ewloe": ["Hawarden: Ewloe ED", "Flintshire"],
    "Llanasa and Trelawyd": ["Llanasa and Trelawnyd ED", "Flintshire"],
    "Brithdir and Llanfachreth / Ganllwyd /": ["Brithdir and Llanfachreth/Ganllwyd/Llanelltyd ED", "Gwynedd"],
    "De Dollgellau": ["De Dolgellau ED", "Gwynedd"],
    "Tre-garth a Mynydd Llandygái": ["Tre-garth a Mynydd Llandygai ED", "Gwynedd"],
    "Cantref": ["Cantref ED (DET)", "Monmouthshire"],
    "Crynant Onllywn and Seven Sisters": ["Crynant, Onllwyn and Seven Sisters ED", "Neath Port Talbot"],
    "Gwaun-Cae-Gurwen and Lower Brynamma": ["Gwaun-Cae-Gurwen and Lower Brynamman ED", "Neath Port Talbot"],
    "Narberth": ["Narberth: Urban ED", "Pembrokeshire"],
    "Newtown West": ["Newton West ED", "Powys"],
    "Bôn-y-maen": ["Bon-y-maen ED", "Swansea"],
    "Goresinon and Penyrheol": ["Gorseinon and Penyrheol ED", "Swansea"],
    "Pontlliw and Tircoed": ["Pontlliew and Tircoed ED", "Swansea"],
    "Wathvale": ["Wathvale and Bishop Monkton", "Harrogate"]
}

replacement_councils = {
    "Comhairle nan Eilean Siar": "Na h-Eileanan Siar",
    "Anglesey": "Isle of Anglesey"
}

#Party code
def partycode(party):
    if party in ["Lab", "Con", "LDem", "Grn", "Ind", "SNP", "PC"]:
        return party
    else:
        return "OTH"

#Clear text of ascii, numbers, capitalisation
def clear(name):

    name = name.lower()
    name = name.replace(" and ","").replace(" a ","").replace(" an ","")
    name = name.replace(" ", "")

    #Remove bracktets
    name = re.sub("[\(\[].*?[\)\]]", "", name)

    #Remove non letters
    name = ''.join([i for i in name if i.isalpha()])

    return name.strip()

def process_council(council):
    if '-' in council:
        council = council.rsplit('-',1)[1]
    council = council.replace("City of", "").replace("London Boro","").replace("District","").replace("City","").replace("Islands","").replace("the ", "").replace("County","")
    return council

def process_name(name):
    if name.endswith('Ward'):
        name = name[:-4]
    if name.endswith('ED'):
        name = name[:-2]
    return name

#Name exceptions
def exceptions(name, council):

    for key in replacement_names:
        if name == key and council == replacement_names[key][1]:
            name = process_name(replacement_names[key][0])

    if council in replacement_councils:
        council = process_council(replacement_councils[council])

    return clear(process_name(name)), clear(process_council(council))

#Parse list data
def parse_csv_list(csv_list):
    item = []

    for x in csv_list:
        x = x.replace(',','')

        if x.isdigit():
            item.append(int(x))
        elif x == '':
            item.append(0)
        else:
            item.append(x)

    return item

#Parse percentages
def parse_percentage(input_item, output_item, total):

    #Voteshare
    for key in output_item:
        output_item[key] = round(output_item[key] / total * 100, 1)

#Read New Results
def new_results():

    data = []

    #Read result values
    with open("../sources/results/2022 local election results (Britain Elects aggregate) - results.csv") as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        sheet_data = [row for row in reader]

        for temp_data in sheet_data[5:]:

            input_item = parse_csv_list(temp_data)

            #Party vote tally
            output_item = {
                "con": input_item[6],
                "lab": input_item[7],
                "lib": input_item[8],
                "green": input_item[9],
                "snp": input_item[10],
                "plaid": input_item[11],
                "other": sum(input_item[12:20])
            }

            total = sum(output_item.values())

            if total > 0:
                parse_percentage(input_item, output_item, total)
            if input_item[4]:
                output_item["shorthand"], output_item["council"] = exceptions(input_item[1], input_item[0])
                output_item['name'] = input_item[1]
                output_item["winner"] = partycode(input_item[4])

                data.append(output_item)

    return data

def old_results():

    data = []

    #England
    with open("../sources/results/LE2018, England - Ward-by-ward results.csv") as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        sheet_data = [row for row in reader]

        for temp_data in sheet_data[3:]:
            input_item = parse_csv_list(temp_data[0:11])
                
            #Party vote tally
            output_item = {
                "con": input_item[4],
                "lab": input_item[5],
                "lib": input_item[6],
                "green": input_item[8],
                "ind": input_item[9],
                "other": input_item[7] + input_item[10]
            }
            
            total = sum(output_item.values())

            if total > 0:
                parse_percentage(input_item, output_item, total)
                output_item["shorthand"], output_item["council"] = exceptions(input_item[3], input_item[2])
                output_item['name'] = input_item[3]
                data.append(output_item)

    #Scotland
    with open("../sources/results/2017-Council-Results.csv") as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        sheet_data = [row for row in reader]

        for temp_data in sheet_data[1:]:

            input_item = parse_csv_list(temp_data[0:11])

            if not input_item[2] == 'All':

                #Party vote tally
                output_item = {
                    "snp": input_item[4],
                    "lab": input_item[5],
                    "con": input_item[6],
                    "lib": input_item[7],
                    "green": input_item[7],
                    "ind": input_item[8],
                    "other": input_item[9] + input_item[10]
                }

                total = sum(output_item.values())

                if total > 0:
                    parse_percentage(input_item, output_item, total)
                    output_item["shorthand"], output_item["council"] = exceptions(input_item[2], input_item[0])
                    output_item['name'] = input_item[2]
                    data.append(output_item)

    #Wales
    with open("../sources/results/2017 Wales LE.csv") as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        sheet_data = [row for row in reader]

        temp_output = {}

        for temp_data in sheet_data[1:]:

            input_item = parse_csv_list(temp_data[0:7])

            if not input_item[6] == 'unop.':

                code = clear(input_item[1])

                if not code in temp_output:
                    temp_output[code] = {}

                if input_item[5] == "PC":
                    temp_output[code]["plaid"] = input_item[6]
                elif input_item[5] == "Lab":
                    temp_output[code]["lab"] = input_item[6]
                elif input_item[5] == "Ind":
                    temp_output[code]["ind"] = input_item[6]
                elif input_item[5] == "C":
                    temp_output[code]["con"] = input_item[6]
                elif input_item[5] == "LD":
                    temp_output[code]["lib"] = input_item[6]
                else:
                    temp_output[code]["other"] = input_item[6]

        for key in temp_output:

            #Party vote tally
            output_item = temp_output[key]
            input_item = [key]

            total = sum(output_item.values())

            if total > 0:
                parse_percentage(input_item, output_item, total)
                output_item["shorthand"], output_item["council"] = exceptions(input_item[0], input_item[1])
                output_item['name'] = input_item[0]
                data.append(output_item)

    return data
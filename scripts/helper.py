import re, csv, unidecode, requests, json
from bs4 import BeautifulSoup as Soup
import urllib

with open("../sources/boundary-line-code-changes-May-2022.csv") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    next(reader)
    changes = [row for row in reader]

#Search for ward's council
def searcharea(code):
    address = "https://findthatpostcode.uk/search/?q=" + str(code)
    response = requests.get(address)

    if response.status_code == 200:
        soup = Soup(response.content, 'html.parser')
        try:
            meta = soup.find(class_='columns').find('ul').find('li').find('a')['href'].replace('.html','.json')

            address = "https://findthatpostcode.uk/" + meta
            response = requests.get(address)

            if response.status_code == 200:
                response = json.loads(response.text)
                name = False
                for included in response['included']:
                    if 'attributes' in included and 'active' in included['attributes'] and included['attributes']['active'] == True:
                        name = included['attributes']['name']
                return name
            else:
                return False
        except:
            return False
    else:
        return False

#Clear text of ascii, numbers, capitalisation
def clear(name):

    #Normalise string
    name = unidecode.unidecode(name)
    name = name.lower()
    
    #Second value keeps translations
    #/, &, and are used interchangably
    if '/' in name:
        name = name.split('/')[1]
    elif '&' in name:
        name = name.split('&')[1]
    elif 'and' in name:
        name = name.split('and')[1]

    #Remove numbers and misc
    filter(lambda x: x.isalpha(), name)

    #Clear
    name = name.strip()

    return name

#Search for council
def findcouncil(code):

    item = code

    for row in changes:
        if row[0] == code:
            item = row[2]
            break
    
    council = searcharea(item)
    return council

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
    with open("../sources/results/LE2022 RESULTS - RESULTS.csv") as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        sheet_data = [row for row in reader]

        for temp_data in sheet_data[5:]:

            input_item = parse_csv_list(temp_data)

            #Party vote tally
            output_item = {
                "con": input_item[10],
                "lab": input_item[11],
                "lib": input_item[12],
                "green": input_item[13],
                "ind": input_item[14],
                "snp": input_item[15],
                "plaid": input_item[16],
                "other": sum(input_item[17:34])
            }

            total = sum(output_item.values())

            if total > 0:
                parse_percentage(input_item, output_item, total)
                output_item["shorthand"] = clear(input_item[3])
                output_item["council"] = clear(input_item[2])
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
                output_item["shorthand"] = clear(input_item[3])
                output_item["council"] = clear(input_item[2])
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
                    output_item["shorthand"] = clear(input_item[2])
                    output_item["council"] = clear(input_item[0])
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
                output_item["shorthand"] = clear(input_item[0])
                output_item["council"] = clear(input_item[1])
                data.append(output_item)

    return data
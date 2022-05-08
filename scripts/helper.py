import re, csv

#Clear text of ascii, numbers, capitalisation
def clear(name):
    #Remove and
    name = str(name.replace(' and ',''))
    #Remove numbers
    filter(lambda x: x.isalpha(), name)
    #Remove misc
    return re.sub(r'\W+', '', name).lower()

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
def parse_percentage(input_item, output_item, name_loc, total):

    #Voteshare
    for key in output_item:
        output_item[key] = round(output_item[key] / total * 100, 1)

    output_item["code"] = clear(input_item[name_loc])

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
                parse_percentage(input_item, output_item, 3, total)
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
                parse_percentage(input_item, output_item, 3, total)
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
                    parse_percentage(input_item, output_item, 2, total)
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
                parse_percentage(input_item, output_item, 0, total)
                data.append(output_item)

    return data

if __name__ == "__main__":
    with open('old.csv', "wt") as f:
        writer = csv.writer(f, delimiter=",")

        data = old_results()

        writer = csv.DictWriter(f, ['code','lab','con','lib','green','plaid','snp','ind','other'])
        writer.writeheader()
        writer.writerows(data)

    with open('new.csv', "wt") as f:
        writer = csv.writer(f, delimiter=",")

        data = new_results()

        writer = csv.DictWriter(f, ['code','lab','con','lib','green','plaid','snp','ind','other'])
        writer.writeheader()
        writer.writerows(data)


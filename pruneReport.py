#Fix IMS CSV Report

import csv
def readCSV(fileName):
    outputArray = []
    with open(fileName, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_ALL, skipinitialspace=True)
        next(reader, None)  # skip the headers
        
        for row in reader:
            temp = []
            for i in range(0,len(row)):
                if row[i] != '':
                    temp.append(row[i])
            #print (row[0])
            outputArray.append(temp)
    return outputArray



import csv
def writeCSV(header, rows, filename):

    with open(filename, 'w', newline='') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 

        # writing the fields 
        csvwriter.writerow(header) 

        # writing the data rows 
        csvwriter.writerows(rows)


def process(row):
    temp = []
    #print (row[3])
    try:
        r = row[3].split(",")
    except:
        print(row)
        r = row[3]
    #print(r[0])

    temp.append(row[0])
    temp.append(row[1])
    temp.append(row[2])
    temp.append(r[0])
    temp.append(row[3])
    
    
    return temp


writeRows = []
writeHeader = ["Patient Name","Visit Date","IDC","ICD_SHORT_DESC","Billing Detail Diagnosis 1 Desc"]

csvAI = readCSV(r"C:\Users\ntak\Desktop\USB\DataSets\Dataset3\IMS AI Macular Degeneration.csv")
for x in range(len(csvAI)):
    #print (x)
    writeRows.append(process(csvAI[x]))


outputFile =  r"C:\Users\ntak\Desktop\USB\DataSets\Dataset3\macular degeneration modified.csv"

writeCSV(writeHeader, writeRows, outputFile)
print()
print("Compleate")
print("Num of entries: " + str(len(writeRows)))
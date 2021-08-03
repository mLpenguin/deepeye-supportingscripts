import os,csv,glob

directory = "D:/"


namesArray = []
def readPatientNames(fileloc):
    with open(fileloc) as my_file:
        for line in my_file:
            x = line.rstrip('\n')
            y = x.split(",")
            #print(y)
            z = y[0] + " " + y[1]
            namesArray.append(x)

idArray = []
def readIds(fileloc):
    with open(fileloc) as my_file:
        for line in my_file:
            line = line.strip()
            #y = x.split(",")
            #z = y[0] + " " + y[1]
            if "[]" in line:
                line="['NONE']"
            line = line.replace('\'', "")
            line = line.replace(', ', "@%")
            #remove first/last bracket
            line = line[1:-1]
            #print (line)
            idArray.append(line)
            
readIds(directory + "Secure/patientid.txt")
readPatientNames(directory + "Secure/patientnames.txt")


idToNameConverter = {}
print("Names Array Lenght: "+ str(len(namesArray)))
print("Id Array Lenght: "+ str(len(idArray)))

#print(idArray)


def convertPatientIdToName(iD):
    
    returnValue = "NONE"
    for x in range(0,len(idArray)):
        if iD in idArray[x]:
            returnValue = namesArray[x]

    return returnValue
    
    """
    possibleIds = idToNameConverter[iD]
    print (possibleIds)
    return idToNameConverter[iD]
    """

#        filename, idc10 root, idc10, side of the idc




def readCSV(fileName):
    outputArray = []
    with open(directory + fileName, 'r') as file:
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

def writeCSV(header, rows, filename):

    f = open(directory + filename,"w")
    f.write(header[0]+","+header[1]+","+header[2]+","+header[3])
    f.write("\n")

    for i in range(0,len(rows)):
        
        
        f.write(rows[i][0]+","+rows[i][1]+","+rows[i][2]+","+rows[i][3])
        f.write("\n")
    f.close()
    """
    # writing to csv file  
    with open(directory + filename, 'w') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(header)
        # writing the data rows
        csvwriter.writerows(rows)
    """

#Read "dosPatientIcdSide.csv" and output to array
DOSPatientNameICD = readCSV("dosPatientIcdSide.csv")



#print (DOSPatientNameICD[0])
    #print(patientID)

#Convert DOS
for x in range(0,len(DOSPatientNameICD)):
    
    
    csVDOS = DOSPatientNameICD[x][0].split("/")
    #print(eachFile)
    month = str(csVDOS[0])
    day = str(csVDOS[1])
    year = str(csVDOS[2])
    csVDOS = year+month+day
    DOSPatientNameICD[x][0] = csVDOS



mLCsvRows = []
mLCsvHeader = ["FILENAME", "ICD_ROOT", "ICD", "ICD_SIDE"]
ff = 0
UsingImages = glob.glob(directory+"ImageDownload/*.jpg")
AllImages = glob.glob(directory+"ImageDownload - Copy/*.jpg")

UI = []
for x in range(0, len(UsingImages)):
    f = UsingImages[x].split("\\")
    UI.append(f[1])
AI = []
for x in range(0, len(AllImages)):
    f = AllImages[x].split("\\")
    AI.append(f[1])


RejectedImages = list(set(AI) - set(UI))

dd = len(RejectedImages)

print (str(dd) + " " + str(len(AllImages))+ " " + str(len(UsingImages)) + " " + str(len(AllImages) - len(UsingImages)) )



def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

#print (str(RejectedImages))

for x in range(0, len(RejectedImages)):
    printProgressBar(ff, dd, prefix = 'Progress:', suffix = 'Complete', length = 50)
    ff += 1

    temp = []
    #print (eachFile + " " + str(DOSPatientNameICD[x][2]))
    temp.append(RejectedImages[x])                       #File Name
    temp.append("0") #Cut off last numberr of ICD
    temp.append("0.0")       #Full ICD
    temp.append("f")        #Side
    #print(temp)
    mLCsvRows.append(temp)

    #print(fileDateOfService)
#print(DOSPatientNameICD[0])
writeCSV(mLCsvHeader, mLCsvRows, "mLlistReject.csv")
#print(convertPatientIdToName("iyity"))

print("Done")
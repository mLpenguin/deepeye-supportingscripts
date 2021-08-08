import os,csv,glob
from typing_extensions import final

LOG = False

directory = r"C:\Users\ntak\Desktop\USB\\"


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
            
readIds(r"C:\Users\ntak\Desktop\USB\DataSets\Dataset4\diabetic retinopathy ID.txt")
readPatientNames(r"C:\Users\ntak\Desktop\USB\DataSets\Dataset4\diabetic retinopathy names.txt")


idToNameConverter = {}
print("Names Array Lenght: "+ str(len(namesArray)))
print("Id Array Lenght: "+ str(len(idArray)))

#print(idArray)


def convertPatientIdToName(iD):
    
    returnValue = "NONE"
    for x in range(0,len(idArray)):

        if iD == idArray[x]:
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

    with open(directory + filename, 'w', newline='') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 

        # writing the fields 
        csvwriter.writerow(header) 

        # writing the data rows 
        csvwriter.writerows(rows)

#Read "dosPatientIcdSide.csv" and output to array
DOSPatientNameICD = readCSV(r"DataSets\Dataset4\dosIcdDescSide.csv")



#print (DOSPatientNameICD[0][4])
    #print(patientID)

#Convert DOS
for x in range(0,len(DOSPatientNameICD)):
    
    
    csVDOS = DOSPatientNameICD[x][0].split("/")
    month = str(csVDOS[0]).zfill(2)
    day = str(csVDOS[1]).zfill(2)
    year = str(csVDOS[2])
    csVDOS = year+month+day
    DOSPatientNameICD[x][0] = csVDOS



mLCsvRows = []
mLCsvHeader = ["FILENAME", "ICD_ROOT", "ICD","ICD_SHORT_DESC", "ICD_SIDE"]
ff = 0
d = glob.glob(directory+"DataSets/Dataset4/sorted/*.jpg")

if (LOG):
    p= []

    p.append(d[0])
    #d = []
    d = p

'''
import pickle
#Introduce diffent arry with file names
d = []
with open (directory+'outfile', 'rb') as fp:
    d = pickle.load(fp)
'''
#print(d)

dd = len(d)

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

#num of files
print ("Number of images read in Directory: " + str(dd))
for eachFile in d:
    printProgressBar(ff, dd, prefix = 'Progress:', suffix = 'Complete', length = 50)
    ff += 1
    foundEntry = False
    eachFile = eachFile.split("\\")

    eachFile = eachFile[len(eachFile)-1]

    if(LOG): print("eachFile: ", eachFile)

    filePatientID = eachFile.split("-")
    #obtain patientID from filename
    fileSide = filePatientID[2][0].lower()
    fileDateOfService = filePatientID[1].split("@")[0]
    filePatientID = filePatientID[0]
    #print(fileSide in DOSPatientNameICD[x][3])
    #print (eachFile)
    #444rt-20210121@151427-R1-S.jpg

    #Find Corresponding Entry in CSV
    for x in range(len(DOSPatientNameICD)):
        #if(LOG): print("Location in csv: ", x)
        #Find corresponding DOSPatientNameICD Entry
        #print("Bye")
        #print(fileDateOfService)
        #print(DOSPatientNameICD[x][0])

        if(foundEntry): #Remove duplicates
            break

        if(LOG): print("NAME: ", convertPatientIdToName(filePatientID), DOSPatientNameICD[x][1])
        if(LOG): print("DOS: ", fileDateOfService, DOSPatientNameICD[x][0])
        if ((convertPatientIdToName(filePatientID) == DOSPatientNameICD[x][1]) and (fileDateOfService in DOSPatientNameICD[x][0])):
            if(LOG): print("FOUND NAME: ", filePatientID)
           
            if (fileSide == DOSPatientNameICD[x][4]) or ("b" == DOSPatientNameICD[x][4]): #only save if side matches code        
                
                #Write CSV
                temp = []
                temp.append(eachFile)                       #File Name
                temp.append(DOSPatientNameICD[x][2][:-1])   #Cut off last numberr of ICD
                temp.append(DOSPatientNameICD[x][2])        #Full ICD
                temp.append(DOSPatientNameICD[x][3])        #ICD_SHORT_DESC
                temp.append(DOSPatientNameICD[x][4])        #ICD_SIDE
                if(LOG): print("append: ", temp)
                foundEntry = True
                mLCsvRows.append(temp)
            
            """
            else: #If no side matched (Normal)

                if("r" in fileSide):
                    if ("l" in DOSPatientNameICD[x][3]):

                        #Write CSV
                        temp = []
                        temp.append(eachFile)       #File Name
                        temp.append('ZZZ')          #Cut off last numberr of ICD
                        temp.append('ZZZZ')         #Full ICD
                        temp.append(fileSide)       #Side
                        #print (temp)
                        mLCsvRows.append(temp)
                
                
                if("l" in fileSide):
                    if ("r" in DOSPatientNameICD[x][3]):

                        #Write CSV
                        temp = []
                        temp.append(eachFile)       #File Name
                        temp.append('ZZZ')          #Cut off last numberr of ICD
                        temp.append('ZZZZ')         #Full ICD
                        temp.append(fileSide)       #Side
                        #print (temp)
                        mLCsvRows.append(temp)
                """



    #if(not foundEntry): # If not found assume normal. Cant do cuz some images are not 
                        # coded in the list of diagnosis. so some images are left undiagnosed.
        #flawed, cant do




    """
    #If none found, label as normal
    if (foundEntry == False):
        #Write CSV
        temp = []
        temp.append(eachFile)                       #File Name
        temp.append(000.00)                         #Cut off last numberr of ICD
        temp.append(000.000)                        #Full ICD
        temp.append(fileSide)                       #Side
        print(temp)
        print(convertPatientIdToName(filePatientID))
        mLCsvRows.append(temp)
    """



writeCSV(mLCsvHeader, mLCsvRows, r"DataSets\Dataset4\dataset4.csv") #C:\\Users\\ntak\\Desktop\\USB\\ file name prefix
print()
print("Compleate")
print("Num of entries: " + str(len(mLCsvRows)))

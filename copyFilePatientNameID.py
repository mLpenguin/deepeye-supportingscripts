import os,csv,glob

from shutil import copyfile

directory = r"C:\Users\ntak\Desktop\USB\DataSets\Dataset8-hypertensiveretinopathy\\"
DEBUG = False

print("###########START###########")

namesArray = []
def readPatientNames(fileloc):
    with open(fileloc) as my_file:
        for line in my_file:
            x = line.rstrip('\n')
            y = x.split(",")
            #print(y)
            z = y[0] + " " + y[1]
            namesArray.append(x.lower())

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
            
readIds(directory + "hypertensive retinopathy ID.txt")
readPatientNames(directory + "hypertensive retinopathy names.txt")

nameToIdConverter = {}
print("Names Array Lenght: "+ str(len(namesArray)))
print("Id Array Lenght: "+ str(len(idArray)))


######Change to idArray[x] in production######
for x in range(0,len(namesArray)): #Build name/id dictionary
    nameToIdConverter[str(namesArray[x])] = str(idArray[x])

if(DEBUG): print(nameToIdConverter)


d = directory + "DOSpatientname.csv"
DOSPatientName = []

with open(d, 'r') as file:
    reader = csv.reader(file, quoting=csv.QUOTE_ALL, skipinitialspace=True)
    next(reader, None)  # skip the headers
    
    for row in reader:
        #print (row[0])
        DOSPatientName.append(row)
        #print(r)

#print (DOSPatientName[1473])

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


#   id-yearmonthday@time-side-S
#   nfdfggy-20210121@150226-R1-S   
  
#for x in range(0,len(DOSPatientName)):

#print(nameToIdConverter['Navarro,Graciela'])
#t = DOSPatientName[0][1]

OptosDirectory = "X:/OptosArchive/site_15028/Secondary/"



listOfFiles = []
with open(OptosDirectory + "contents.txt") as f: #Assume contents has list of all files in directory
    listOfFiles = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
listOfFiles = [x.strip() for x in listOfFiles] 
listOfFiles.pop(0) #remove header
listOfFiles.pop(0) #remove inital blank row
#1473
fileList = []
NoCopyList = []


ff=0
yy = len(DOSPatientName)

for y in range(len(DOSPatientName)):

    if(not DEBUG): printProgressBar(ff, yy, prefix = 'Progress:', suffix = 'Complete', length = 50)
    ff += 1
    #print (y)
    DOS = DOSPatientName[y][0]
    PATIENTNAME = str(DOSPatientName[y][1]).lower()

    DOS = DOS.split("/")

    month = str(DOS[0]).zfill(2)
    day = str(DOS[1]).zfill(2)
    year = str(DOS[2])

    p = nameToIdConverter[PATIENTNAME]
    ids = p.split("@%")


    isCopied = False

    for x in range(0,len(ids)):

        if(DEBUG): print("ID: ", ids[x], ids)
        
        for i in range(0,len(listOfFiles)):
            #print (i)
            skip = False
            try:
                eachFile = str(listOfFiles[i])
                #if(DEBUG): print("File: ", eachFile)
                eachFile_ID = eachFile.split("-")[0]
                eachFile_DATE = str(eachFile.split("-")[1]).split("@")[0]

            except: #if cant split discard
                skip = True
                pass

            if(not skip):
                #if(DEBUG): print(eachFile_ID, eachFile_DATE)
                #print(ids[x])
                #if(DEBUG): print("Found: ", year+month+day, eachFile_DATE)
                #if(DEBUG): print("Found: ", ids[x], eachFile_ID)
                if (year+month+day == eachFile_DATE) and (ids[x] == eachFile_ID):
                    if(DEBUG): print("Found: ", ids[x], eachFile_ID)
                    fileList.append(eachFile)
                    isCopied = True

                    if(not DEBUG): copyfile(OptosDirectory+eachFile, directory +"OPTOS_OUTPUT/"+eachFile)
                    ##copyfile("X:/site_15028/Secondary"+"/"+eachFile, "C:/Users/rcexam01/Desktop/OptoDownload/ImageDownload/" +eachFile)


    if (not isCopied):
        f = open(directory +"OPTOS_OUTPUT/" + "NoCopyimageDirectory.txt","a")
        if(not DEBUG): f.write(str(DOSPatientName[y]))
        if(not DEBUG): f.write("\n")
        f.close()


print()
print("DONE")


"""
def saveCSV(fields,rows):
    # writing to csv file  
    with open(directory + "imageDirectory.csv", 'w') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(rows)

Fields = ['DATE_OF_SERVICE', 'ID', 'SIDE', 'FILENAME']
Rows = []
for x in range(0, len(fileList)):
    row = []
    temp = fileList[x].split("-")
    
    
    
    
    
    ID = temp[0]
    SIDE = temp[2]
    DATE = temp[1].split("@")[0]
    FILENAME = fileList[x]
    
    print(DATE)
    row.append(DATE)
    row.append(ID)
    row.append(SIDE)
    row.append(FILENAME)
    
    Rows.append(row)

saveCSV(Fields, Rows)
"""


#print (nameToIdConverter[PATIENTNAME])

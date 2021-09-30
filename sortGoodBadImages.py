import csv,glob

directory = r"C:\Users\ntak\Desktop\USB\DataSets\GoodBadTrain\Dataset3\\"

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

def writeCSV(header, rows, filename):

    with open(filename, 'w', newline='') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 

        # writing the fields 
        csvwriter.writerow(header) 

        # writing the data rows 
        csvwriter.writerows(rows)


goodImages = glob.glob(directory+"sorted/*.jpg")
for x in range(len(goodImages)):
    temp = str(goodImages[x])
    temp = temp.replace(directory+"sorted\\", '')
    goodImages[x] = temp


allImages = glob.glob(directory+"OPTOS_OUTPUT-dataset3\*.jpg")
for x in range(len(allImages)):
    temp = str(allImages[x])
    temp = temp.replace(directory+"OPTOS_OUTPUT-dataset3\\", '')
    allImages[x] = temp

print(goodImages[0])
print(allImages[0])
ff = 0
dd = len(allImages)

mLCsvRows = []
mLCsvHeader = ["FILENAME", "GOOD_IMAGE"]


for eachFile in allImages:
    printProgressBar(ff, dd, prefix = 'Progress:', suffix = 'Complete', length = 50)
    ff += 1
    temp=[]
    temp.append(eachFile)

    if eachFile in goodImages:
        temp.append("1")
        #print("yay")
    else:
        temp.append("0")


    mLCsvRows.append(temp)



writeCSV(mLCsvHeader, mLCsvRows, directory + "dataset3BadGoodImages.csv")
print()
print("Compleate")
print("Num of entries: " + str(len(mLCsvRows)))
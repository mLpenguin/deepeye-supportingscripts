# Important Python Methods:

# Read CSV Files

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


# Write CSV Files

import csv
def writeCSV(header, rows, filename):

    with open(filename, 'w', newline='') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 

        # writing the fields 
        csvwriter.writerow(header) 

        # writing the data rows 
        csvwriter.writerows(rows)


# Export List
import glob

d = glob.glob(savePath+"*.jpg")

import pickle

with open('outfile', 'wb') as fp:
    pickle.dump(d, fp)


# Import List
import glob

with open ('outfile', 'rb') as fp:
    d = pickle.load(fp)


#Progress Bar
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

printProgressBar(countStatus, progressMax, prefix = 'Progress:', suffix = 'Complete', length = 50)

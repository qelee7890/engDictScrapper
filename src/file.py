import sys, os, csv
from webdict import cambridge, etymology
from tqdm import tqdm

def findParentPath():
    thisDirPath = os.path.dirname(os.path.abspath(__file__))
    parentDirPath = os.path.dirname(thisDirPath)
    return parentDirPath

def joinPath(dirPath1, dirPath2):
    pathJoined = os.path.join(dirPath1, dirPath2)
    return pathJoined

def findTargetDirPath(subDirName):
    parentDirPath = findParentPath()
    dirPath = joinPath(parentDirPath, subDirName)
    return dirPath  

def isFileExist(filePath):
    if os.path.isfile(filePath):
        return True
    else:
        return False

def isDirExist(dirPath):
    if os.path.isdir(dirPath):
        return True
    else:
        return False  

def makeDir(subDirName):
    dirPath = findTargetDirPath(subDirName)
    if not isDirExist(dirPath):
        os.mkdir(dirPath)
    return dirPath

def readCsvFile(subDirName, csvFileName):
    wordList = []
    csvTotalLineNumber = 0
    dirPath = findTargetDirPath(subDirName)
    makeDir(subDirName)
    filePath = joinPath(dirPath, csvFileName)
    if not isFileExist(filePath):
        raise ValueError(f"{csvFileName} file cannot be read")
    fileOpened = open(filePath, mode="r")
    csvReader = csv.reader(fileOpened)
    for word in csvReader:
        wordList.append(word[0])
        csvTotalLineNumber += 1
    fileOpened.close()
    return wordList, csvTotalLineNumber

def writeCsvFile(subDirName, csvFileName, wordList):
    fileWriter = None
    csvStartLineNumber = 0
    dirPath = findTargetDirPath(subDirName)
    makeDir(subDirName)
    filePath = joinPath(dirPath, csvFileName)
    if not isFileExist(filePath):
        fileOpened = open(filePath, mode="w")
    else:
        fileOpened = open(filePath, mode="r")
        csvReader = csv.reader(fileOpened)
        for _ in csvReader:
            csvStartLineNumber += 1
        wordList = wordList[csvStartLineNumber:]
        fileOpened.close()
        fileOpened = open(filePath, mode="a")
    fileWriter = csv.writer(fileOpened)
    writeCsvRow(fileWriter, wordList)
    fileOpened.close()

def writeCsvRow(fileWriter, wordList):
    rowContent = ["WORD", "PHR1", "PHR2", "PHR3",
                 "DEF1", "DEF2", "DEF3", "ETYM", "AUDI"]
    soundDirPath = makeDir("sound")
    for word in tqdm(wordList):
        defi, news, soundFileTag = cambridge(word, soundDirPath)
        etym = etymology(word)
        csvRow = [""] * len(rowContent)
        csvRow[0] = word
        for ii in range(0, min(3, len(news))):
            csvRow[ii + 1] = news[ii]["exa"] \
                               + " (" + news[ii]["src"] + ")"
        for ii in range(0, min(3, len(defi))):
            csvRow[ii + 4] = "<" + defi[ii]["pos"] \
                               + "> " + defi[ii]["def"] \
                               + "; " + defi[ii]["exa"]
        if etym["sub"] == "":
            csvRow[-2] == ""
        else:
            csvRow[-2] = etym["sub"] + "; " + etym["def"]
        csvRow[-1] = soundFileTag
        fileWriter.writerow(csvRow)
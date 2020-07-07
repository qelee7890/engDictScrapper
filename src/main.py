from file import readCsvFile, writeCsvFile, makeSoundDir

importFileName = "TIME CNN english words - n-s.csv"
exportFileName = "anki " + importFileName

wordList, csvTotalLineNumber = readCsvFile("wordlist", importFileName)
writeCsvFile("dict", exportFileName, wordList)
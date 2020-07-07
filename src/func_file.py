import csv
import sys, os

def completeAbsPath(fileName):
    thisFolder = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(thisFolder, fileName)
    return filePath

def import_file(import_file_name):
    filePath = completeAbsPath(import_file_name)
    file = open(filePath, mode="r")
    csv_reader = csv.reader(file)
    list_word = []
    csv_line_num = 0
    for word in csv_reader:
        list_word.append(word[0])
        csv_line_num += 1
    return file, list_word, csv_line_num

def export_file(export_file_name):
    filePath = completeAbsPath(export_file_name)
    if not os.path.isfile(filePath):
        file = open(filePath, mode="w")
        csv_line_num = 0
    else:
        file, _, csv_line_num = import_file(export_file_name)
        file.close()
        file = open(filePath, mode="a")
    csv_writer = csv.writer(file)
    return file, csv_writer, csv_line_num

def check_sound_dir(check):
    filePath = completeAbsPath("sound")
    sound_file_folder = filePath
    if check:
        if not os.path.isdir(sound_file_folder):
            os.mkdir(sound_file_folder)
        return
    else:
        return sound_file_folder

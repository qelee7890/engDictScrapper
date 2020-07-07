from func_file import import_file, export_file, check_sound_dir
from func_crawler import reformat_writer

import_file_name = "TIME CNN english words - n-s.csv"
export_file_name = "anki " + import_file_name
check_sound_dir(True)

file, list_word, csv_line_num = import_file(import_file_name)
file.close()

file, csv_writer, csv_line_num = export_file(export_file_name)
list_word = list_word[csv_line_num:]
reformat_writer(csv_writer, list_word)
file.close()
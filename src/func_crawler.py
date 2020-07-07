import os, requests
import urllib.request as urlReq
from urllib.parse import urlparse
from tqdm import tqdm
from bs4 import BeautifulSoup
from func_potato import potato_cutter, potato_squeezer

def reformat_writer(csv_writer, list_word, soundDirPath):
    row_title = ["WORD", "PHR1", "PHR2", "PHR3",
                 "DEF1", "DEF2", "DEF3", "ETYM", "AUDI"]
    for word in tqdm(list_word):
        definition, news, anki_sound_tag = cambridge(word, soundDirPath)
        origin = etymology(word)

        row_word = [""] * len(row_title)
        row_word[0] = word
        for ii in range(0, min(3, len(news))):
            row_word[ii + 1] = news[ii]["exa"] \
                               + " (" + news[ii]["src"] + ")"
        for ii in range(0, min(3, len(definition))):
            row_word[ii + 4] = "<" + definition[ii]["pos"] \
                               + "> " + definition[ii]["def"] \
                               + "; " + definition[ii]["exa"]
        if origin["sub"] == "":
            row_word[-2] == ""
        else:
            row_word[-2] = origin["sub"] + "; " + origin["def"]
        row_word[-1] = anki_sound_tag
        csv_writer.writerow(row_word)

def cambridge(word, soundDirPath):
    target = f"https://dictionary.cambridge.org/us/dictionary/english/{word}"
    soup = BeautifulSoup(requests.get(target).text, "html.parser")
    definition = []
    news = []

    sound_file_folder = soundDirPath

    potato_tag = ["div", "class", "pr entry-body__el"]
    potatoes = potato_cutter(soup, potato_tag, 3)
    for potato in potatoes:
        juice_box = get_definition(potato)
        definition += juice_box

    potato_tag = ["div", "class", "lbb lb-cm lpt-10"]
    potatoes = potato_cutter(soup, potato_tag, 3)
    for potato in potatoes:
        juice_box = get_news(potato)
        news.append(juice_box)

    potato_tag = ["span", "class", "daud"]
    potatoes = potato_cutter(soup, potato_tag, 3)
    anki_sound_tag = get_sound(potatoes, sound_file_folder)

    return definition, news, anki_sound_tag

def etymology(word):
    target = f"https://www.etymonline.com/search?q={word}"
    soup = BeautifulSoup(requests.get(target).text, "html.parser")

    juice_tag = ["a", "class", "word__name--TTbAA word_thumbnail__name--1khEg"]
    subj = potato_squeezer(soup, juice_tag)
    juice_tag = ["section", "class", "word__defination--2q7ZH undefined"]
    desc = potato_squeezer(soup, juice_tag)
    origin = {"sub": subj, "def": desc}
    return origin

def get_definition(potato):
    juice_tag = ["div", "class", "posgram dpos-g hdib lmr-5"]
    posg = potato_squeezer(potato, juice_tag)
    potato_tag = ["div", "class", "def-block ddef_block"]
    potato_cubes = potato_cutter(potato, potato_tag, 3)
    juice_box = []
    for potato in potato_cubes:
        juice_tag = ["div", "class", "def ddef_d db"]
        defi = potato_squeezer(potato, juice_tag)
        juice_tag = ["div", "class", "examp dexamp"]
        exam = potato_squeezer(potato, juice_tag)
        juice_box.append({"pos": posg, "def": defi, "exa": exam})
    return juice_box

def get_news(potato):
    juice_tag = ["div", "class", "dsource lpr-20 pr"]
    sour = potato_squeezer(potato, juice_tag)[5:]
    juice_tag = ["span", "class", "deg"]
    phra = potato_squeezer(potato, juice_tag)
    juice_box = {"src": sour, "exa": phra}
    return juice_box

def get_sound(potatoes, sound_file_folder):
    anki_sound_tag = ""
    if not potatoes:
        return anki_sound_tag
    else:
        for potato in potatoes:
            if potato.find("source", {"type": "audio/mpeg"})["src"] is None:
                continue
            else:
                juice = potato.find("source", {"type": "audio/mpeg"})["src"]
                sound_file_url = "https://dictionary.cambridge.org" + juice
                if check_url(sound_file_url):
                    sound_file_name = os.path.basename(urlparse(sound_file_url).path)
                    urlReq.urlretrieve(sound_file_url,
                                            sound_file_folder + "/" + sound_file_name)
                    anki_sound_tag = f"[sound:{sound_file_name}]"
                    return anki_sound_tag
    return anki_sound_tag


def check_url(sound_file_url):
    try:
        u = urlReq.urlopen(sound_file_url)
        u.close()
        return True
    except:
        return False

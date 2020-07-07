import os, requests
import urllib.request as urlReq
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from potato import potatoCutter, potatoSqueezer

def cambridge(word, soundDirPath):
    target = f"https://dictionary.cambridge.org/us/dictionary/english/{word}"
    soup = BeautifulSoup(requests.get(target).text, "html.parser")
    defi = []
    news = []
    potatoTag = ["div", "class", "pr entry-body__el"]
    potatoes = potatoCutter(soup, potatoTag, 3)
    for potato in potatoes:
        juiceBox = getCambDefi(potato)
        defi += juiceBox
    potatoTag = ["div", "class", "lbb lb-cm lpt-10"]
    potatoes = potatoCutter(soup, potatoTag, 3)
    for potato in potatoes:
        juiceBox = getCambNews(potato)
        news.append(juiceBox)
    potatoTag = ["span", "class", "daud"]
    potatoes = potatoCutter(soup, potatoTag, 3)
    soundFileTag = getCambSound(potatoes, soundDirPath)
    return defi, news, soundFileTag

def getCambDefi(potato):
    juiceTag = ["div", "class", "posgram dpos-g hdib lmr-5"]
    posg = potatoSqueezer(potato, juiceTag)
    potatoTag = ["div", "class", "def-block ddef_block"]
    potato_cubes = potatoCutter(potato, potatoTag, 3)
    juiceBox = []
    for potato in potato_cubes:
        juiceTag = ["div", "class", "def ddef_d db"]
        defi = potatoSqueezer(potato, juiceTag)
        juiceTag = ["div", "class", "examp dexamp"]
        exam = potatoSqueezer(potato, juiceTag)
        juiceBox.append({"pos": posg, "def": defi, "exa": exam})
    return juiceBox

def getCambNews(potato):
    juiceTag = ["div", "class", "dsource lpr-20 pr"]
    sour = potatoSqueezer(potato, juiceTag)[5:]
    juiceTag = ["span", "class", "deg"]
    phra = potatoSqueezer(potato, juiceTag)
    juiceBox = {"src": sour, "exa": phra}
    return juiceBox

def getCambSound(potatoes, soundDirPath):
    soundFileTag = ""
    if not potatoes:
        return soundFileTag
    else:
        for potato in potatoes:
            if potato.find("source", {"type": "audio/mpeg"})["src"] is None:
                continue
            else:
                juice = potato.find("source", {"type": "audio/mpeg"})["src"]
                soundFileUrl = "https://dictionary.cambridge.org" + juice
                if checkSoundFileUrl(soundFileUrl):
                    soundFileName = os.path.basename(urlparse(soundFileUrl).path)
                    urlReq.urlretrieve(soundFileUrl,
                                            soundDirPath + "/" + soundFileName)
                    soundFileTag = f"[sound:{soundFileName}]"
                    return soundFileTag
    return soundFileTag

def etymology(word):
    target = f"https://www.etymonline.com/search?q={word}"
    soup = BeautifulSoup(requests.get(target).text, "html.parser")
    juiceTag = ["a", "class", "word__name--TTbAA word_thumbnail__name--1khEg"]
    subj = potatoSqueezer(soup, juiceTag)
    juiceTag = ["section", "class", "word__defination--2q7ZH undefined"]
    defi = potatoSqueezer(soup, juiceTag)
    etym = {"sub": subj, "def": defi}
    return etym

def checkSoundFileUrl(soundFileUrl):
    try:
        u = urlReq.urlopen(soundFileUrl)
        u.close()
        return True
    except:
        return False

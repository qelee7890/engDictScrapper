import re

def potatoCutter(soup, potatoTag, limit):
    """soup, potatoes are a <list> type."""
    if not soup:
        return []
    else:
        tag = potatoTag[0]
        tagId = potatoTag[1]
        tagValue = potatoTag[2]
        if soup.find(tag, {tagId: tagValue}) is None:
            return []
        else:
            potatoes = soup.find_all(tag, {tagId: tagValue}, limit=limit)
            return potatoes

def potatoSqueezer(potato, juiceTag):
    """ potato is a <list> type and juice a <string> type."""
    if not potato:
        return ""
    else:
        tag = juiceTag[0]
        tagId = juiceTag[1]
        tagValue = juiceTag[2]
        if potato.find(tag, {tagId: tagValue}) is None:
            return ""
        else:
            juice = trimText(potato.find(tag, {tagId: tagValue}).get_text().strip())
    return juice

def trimText(text):
    text = re.sub("\\xa0", " ", text)
    text = re.sub("\\\'s", "\'s", text)
    text = re.sub("\\n", "", text)
    text = re.sub(":", "", text)
    return text

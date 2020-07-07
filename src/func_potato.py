import re

def potato_cutter(soup, potato_tag, limit):
    """soup, potatoes are a <list> type."""
    if not soup:
        return []
    else:
        tag = potato_tag[0]
        tag_id = potato_tag[1]
        name = potato_tag[2]
        if soup.find(tag, {tag_id: name}) is None:
            return []
        else:
            potatoes = soup.find_all(tag, {tag_id: name}, limit=limit)
            return potatoes

def potato_squeezer(potato, juice_tag):
    """ potato is a <list> type and juice a <string> type."""
    if not potato:
        return ""
    else:
        tag = juice_tag[0]
        tag_id = juice_tag[1]
        name = juice_tag[2]
        if potato.find(tag, {tag_id: name}) is None:
            return ""
        else:
            juice = trim_text(potato.find(tag, {tag_id: name}).get_text().strip())
    return juice

def trim_text(text):
    text = re.sub("\\xa0", " ", text)
    text = re.sub("\\\'s", "\'s", text)
    text = re.sub("\\n", "", text)
    text = re.sub(":", "", text)
    return text

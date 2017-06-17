import re

# Remove all the html tags in the string
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def removesquares(text):
    return re.sub(r'\[.*?\]', ' ', cleanhtml(text))
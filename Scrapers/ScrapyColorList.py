from bs4 import BeautifulSoup
import lxml
import requests
import re

req = requests.get('http://cloford.com/resources/colours/500col.htm').content
soup = BeautifulSoup(req, 'lxml')

colors = {}

hexRe = re.compile(r'(#[A-Z0-9]+)')
rgbRe = re.compile(r'(\s(\d+)\s(\d+)\s(\d+))')
nameRe = re.compile(r'\s*([a-zA-Z]+\s*[a-zA-Z]*\s*\d*)\s*')

colorsList = []

table = soup.findAll('tr')
count = 0
outFile = open('colors.py', 'w+')
for row in table:
    nameMatch = nameRe.search(row.text)
    hexMatch = hexRe.search(row.text)
    rgbMatch = rgbRe.search(row.text)
    if nameMatch and rgbMatch and hexMatch:
        name = nameMatch.group(1).split('\n')[0]
        name = name.replace(' ', '').upper()
        r, g, b = rgbMatch.group(2), rgbMatch.group(3), rgbMatch.group(4)
        hex = hexMatch.group(1)
        hex = str(hex)
        count += 1
        line = "{} = ({}, {}, {}, '{}')\n".format(name.replace(' ', '').upper(), r, g, b, hex)
        colorsList.append((name, int(r), int(g), int(b), hex))
        print(colorsList[len(colorsList) - 1])
for row in sorted(colorsList[1:]):
    line = "{} = ({}, {}, {}, '{}')\n".format(*row)
    outFile.write(line)
print(count)
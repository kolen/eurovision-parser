import json
from sys import stdout
data = json.load(open("items.json"))

for row in data:
    year = row['year']
    for par in row['participants']:
        if par['place'] == 1:
            winner = par['performer']
            winning = par['song']
            descr = par['name']
    
    stdout.write((u"%s\t%s\t%s\t\t%s\r\n" % (year, winner, winning, descr)).encode('utf-8'))

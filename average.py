import json
import sys
from jinja2 import Environment, FileSystemLoader

data = json.load(open(sys.argv[1]))

countries = {} #mapping from countries to event title sets
rates = {} # (from, to) => [ (score, num_participants) ]
participants = {} # year_and_stage => set(countries)
average = {} # (from, to) => average

for row in data:
    year_and_stage = "%s %s" % (row['year'], row['stage'].strip())

    if year_and_stage not in participants:
        participants[year_and_stage] = set()

    participants[year_and_stage].add(row['country_from'])

for row in data:
    country_from = row['country_from']
    country_to = row['country_to']
    
    year_and_stage = "%s %s" % (row['year'], row['stage'].strip())
    
    if country_from not in countries:
        countries[country_from] = set()

    countries[country_from].add(year_and_stage)
    
    if (country_from, country_to) not in rates:
        rates[(country_from, country_to)] = []

    rates[(country_from, country_to)].append((int(row['score']), 
        len(participants[year_and_stage])))

for (c_from, c_to), entries in rates.iteritems():
    sum = 0
    for score, num_participants in entries:
        sum += score * num_participants
    avg = float(sum) / len(entries) 
    average[(c_from, c_to)] = avg 

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('base.html')

countries_list = countries.keys()
countries_list.sort()

fout = open("out.html", 'w')
fout.write(template.render(
    countries=countries,
    rates=rates,
    participants=participants,
    average=average,
    countries_list=countries_list,
))

import json
import sys
import itertools
from jinja2 import Environment, FileSystemLoader

data = json.load(open(sys.argv[1]))

countries = {} #mapping from countries to event title sets
rates = {} # (from, to) => [ (score, num_participants) ]
participants = {} # year_and_stage => set(countries)
average = {} # (from, to) => average

def replace_country(country):
    if country == "Serbia & Montenegro":
        return "Serbia"
    else:
        return country

for row in data:
    row['country_from'] = replace_country(row['country_from'])
    row['country_to'] = replace_country(row['country_to'])

for row in data:
    year_and_stage = ("%s %s" % (row['year'], row['stage'].strip())).strip()

    if year_and_stage not in participants:
        participants[year_and_stage] = set()

    participants[year_and_stage].add(row['country_from'])

for row in data:
    country_from = row['country_from']
    country_to = row['country_to']
    
    year_and_stage = ("%s %s" % (row['year'], row['stage'].strip())).strip()
    
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

for cs in participants.itervalues():
    for c_from, c_to in itertools.permutations(cs, 2):
        if (c_from, c_to) not in average:
            average[(c_from, c_to)] = 0.0 

countries_list = countries.keys()
countries_list.sort()

most_loved = [
    {
        'from': c_from,
        'to': c_to,
        'score': average.get((c_from, c_to), -1)
    }
    for c_from, c_to in itertools.permutations(countries_list, 2) ]
most_loved.sort(key=lambda x: x['score'], reverse=True)
most_loved = most_loved[:10]

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('base.html')

fout = open("out.html", 'w')
fout.write(template.render(
    countries=countries,
    rates=rates,
    participants=participants,
    average=average,
    countries_list=countries_list,
    most_loved=most_loved,
))

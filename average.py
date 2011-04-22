import json
import sys
import itertools
from jinja2 import Environment, FileSystemLoader

data = json.load(open(sys.argv[1]))

countries = {} #mapping from countries that voted to event title sets where 
               #voted
countries_all = set()
rates = {} # (from, to) => [ (score, num_participants) ]
average = {} # (from, to) => average

def replace_country(country):
    country = country.replace("&amp;", "&")
    if country == "Serbia & Montenegro":
        return "Serbia"
    else:
        return country

for evt in data:
    year_and_stage = ("%s %s" % (evt['year'], evt['stage'].strip())).strip()

    countries_voted_from = set()
    for score in evt['scores']:
        country_from = replace_country(score['country_from'])
        country_to = replace_country(score['country_to'])
        countries_voted_from.add(country_from)

        if (country_from, country_to) not in rates:
            rates[(country_from, country_to)] = []

        rates[(country_from, country_to)].append((int(score['score']), 
            len(evt['participants'])))

    for c in countries_voted_from:
        # Mark all participants x voted from
        for participant in evt['participants']:
            c2 = replace_country(participant['country'])
            if (c, c2) not in rates:
                rates[(c, c2)] = []

        if c not in countries:
            countries[c] = set()
        countries[c].add(year_and_stage)
        countries_all.add(c)

for (c_from, c_to), entries in rates.iteritems():
    sum = 0
    for score, num_participants in entries:
        sum += score * num_participants
    avg = float(sum) / len(countries[c_from]) 
    average[(c_from, c_to)] = avg

countries_list = list(countries_all)
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
    average=average,
    countries_list=countries_list,
    most_loved=most_loved,
))

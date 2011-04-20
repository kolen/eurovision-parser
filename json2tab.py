from json import load
from sys import stdin, stdout, argv

data = load(open(argv[1]))

keys = data[0].keys()
keys.sort()
stdout.write("%s\n" % "\t".join(keys))

for row in data:
    rows = [unicode(row.get(key, '')).replace("\t", " ").encode('utf-8') for key in keys]
    stdout.write("\t".join(rows))
    stdout.write("\n")

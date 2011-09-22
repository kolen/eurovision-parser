from json import load, dumps
from sys import stdin, stdout, argv

data = load(open(argv[1]))

keys = data[0].keys()
keys.sort()
stdout.write("%s\n" % "\t".join(keys))

for row in data:
    rows = []
    for key in keys:
        item = row.get(key, '')
        if isinstance(item, dict) or isinstance(item, list) or isinstance(item, tuple):
            item = dumps(item)

        item = unicode(item).replace(u"\t", u" ").encode("utf-8")
        rows.append(item)

    stdout.write("\t".join(rows))
    stdout.write("\n")

with open(r'.\Day6\input.txt') as thefile:

    rawtext = thefile.read()

rawtext = rawtext.replace('\n\n', '.').replace('\n', '')
entries = rawtext.split('.')
totalcount = 0

for i in entries:
#    entriescount.append((len(set(i))))
    totalcount += len(set(i))

print(totalcount)
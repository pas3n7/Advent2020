with open(r'.\Day6\input.txt') as thefile:

    rawtext = thefile.read().rstrip() #get rid of that trailing newline

rawtext = rawtext.replace('\n\n', '.').replace('\n', '-')
entries = rawtext.split('.')
matches = 0
for i in entries:
        memberscount= i.count('-') + 1
        i = i.replace('-', '')
        for n in set(i):
            if i.count(n) == memberscount:
                matches += 1

print(matches)
        
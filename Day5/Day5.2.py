seatIDs = []

with open(r'.\Day5\input.txt') as thefile:
    for line in thefile:
        row = int(line[0:7].replace("F", "0").replace("B", "1"), 2)
        seat = int(line[7:10].replace("R", "1").replace("L", "0"), 2)
        seatIDs.append((8*row)+seat)

#Need to find the missing number
#We can compare the sum of all numbers in the list to what we expect for the sum of the 
# complete series, the difference will
# be the missing number
#Thanks to Gauss, for a series from a to b it's = (b-a+1)(a+b)/2

firstseat = min(seatIDs)
lastseat = max(seatIDs)
expected = (lastseat-firstseat+1)*(lastseat+firstseat)//2
print(expected - sum(seatIDs))
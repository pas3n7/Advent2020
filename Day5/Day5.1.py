seatIDs = []

with open(r'.\Day5\input.txt') as thefile:
    for line in thefile:
        row = int(line[0:7].replace("F", "0").replace("B", "1"), 2)
        seat = int(line[7:10].replace("R", "1").replace("L", "0"), 2)
        seatIDs.append((8*row)+seat)
print(max(seatIDs))
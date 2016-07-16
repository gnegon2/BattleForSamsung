

fields = []
for y in range(4):
    row = []
    for x in range(4):
        row.append(0)
    fields.append(row)

fields[0][1] = 1
fields[1][1] = 1
localMap = []
localMap.append(fields[0][:2])
localMap.append(fields[1][:2])
print localMap
print fields
localMap[0][0] = 3
print localMap
print fields

import csv
with open('Postagged_words.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split() for line in stripped if line)
    print(stripped)
    with open('postag.csv', 'wb') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('Word', 'Postag'))
        writer.writerows(lines)

with open('postag.csv', 'r') as csvFile:
    data = list(csv.reader(csvFile))
    reader = csv.reader(csvFile)
    rows = [r for r in reader]
    rows = list(reader)

row_count = sum(1 for row in data)
print(row_count)
outputfile = open('output.csv', 'wb')
outputfile1 = open('output.txt', 'wb')
writer = csv.writer(outputfile)
wtire = csv.writer(outputfile1)
for i in range(2, row_count, 2):
    word = data[i][0]
    word2 = data[i][1]
    repWord = word2

    if word[0][0].isupper():
        hakhak = data[i][1].replace("PR", "Pangalan")
      #  hakhak = data[i][1].replace(repWord, "Pangalan")
        data[i][1] = hakhak
        try_list = data

print(data)
writer.writerows(data)
wtire.writerows(data)
# outputfile.write(data[i][1])
# print(word2)






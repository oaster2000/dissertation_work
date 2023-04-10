import csv, time, shutil
from tempfile import NamedTemporaryFile

count = 0

ids = []

for x in range(1, 16):
    i = 0
    filename = 'assets/random_sample_' + str(x) +'.csv'
    
    with open(filename, 'r+', encoding="utf8") as f:
        reader = csv.reader((i.replace('\0', '') for i in f), delimiter='␟')
        headers = next(reader)
        for row in reader:
            if len(row) <= 0:
                continue
            
            if row[0] in ids:
                continue
            
            ids.append(row[0])  
            count += 1
            i += 1
            label = ""
            topicDict = dict()
            with open('assets/frequent_terms.csv', 'r+', encoding="utf8") as f:
                term_reader = csv.reader((x.replace('\0', '') for x in f))
                for term in term_reader:
                    if term[0].casefold() in row[1].casefold():
                        topicDict[term[1]] = topicDict.get(term[1], 0) + int(term[2])
                    
            if len(topicDict) >= 1:
                label = max(topicDict, key=topicDict.get)
            else:
                label = "Unmarked"
            
            with open('assets/training_data.csv', 'a', encoding="utf8") as f:
                row_data = '␟'.join(row)
                f.write(row_data + '␟' + label + '\n')
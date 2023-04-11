import time

count = 0
file_count = 0

file_content = []

with open("assets/tweet_ids.txt", "r") as f:
    for line in f:
        count += 1
        if file_count >= 35:
            file_content.append(line)
            
        if count == 10000000:
            count = 0
            file_count += 1
            print("File number " + str(file_count) + " skipped!")
            
with open("assets/split/tweet_ids_" + str(file_count) + ".txt", "w+") as f:
    for line in file_content:
        f.write(line)

file_count += 1
print("File number " + str(file_count) + " completed!")
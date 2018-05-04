import re

with open('directory.txt', 'r', encoding='utf-8') as raw_file:
    raw_text = raw_file.read()
    lines = raw_text.split('\n')


primary_categories = []

secondary_categories = []

dirs = []

for line in lines:
    if line[-1:] == ":" and line[0] != "/":
        primary_categories.append(line)

# print(primary_categories[0])

ref_index = 2

for line in enumerate(lines):
    if line[1][-1:] == ":":
        # print(line[1:len(primary_categories[0])])
        if line[1][1:len(primary_categories[ref_index])] == primary_categories[ref_index][:-1]:
            secondary_categories.append(line)

i = 0

for dir in secondary_categories:
    
    while i < len(secondary_categories) - 1:
        span = secondary_categories[i + 1][0] - secondary_categories[i][0]
        # print(secondary_categories[i + 1][0], secondary_categories[i][0])
        temp_dirs = lines[secondary_categories[i][0]:secondary_categories[i + 1][0]]
        for line in temp_dirs:
            if line[-1:] != ":" and len(line) > 0:
                print(secondary_categories[i][1][:-1] + "/" + line)
        dirs.append(temp_dirs)

        i += 1

# for line in dirs:
#     for entry in line:
#         print(entry)
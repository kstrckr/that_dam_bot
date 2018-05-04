import re

with open('directory.txt', 'r', encoding='utf-8') as raw_file:
    raw_text = raw_file.read()
    lines = raw_text.split('\n')


primary_categories = []

for line in lines:
    if line[-1:] == ":" and line[0] != "/":
        primary_categories.append(line)

# print(primary_categories[0])

ref_index = 9

for line in lines:
    if line[-1:] == ":":
        # print(line[1:len(primary_categories[0])])
        if line[1:len(primary_categories[ref_index])] == primary_categories[ref_index][:-1]:
            print(line)
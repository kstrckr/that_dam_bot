import re

class DamDirs:

    primary_categories = []

    secondary_categories = []

    dirs = []

    def __init__(self, filename):
        with open(filename, 'r') as raw_file:
            raw_text = raw_file.read()
            lines = raw_text.split('\n')


        for line in lines:
            if line[-1:] == ":" and line[0] != "/":
                self.primary_categories.append(line)

        # print(self.primary_categories[0])

        ref_index = range(0,10)

        for i in ref_index:
            for line in enumerate(lines):
                if line[1][-1:] == ":":
                    # print(line[1:len(self.primary_categories[0])])
                    if line[1][1:len(self.primary_categories[i])] == self.primary_categories[i][:-1]:
                        self.secondary_categories.append(line)

        i = 0

        for dir in self.secondary_categories:
            
            while i < len(self.secondary_categories) - 1:

                if i == len(self.secondary_categories) - 2:
                    temp_dirs = lines[self.secondary_categories[i][0]:-3]
                else:
                    temp_dirs = lines[self.secondary_categories[i][0]:self.secondary_categories[i + 1][0]]

                for line in temp_dirs:
                    if line[-1:] != ":" and len(line) > 0:
                        path = "//Storage/Editorial Storage" + self.secondary_categories[i][1][:-1] + "/" + line
                        self.dirs.append(path)
                        
                i += 1

if __name__ == '__main__':
    
    output_parsing = DamDirs('directory.txt')

    with open('parsed_output.txt', 'w') as output_file:
        for line in output_parsing.dirs:
            write_line = line + "\n"
            output_file.write(write_line)
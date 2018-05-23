import re

class StillDamDirs:

    def __init__(self, text_file_to_parse):

        self.months = []

        self.subdir_index = []

        self.subdirs = []

        self.endpoints = []

        self.dirs = []

        with open(text_file_to_parse, 'r') as raw_text_file:
            raw_text = raw_text_file.read()
            lines = raw_text.split('\n')

            clean_lines = lines[9:-2]
            self.root_path = lines[-2:-1][0][6:]

        for line in enumerate(clean_lines):
            if line[1][-1:] == ':':
                self.months.append(line)

        prev_index = len(clean_lines) - 1

        for line in self.months[::-1]:
            self.subdir_index.append([line[0], prev_index])
            prev_index = line[0]

        for line in self.subdir_index:
            start = int(line[0])
            end = int(line[1])
            endpoint = clean_lines[start:end]

            clean_endpoint = []
            for point in endpoint:
                if point != '':
                    clean_endpoint.append(point)
            
            self.endpoints.append(clean_endpoint)

        for line in self.endpoints:
            full_path = self.root_path + "/" + line[0][:-1] + "/"
            for point in line[1:]:
                self.dirs.append(full_path + point)

        # for dir in self.dirs:
        #     print(dir)

        print(len(self.dirs))
            




if __name__ == '__main__':

    monthly_dirs = StillDamDirs('stills_2017.txt')

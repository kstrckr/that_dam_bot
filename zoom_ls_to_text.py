import shlex
import subprocess

class ZmLsToText:

    def generate_ls_txt(self):
        '''
        will return code 234 if not authenticated
        '''

        p = subprocess.Popen(self.args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        action = p.communicate()

        rc = p.returncode

        if rc == 0:
            with open(self.filename, 'w') as output_file:
                for line in action[1]:
                    output_file.write(line)

        return rc

    def __init__(self, zm_path, txt_file_name):

        self.filename = txt_file_name

        self.args = ['zm', 'ls', '-d', '2', zm_path, '2>', self.filename]

        self.tset_args = ['ls', '-a']

if __name__ == "__main__":

    test = ZmLsToText("/Post-Production/Photo Wonder/Complete/3-24", "test.txt")

    test.generate_ls_txt()




    
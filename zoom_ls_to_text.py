import shlex
import subprocess

class ZmLsToText:

    def generate_ls_txt(self):
        '''
        will return code 234 if not authenticated
        '''

        p = subprocess.Popen(self.args)

        action = p.communicate()

        rc = p.returncode

        return rc

    def __init__(self, zm_path, txt_file_name):

        self.args = ['zm', 'ls', '-d', '2', zm_path, '2>', txt_file_name]

        self.tset_args = ['ls', '-a']

if __name__ == "__main__":

    test = ZmLsToText("/Image Storage I/Product/Men/2xist/2xist_Underwear_MRTW_1028368234_11447_SELECTS", "test.txt")

    test.generate_ls_txt()




    
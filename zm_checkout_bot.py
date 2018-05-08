import shlex
import subprocess

from gamil_sender import EmailUpdate
from parse_list_output import DamDirs

def download_from_dirs_list(dirs_list):


    for path in dirs_list[50:75]:
        full_call = []

        full_call.extend(args)
        full_call.append(path)

        try:
            p = subprocess.check_call(full_call)
            message = path + ' has been downloaded'
            EmailUpdate(message).send_email_update()
            message = None
        except subprocess.CalledProcessError:
            EmailUpdate.send_email_update(path + ' has failed to download')

parsed_txt = DamDirs('directory.txt')

dirs = parsed_txt.dirs

args = ['zm', 'checkout', '--nowc', '-d', './']

# download_from_dirs_list(dirs)
import shlex
import subprocess

from database_setup_and_seed import DbSetup
# from gamil_sender import EmailUpdate
from parse_list_output import DamDirs

def insert_dirs_to_db(dirs_list):

    try:
        db = DbSetup('dirs.db')
        print('Database Connected')
    except:
        print('Error connecting to database')


    print('Creating Table')
    db.create_table()

    print('Inserting directory records')
    db.insert_dirs(dirs_list)


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

parsed_adult_dirs = DamDirs('directory.txt')
parsed_kid_dirs = DamDirs('kids_dirs.txt')

insert_dirs_to_db(parsed_adult_dirs.dirs)

# dirs = parsed_adult_dirs.dirs

args = ['zm', 'checkout', '--nowc', '-d', './']

# download_from_dirs_list(dirs)
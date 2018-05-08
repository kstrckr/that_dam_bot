import shlex
import subprocess

from database_setup_and_seed import DbSetup, DbInterface
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


def download_from_dirs_list(dir_to_download, args):


    full_call = []

    full_call.extend(args)
    full_call.append(dir_to_download)

    try:
        p = subprocess.check_call(full_call)
        message = dir_to_download + ' has been downloaded'
        # EmailUpdate(message).send_email_update()
        message = None
    except subprocess.CalledProcessError:
        pass
        # EmailUpdate.send_email_update(path + ' has failed to download')

# parsed_adult_dirs = DamDirs('zm_full_ls.txt')
# parsed_kid_dirs = DamDirs('zm_kids_ls.txt', parse_kids=True)


# print(len(parsed_kid_dirs.dirs))

# for path in parsed_kid_dirs.dirs:
#     print(path)


# insert_dirs_to_db(parsed_adult_dirs.dirs)
# insert_dirs_to_db(parsed_kid_dirs.dirs)

args = ['zm', 'checkout', '--nowc', '-d', './']

while (DbInterface.db_monitor()[0] > 0):
    print(DbInterface.db_monitor()[0])

    db_dir_record = DbInterface.return_single_directory()

    directory = db_dir_record[0]
    
    DbInterface.download_initiated(directory)
    download_from_dirs_list(directory, args)
    DbInterface.download_complete(directory)

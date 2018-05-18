import datetime
import logging
import shlex
import subprocess

from database_setup_and_seed import DbSetup, DbInterface
# from gamil_sender import EmailUpdate
from parse_list_output import DamDirs


def return_strf_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
        return True

    except subprocess.CalledProcessError:

        error_time = return_strf_now()

        print("\n\nZM Error encountered at {}\n\n".format(error_time))
        logging.debug("ZM Error encountered at {}".format(error_time))

        return False
        # EmailUpdate.send_email_update(path + ' has failed to download')

def zm_authenticate():

    user = "LOLnawD0g"
    pw = "bcryptrulez"

    auth_args = ['zm', '-s', 'EvolProd', '--username', user, '--password', pw, 'getcredentials']

    p = subprocess.Popen(auth_args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    interface = p.communicate()
    
    if p.poll() == 0:
        print("Login Successful")
        logging.info("Sucesfully Logged Back in at {}".format(return_strf_now()))
        return True
    else:
        print("Login ERROR")
        logging.debug('Login ERROR at {}'.format(return_strf_now()))

def zm_checkout_popen(dir_to_download):

    checkout_args = ['zm', 'checkout', '--nowc', '-d', '/Volumes/DAM_drive_2/stills_2016/']

    checkout_args.append(dir_to_download)

    p = subprocess.Popen(checkout_args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    try:
        print(u'Downloading {}'.format(dir_to_download[27:]))
        interface = p.communicate()



        if interface[1] == 'Authentication failed, please try again with valid credentials.\n':

            print('Attempting to log back in')
            logging.info('Attempting to log back in at {}'.format(return_strf_now()))

            zm_authenticate()

        
        return True

    except subprocess.CalledProcessError:

        error_time = return_strf_now()

        print("\n\nZM Error encountered at {}\n\n".format(error_time))
        logging.debug("ZM Error encountered at {}".format(error_time))

        return False


# parsed_adult_dirs = DamDirs('zm_full_ls.txt')
# parsed_kid_dirs = DamDirs('zm_kids_ls.txt', parse_kids=True)


# print(len(parsed_kid_dirs.dirs))

# for path in parsed_kid_dirs.dirs:
#     print(path)


# insert_dirs_to_db(parsed_adult_dirs.dirs)
# insert_dirs_to_db(parsed_kid_dirs.dirs)

if __name__ == "__main__":

    
    args = ['zm', 'checkout', '--nowc', '-d', "./"]

    logging.basicConfig(filename='zm_checkout_log.log',level=logging.DEBUG)

    logging.info("Downloads started at {}".format(return_strf_now()))

    while (DbInterface.db_monitor()[0] > 0):
        try:
            print('{} Directories Remaining'.format(DbInterface.db_monitor()[0]))

            db_dir_record = DbInterface.return_single_directory()

            directory = db_dir_record[0]
            
            DbInterface.set_download_initiated(directory, 1)

            # downloaded = download_from_dirs_list(directory, args)
            downloaded = zm_checkout_popen(directory)

            if downloaded:
                DbInterface.set_download_complete(directory, 1)
            else:
                DbInterface.set_download_initiated(directory, 0)
        except KeyboardInterrupt:
            print("\n\nDownload stopped manually, restart process to resume")
            logging.info("Downloads manually stopped at {}".format(return_strf_now()))
            break
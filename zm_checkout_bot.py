import datetime
import logging

from authenticator import Authenticator as Auth
from database_setup_and_seed import DbSetup, DbInterface
from parse_stills_txt_to_path import StillDamDirs
from zoom_checkout import ZmCheckoutSession
from zoom_ls_to_text import ZmLsToText


def return_strf_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":

    auth = Auth()
    auth.login()

    dam_checkout_target = raw_input("Please paste the DAM path to target for subdirectory checkout: ")

    db_name = 'current_batch.db'
    current_targets_txt = 'current_targets.txt'

    logging.basicConfig(filename='zm_checkout_log.log',level=logging.DEBUG)

    target_dirs = ZmLsToText(dam_checkout_target, current_targets_txt)

    target_dirs.generate_ls_txt()

    current_db = DbSetup(db_name)

    current_db.create_table()

    current_data = StillDamDirs(current_targets_txt)
    
    insert_data = current_db.insert_dirs(current_data.dirs)

    dbMonitor = DbInterface(db_name)
    

    # logging.info("Downloads started at {}".format(return_strf_now()))

    while (dbMonitor.db_monitor(db_name)[0] > 0):
        try:
            print('{} Directories Remaining'.format(dbMonitor.db_monitor(db_name)[0]))

            db_dir_record = dbMonitor.return_single_directory(db_name)

            directory = db_dir_record[0]
            
            dbMonitor.set_download_initiated(directory, 1, db_name)

            # downloaded = download_from_dirs_list(directory, args)
            downloaded = ZmCheckoutSession.checkout_a_dir('./', directory)

            if downloaded:
                dbMonitor.set_download_complete(directory, 1, db_name)
            else:
                dbMonitor.set_download_initiated(directory, 0, db_name)
        except KeyboardInterrupt:
            print("\n\nDownload stopped manually, restart process to resume")
            logging.info("Downloads manually stopped at {}".format(return_strf_now()))
            break
import datetime
import logging

import bot_modules as m

# from authenticator import Authenticator as Auth
# from database_setup_and_seed import DbSetup, DbInterface
# from parse_stills_txt_to_path import m.StillDamDirs
# from zoom_checkout import m.ZmCheckoutSession
# from zoom_ls_to_text import m.ZmLsToText


def return_strf_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":

    logged_in = False

    auth = m.Authenticator()

    while (not logged_in):
        logged_in = auth.login()

        if (not logged_in):
            auth.enter_credentials()

    db_name = 'current_batch.db'
    current_targets_txt = 'current_targets.txt'

    current_db = m.DbSetup(db_name)
    current_db.create_table()
    dbMonitor = m.DbInterface(db_name)

    raw_local_dir_path = raw_input("Please specify the local path to download to: ")

    local_dir_path = raw_local_dir_path.strip()

    if (dbMonitor.db_monitor(db_name)[0] == 0):

        dam_checkout_target = raw_input("Please paste the DAM path to target for subdirectory checkout: ")

        target_dirs = m.ZmLsToText(dam_checkout_target, current_targets_txt)

        target_dirs.generate_ls_txt()

        current_data = m.StillDamDirs()

        current_data.parse_txt(current_targets_txt)
    
        insert_data = current_db.insert_dirs(current_data.dirs)

    else:
        print("Continuintinuing to download directory in progress.\n")

    logging.basicConfig(filename='zm_checkout_log.log',level=logging.DEBUG)

    
    

    # logging.info("Downloads started at {}".format(return_strf_now()))

    while (dbMonitor.db_monitor(db_name)[0] > 0):
        try:
            print('{} Directories Remaining'.format(dbMonitor.db_monitor(db_name)[0]))

            db_dir_record = dbMonitor.return_single_directory(db_name)

            directory = db_dir_record[0]
            
            dbMonitor.set_download_initiated(directory, 1, db_name)

            # downloaded = download_from_dirs_list(directory, args)
            downloaded = m.ZmCheckoutSession.checkout_a_dir(local_dir_path, directory)
            
            if downloaded == 0:
                dbMonitor.set_download_complete(directory, 1, db_name)
            elif downloaded == 234:
                dbMonitor.set_download_initiated(directory, 0, db_name)
                auth.login()

        except KeyboardInterrupt:
            print("\n\nDownload stopped manually, restart process to resume")
            logging.info("Downloads manually stopped at {}".format(return_strf_now()))
            break
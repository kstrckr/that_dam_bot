import datetime
import sqlite3

class DbSetup:

    create_table_cmd = u'''CREATE TABLE IF NOT EXISTS dirs (
        dir TEXT,
        in_progress BOOLEAN,
        start_time INTEGER,
        finish_time INTEGER,
        download_complete BOOLEAN,
        UNIQUE(dir))
    '''

    insert_rows_cmd = u'''INSERT INTO dirs VALUES (?, ?, ?, ?, ?);
    '''

    def return_connect(self):

        return self.conn

    def create_table(self):

        with self.conn as conn:
            conn.execute(self.create_table_cmd)

    def insert_dirs(self, insert_data):


        list_of_insert_values = []
        
        

        for line in insert_data:
            
            list_of_insert_values.append((line.decode('utf-8'), 0, None, None, 0))

        print(len(list_of_insert_values))
        with self.conn as conn:
            conn.executemany(self.insert_rows_cmd, list_of_insert_values)

    def __init__(self, db_name):

        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)

class DbInterface:

    query = 'SELECT * FROM dirs WHERE download_complete = 0 LIMIT 1'
    db_name = 'stills_2016.db'

    @classmethod
    def db_monitor(self):

        with sqlite3.connect(self.db_name) as conn: 
            cur = conn.cursor()

            queue_count = cur.execute('SELECT COUNT(*) FROM dirs WHERE download_complete = 0')
            queue_check = cur.fetchone()

        return queue_check
    
    @classmethod
    def return_single_directory(self):
        
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()

            cur.execute(self.query)

            db_entry = cur.fetchone()
            

        single_download_directory = db_entry
        
        return single_download_directory
    
    @classmethod
    def set_download_initiated(self, dir_in_progress, value):
        
        if value == 1:
            download_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            download_start = None

        sql_values = [value, download_start, dir_in_progress]

        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()

            cur.execute('UPDATE dirs SET in_progress = ?, start_time=? WHERE dir = ?', sql_values)

    @classmethod
    def set_download_complete(self, dir_complete, value):

        if value == 1:
            download_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            download_end = None

        sql_values = [value, download_end, dir_complete]

        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()

            cur.execute('UPDATE dirs SET in_progress = 0, download_complete = ?, finish_time = ? WHERE dir = ?', sql_values)

if __name__ == '__main__':

    from parse_stills_txt_to_path import StillDamDirs

    dirs_2017 = StillDamDirs('stills_2016.txt')

    still_dirs_2017 = DbSetup('stills_2016.db')

    still_dirs_2017.create_table()
    still_dirs_2017.insert_dirs(dirs_2017.dirs)

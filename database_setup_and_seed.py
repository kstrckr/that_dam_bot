import sqlite3

class DbSetup:

    create_table_cmd = '''CREATE TABLE IF NOT EXISTS dirs (
        dir TEXT,
        in_progress BOOLEAN,
        start_time INTEGER,
        finish_time INTEGER,
        download_complete BOOLEAN,
        UNIQUE(dir))
    '''

    insert_rows_cmd = '''INSERT INTO dirs (
        VALUES (?, ?, ?, ?, ?)
    )

    '''

    def return_connect(self):

        return self.conn

    def create_table(self):

        with self.conn as conn:
            conn.execute(self.create_table_cmd)

    def insert_dirs(self, insert_data):

        list_of_insert_values = []
        
        for line in insert_data:
            list_of_insert_values.append((line, 0, '', '', 0))

        self.conn.execute(self.insert_rows_cmd, list_of_insert_values)

    def __init__(self, db_name):

        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
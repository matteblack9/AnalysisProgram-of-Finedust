import sqlite3
import csv


class DBWeather:
    _sql_create_weather_table = """ CREATE TABLE IF NOT EXISTS weather (
                        station text,
                        date integer,
                        precipitation real,
                        direction integer,
                        velocity real,
                        year integer,
                        month integer,
                        day integer,
                        hour integer,
                        primary key(station, date)                    
                        ); """

    def __init__(self, db_file):
        self.db_file = db_file

        # create a database connection
        self.conn = self._create_connection(db_file)

        if self.conn is not None:
            # create table
            self._create_table(self.conn, self._sql_create_weather_table)
        else:
            print("E : cannot create the DB connection")

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def insert_from_csv(self, csv_files, stations):
        for file_name in csv_files:
            file = open(file_name, 'r')
            reader = csv.reader(file)
            for line in reader:
                if line[0] in stations:
                    values = []
                    values.append(line[0]) # station

                    year = line[1][:4]
                    month = line[1][5:7]
                    day = line[1][8:10]
                    hour = line[1][11:13]

                    date = year + month + day + hour
                    values.append(date) # date

                    values.append(line[3]) # precipitation

                    values.append(line[5]) # direction

                    values.append(line[4]) # velocity

                    values.append(year)
                    values.append(month)
                    values.append(day)
                    values.append(hour)

                    self._insert_table(self.conn, self._sql_insert_weather_table, values)
            self.conn.commit()
            file.close()

    def get_row_num(self):
        cur = self.conn.cursor()
        sql = 'select count(*) from weather'
        cur.execute(sql)
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_date(self):
        cur = self.conn.cursor()
        sql = 'select * from weather'
        cur.execute(sql)
        try:
            return cur.fetchall()
        except Exception:
            return None

    _sql_insert_weather_table = """insert into weather(
                                station,
                                date,
                                precipitation,
                                direction,
                                velocity,
                                year,
                                month,
                                day,
                                hour
                                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    @staticmethod
    def _create_connection(db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Exception as e:
            print("error : ", e)

        return None

    @staticmethod
    def _create_table(conn, create_table_sql):
        try:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
        except Exception as e:
            print("create table error : ", e)

    @staticmethod
    def _insert_table(conn, insert_table_sql, values):
        try:
            cursor = conn.cursor()
            cursor.execute(insert_table_sql, values)
        except Exception as e:
            print("insert error : ", e)
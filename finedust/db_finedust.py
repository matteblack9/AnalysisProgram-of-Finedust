# -*- coding: utf-8 -*-

import sqlite3
import csv


class DBFineDust:
    _sql_create_dust_table = """ CREATE TABLE IF NOT EXISTS dust (
                    area text NOT NULL,
                    station_code integer NOT NULL,
                    station_name text NOT NULL,
                    date integer NOT NULL,
                    so2 real,
                    co real,
                    o3 real,
                    no2 real,
                    pm10 integer,
                    pm25 integer,
                    address text,
                    year integer NOT NULL,
                    month integer NOT NULL,
                    day integer NOT NULL,
                    hour integer NOT NULL,
                    primary key(station_name, date)                    
                    ); """

    def __init__(self, db_file):
        self.db_file = db_file

        # create a database connection
        self.conn = self._create_connection(db_file)

        if self.conn is not None:
            # create table
            self._create_table(self.conn, self._sql_create_dust_table)
        else:
            print("E : cannot create the DB connection")

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def insert_from_csv(self, csv_files, stations):
        # insert data to DB
        if isinstance(csv_files, list):
            for file_name in csv_files:
                self._insert_csv(file_name, stations)
        else:
            self._insert_csv(csv_files, stations)

    def _insert_csv(self, file_name, stations):
        file = open(file_name, 'rw')
        reader = csv.reader(file)
        for line in reader:
            if line[2] in stations:
                the_line = line
                line[3] = self._hour24to0(line[3])
                the_line.append(line[3][0:4])   # year
                the_line.append(line[3][4:6])   # month
                the_line.append(line[3][6:8])   # day
                the_line.append(line[3][8:10])  # hour
                self._insert_table(self.conn, self._sql_insert_dust_table, the_line)
        self.conn.commit()
        file.close()

    def insert_from_csv_all(self, csv_files):
        # insert data to DB
        if isinstance(csv_files, list):
            for file_name in csv_files:
                self._insert_csv_all(file_name)
        else:
            self._insert_csv_all(csv_files)

    def _insert_csv_all(self, file_name):
        file = open(file_name, 'r')
        reader = csv.reader(file)
        for line in reader:
            if "부산" in line[0]: 
                the_line = line
                line[3] = self._hour24to0(line[3])
                the_line.append(line[3][0:4])   # year
                the_line.append(line[3][4:6])   # month
                the_line.append(line[3][6:8])   # day
                the_line.append(line[3][8:10])  # hour
                self._insert_table(self.conn, self._sql_insert_dust_table, the_line)
        self.conn.commit()
        file.close()

    @staticmethod
    def _hour24to0(date):
        if date[8:10] == '24':
            hour = '00'  # hour
            day = date[6:8]
            month = date[4:6]
            year = date[0:4]

            month31 = ['01','03','05','07','08','10','12']
            month30 = ['04','06','09','11']
            leapYear = ['2016', '2012']

            if date[4:6] in month31 and date[6:8] == '31':
                month = ('0' + str(int(date[4:6]) + 1))[-2:] # month
                day = '01'    # day

            elif date[4:6] in month30 and date[6:8] == '30':
                month = ('0' + str(int(date[4:6]) + 1))[-2:] # month
                day = '01'  # day

            elif date[4:6] == '02' and date[0:4] in leapYear and date[6:8] == '29':
                month = ('0' + str(int(date[4:6]) + 1))[-2:]  # month
                day = '01'  # day

            elif date[4:6] == '02' and date[0:4] not in leapYear and date[6:8] == '28':
                month = ('0' + str(int(date[4:6]) + 1))[-2:]  # month
                day = '01'  # day

            else:
                day = ('0' + str(int(date[6:8]) + 1))[-2:]

            if int(date[4:6]) == 13:
                month = '01'
                year = str(int(date[0:4]) + 1)
        else:
            return date
        modified = year + month + day + hour
        return modified

    def get_row_num(self):
        cur = self.conn.cursor()
        sql = 'select count(*) from dust'
        cur.execute(sql)
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_row_num_station(self, station):
        cur = self.conn.cursor()
        sql = 'select count(*) from dust where station_name = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_all(self):
        # get all data
        cur = self.conn.cursor()
        sql = 'select * from dust'
        cur.execute(sql)
        return cur.fetchall()

    def get_all_option(self, station, date):
        # get all options fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct * from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        return cur.fetchone()

    def get_area(self, station):
        # get area fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct area from dust where station_name = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_station_code(self, station):
        # get station code fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct station_code from dust where station_name = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_station_name(self, station_code):
        # get station name fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct station_name from dust where station_code = :code'
        cur.execute(sql, {"code": station_code})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_so2(self, station, date):
        # get SO2 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct so2 from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_co(self, station, date):
        # get CO fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct co from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_o3(self, station, date):
        # get O3 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct o3 from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_no2(self, station, date):
        # get NO2 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct no2 from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_pm10(self, station, date):
        # get pm10 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct pm10 from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_pm25(self, station, date):
        # get pm2.5 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct pm25 from dust where station_name=?'
        cur.execute(sql, (station))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_pm25_alldate(self, station):
        # get pm2.5 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct pm10 from dust where station_name=?'
        cur.execute(sql, (station))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_pm25_alldate(self, station):
        # get pm2.5 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct pm25 from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None    

    def get_address(self, station):
        # get station code fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct address from dust where station_name = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_all_pm10_by_station(self, station):
        cur = self.conn.cursor()
        sql = 'select distinct pm10 from dust where station_name = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_all_pm10_by_station_at_time(self, station, time_from, time_to):
        cur = self.conn.cursor()
        sql = 'select distinct pm10 from dust where station_name=? and hour >= ? and hour <= ?'
        cur.execute(sql, (station, time_from, time_to))
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_all_pm10_by_station_at_month(self, station, year, month):
        cur = self.conn.cursor()
        sql = 'select distinct pm10 from dust where station_name=? and year =? and month=?'
        cur.execute(sql, (station, year, month))
        try:
            return cur.fetchall()
        except Exception:
            return None
        
    def get_all_pm25_by_station_at_month(self, station, year, month):
        cur = self.conn.cursor()
        sql = 'select distinct pm25 from dust where station_name=? and year=? and month=?'
        cur.execute(sql, (station, year, month))
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_alldate_pm25_allstation_at_month(self, year, month):
        cur = self.conn.cursor()
        sql = 'select distinct date from dust where year=? and month=?'
        cur.execute(sql, (year, month))
        try:
            return cur.fetchall()
        except Exception:
            return None
        
    def get_alldate_pm10_allstation_at_month(self, year, month):
        cur = self.conn.cursor()
        sql = 'select distinct date from dust where year=? and month=?'
        cur.execute(sql, (year, month))
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_all_pm25_allstation_at_month(self, year, month):
        cur = self.conn.cursor()
        sql = 'select distinct pm25 from dust where year=? and month=?'
        cur.execute(sql, (year, month))
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_all_pm10_allstation_at_month(self, year, month):
        cur = self.conn.cursor()
        sql = 'select distinct pm25 from dust where year=? and month=?'
        cur.execute(sql, (year, month))
        try:
            return cur.fetchall()
        except Exception:
            return None
        
    def get_all_pm25_by_station_at_month(self, station, year, month):
        cur = self.conn.cursor()
        sql = 'select distinct pm25 from dust where station_name=? and month=?'
        cur.execute(sql, (station, month))
        try:
            return cur.fetchall()
        except Exception:
            return None
        
    def get_all_pm25(self):
        cur = self.conn.cursor()
        sql = 'select distinct pm25 from dust'
        cur.execute(sql)
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_all_by_day(self, station,year,month, day):
        cur = self.conn.cursor()
        sql = 'select distinct * from dust where station_name=? and year=? and month=? and day == ?'
        cur.execute(sql, (station, year, month, day))
        try:
            return cur.fetchall()
        except Exception:
            return None

    _sql_insert_dust_table = """insert into dust(
                             area,
                             station_code,
                             station_name,
                             date,
                             so2,
                             co,
                             o3,
                             no2,
                             pm10,
                             pm25,
                             address,
                             year,
                             month,
                             day,
                             hour
                             ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

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
            print("insert error : ", e , values)

"""
# db_finedust.DBFineDust(DB 파일 이름) : 객체 만들기
fine_dust = db_finedust.DBFineDust(db_file_name)

# fine_dust.insert_from_csv(csv 파일[에어코리아 미세먼지 csv] list, 원하는 측정소 이름 list)
# 입력한 csv 파일들에서 원하는 측정소의 데이터를 읽어서 DB 파일에 넣는다.
# 중요!!! -> DB 파일에 이미 insert 했으면 또 할 필요 없음!!!! 주석 처리해!!!!!
# error :  UNIQUE constraint failed: dust.station_name, dust.date 라고 막 뜨는건 이미 넣은 거 또 넣으려고 해서 뜨는건데 값에 영향을 주지는 않음
fine_dust.insert_from_csv(csv_file_list, station_list)

# 객체.get_row_num() : DB 행 개수 리턴
print(fine_dust.get_row_num())

# 객체.get_all() : DB에 저장된 모든 데이터 리턴, 너무 길어서 쓸 일은 없을 듯
print(fine_dust.get_all())

# 객체.get_all_option(측정소 이름, 시각 - yyyymmddhh string도 되고 int도 됨)
# 원하는 측정소의 원하는 시각의 위치, 측정소코드, 측정소이름, SO2, CO, O3, NO2, PM10(미세먼지), PM2.5(초미세먼지), 주소를 리턴
print(fine_dust.get_all_option('부곡동', '2016012213')) # 또는
print(fine_dust.get_all_option('부곡동', 2016012213))

# 객체.get_area(측정소 이름) : 지역 리턴
print(fine_dust.get_area('부곡동'))

# 객체.get_station_code(측정소 이름) : 측정소 코드 리턴
print(fine_dust.get_station_code('부곡동'))

# 객체.get_station_name(측정소 코드) : 측정소 이름 리턴
print(fine_dust.get_station_name('221251'))

# 객체.get_so2(측정소이름, 시각) : SO2 리턴
print(fine_dust.get_so2('부곡동', '2016012213'))

# 객체.get_co(측정소이름, 시각) : CO 리턴
print(fine_dust.get_co('부곡동', '2016012213'))

# 객체.get_o3(측정소이름, 시각) : O3 리턴
print(fine_dust.get_o3('부곡동', '2016012213'))

# 객체.get_no2(측정소이름, 시각) : NO2 리턴
print(fine_dust.get_no2('부곡동', '2016012213'))

# 객체.get_pm10(측정소이름, 시각) : 미세먼지 pm10 리턴
print(fine_dust.get_pm10('부곡동', '2016012213'))

# 객체.get_pm25(측정소이름, 시각) : 초미세먼지 pm2.5 리턴
print(fine_dust.get_pm25('부곡동', '2016012213'))

# 객체.get_address(측정소이름) : 주소 리턴
print(fine_dust.get_address('부곡동'))

# 시각 파라미터는 integer string 상관 없음
# 없는 데이터는 None 리턴
"""

import db_finedust, db_weather
import numpy as np
from PIL import Image
from PIL import ImageDraw, ImageFont

db_file_name_dust = 'fine_dust.db'
db_file_name_weather = 'weather.db'

csv_file_list_dust = ['2016년 1분기.csv',
                    '2016년 2분기.csv',
                    '2016년 3분기.csv',
                    '2016년 4분기.csv']

station_list_dust = ['장림동','녹산동','화전동','지사동']

#weather_file_name = ["2016_중구_종관_기상.csv"]
#weather_station = ["159"]

# Busan yellow dust date from 'http://www.kma.go.kr'
date_yellow_dust = ['20160409', '20160410', '20160414', '20160423', '20160424', '20160507', '20160508']

"""
xy_image = [(220, 330), # 중구 광복동
            (295, 255), # 수영구 광안동
            (395, 150), # 기장군 기장읍
            (73, 340),  # 강서구 녹산동
            (205, 300), # 서구 대신동
            (268, 285), # 남구 대연동
            (150, 198), # 강서구 대저동
            (203, 205), # 북구 덕천동
            (274, 212), # 동래구 명장동
            (277, 184), # 금정구 부곡동
            (228, 292), # 동구 수정동
            (266, 234), # 연제구 연산동
            (0, 0),     # 동래구 온천동
            (347, 80),  # 기장군 용수리
            (183, 350), # 사하구 장림동
            (231, 258), # 부산진구 전포동
            (348, 261), # 해운대구 좌동
            (282, 134), # 금정구 청룡동
            (0, 0),     # 동구 초량동
            (254, 335), # 영도구 태종대
            (170, 262)] # 사상구 학장동

"""
# 미세먼지 DB
fine_dust = db_finedust.DBFineDust(db_file_name_dust)

fine_dust.insert_from_csv_all(csv_file_list_dust)

# 기상 DB
#weather = db_weather.DBWeather(db_file_name_weather)

#weather.insert_from_csv(weather_file_name, weather_station)

# -----------------------------------


def main():

   list = []
   k = 0
   db_val = fine_dust.get_all_pm25()
   for i in db_val:
      list.append(i)
      k = k + 1
   print(list)
   print(k)

   """
   for station in station_list_dust:
      get_aver_of_station(fine_dust, "pm10", station)
      print("\n")

   average_of_allstation(fine_dust, "pm10")
   """
    # print(weather.get_date())

"""
def get_map():
    pm10_in_stations = []
    # 1년 평균
    i = 0
    for station in station_list_dust:
        pm10_of_station = get_aver_pm10_of_station(fine_dust, station)
        pm10_in_stations.append(pm10_of_station)
        i += 1
        print(i, fine_dust.get_area(station), station, pm10_of_station)
"""
#    img = Image.open("busandust.png")
#    font = ImageFont.truetype("arial.ttf", 15)
#    draw = ImageDraw.Draw(img)

#    draw.text((10, 10), "2016 year average fine dust each station", (0, 0, 0), font)
#    for i, station in enumerate(station_list_dust):
#        if station != "초량동" and station != "온천동":
#            draw.text(xy_image[i], str(int(pm10_in_stations[i])), (255, 0, 0), font)

#    img.show()

def get_aver_of_station(db, pm, station):
    aver_month = []
    for i in range(1,13):
       list = []
       if pm == 'pm10':
          db_value = db.get_all_pm10_by_station_at_month(station, 2016, i)
       elif pm == 'pm25':
          db_value = db.get_all_pm25_by_station_at_month(station, 2016, i)
       for li in db_value:
          if li[0] != '':
             list.append(li[0])
       aver_month.append(np.average(list))
    for i in aver_month:
       print("{0:.2f}".format(i))


def average_of_allstation(db, pm):
   total_aver_month = []
   k = 0
   t = 0
   for i in range(1,13):
      list = []
      listt = []
      if pm == 'pm10':
         db_value = db.get_all_pm10_allstation_at_month(2016, i)
         db_date = db.get_alldate_pm10_allstation_at_month(2016, i)
      elif pm == 'pm25':
         db_value = db.get_all_pm25_allstation_at_month(2016, i)
         db_date = db.get_alldate_pm25_allstation_at_month(2016, i)
      for li in db_value:
         if li[0] != ' ':
            list.append(li[0])
            k = k + 1
      for li in db_date:
         if li[0] != ' ':
            listt.append(li[0])
            t = t + 1
      print("\n")
      print(i,"-----------------\n")
      print(list)
      print(listt)
      print("\n")
      print(k)
      print(t)
      print("\n")
      k = 0
     # total_aver_month.append(np.mean(list))
   for i in total_aver_month:
      print("{0:.2f}".format(i))

if __name__ == '__main__':
    main()

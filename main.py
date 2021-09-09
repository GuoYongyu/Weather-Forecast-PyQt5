'''
Author: your name
Date: 2021-09-09 11:44:29
LastEditTime: 2021-09-09 14:30:44
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \dbpolicye:\Codes\C++\weather_forecast\main.py
'''
from spider import *
from ui_Window import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QApplication
import sys
import pygame
import json
import time

file_path = './json_data/'
image_path = './image/'
ch2en = {
    '晴': 'sunny.png', '阴': 'overcast.png', '多云': 'cloudy.png', 
    '雨': 'rainy.png', '冰雹': 'ice_rain.png', '雾': 'foggy.png',
    '霾': 'haze.png', '雪': 'snowy.png', '沙尘': 'sand.png',
    '大雨': 'rainy.png', '中雨': 'rainy.png', '小雨': 'rainy.png',
    '暴雨': 'rainy.png', '大雪': 'snowy.png', '小雪': 'snowy.png',
    '中雪': 'snowy.png', '暴雪': 'snowy.png', '大雾': 'foggy.png',
    '雨夹雪': 'sleet.png', '沙尘暴': 'sand.png',
}

def get_date():
    date = time.strftime("%d/%m/%Y")
    date = date.split('/')
    date = date[1] + '月' + date[0] + '日'
    return date

def  internet_connected():
    try:
        html = requests.get("http://www.baidu.com", timeout=2)
    except:
        return False
    return True

class Forecast(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Forecast, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        pygame.init()
        self.setWindowTitle('天气预报')
        self.setFixedSize(self.width(), self.height())
        self.ui.cur_city_tb.setText('北京')
        self.bkg_music_path = './music/background.mp3'
        self.music_playing = True
        self.spider = Spider()
        self.initialize()
    
    def initialize(self):
        self.ui.music_btn.clicked.connect(self.music_btn_clicked)
        self.ui.search.clicked.connect(self.search_btn_clicked)
        if not internet_connected():
            self.no_internet()
            return
        self.spider.sparse('北京')
        self.play_music()
        self.draw_current_weather()
        self.draw_time_weather()
        self.draw_future_weather()

    def play_music(self):
        pygame.mixer.music.load(self.bkg_music_path)
        pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    def music_btn_clicked(self):
        self.music_playing = not self.music_playing
        if self.music_playing:
            self.play_music()
        else:
            self.stop_music()

    def search_btn_clicked(self):
        self.ui.wrong_city.setText('')
        city = self.ui.input_city.text()
        ret = self.spider.sparse(city)
        if ret == False:
            self.wrong_city()
            return
        self.draw_current_weather()
        self.draw_time_weather()
        self.draw_future_weather()
        self.successful_search()

    def wrong_city(self):
        self.ui.wrong_city.setText("<font color='red'>城市不存在或暂时无法查询！</font>")

    def no_internet(self):
        self.ui.wrong_city.setText("<font color='red'>网络未连接！</font>")

    def successful_search(self):
        self.ui.wrong_city.setText("<font color='green'>查询成功！</font>")

    def draw_current_weather(self):
        with open(file_path + 'current_weather.json', 'r', encoding='utf-8') as f:
            cur = json.load(f)
        self.ui.cur_update.setText(cur['update_time'])
        self.ui.cur_time.setText(get_date() + cur['day'])
        self.ui.cur_temp.setText(cur['temperature'])
        self.ui.cur_sunrise.setText(cur['sunrise_time'])
        self.ui.cur_sunfall.setText(cur['sunfall_time'])
        self.ui.cur_weather.setText(cur['weather'])
        wea = cur['weather'].split('转')
        wea1 = wea[0]
        wea2 = wea[-1]
        self.ui.cur_wea1.setStyleSheet(
            "QPushButton{background-image:url(:" + image_path + ch2en[wea1] + ");border-radius: 20px;}"
        )
        self.ui.cur_wea2.setStyleSheet(
            "QPushButton{background-image:url(:" + image_path + ch2en[wea2] + ");border-radius: 20px;}"
        )

    def draw_time_weather(self):
        with open(file_path + 'time_weather.json', 'r', encoding='utf-8') as f:
            cur = json.load(f)
        time_wea = {
            'time_0': [self.ui.time_1, self.ui.weather_1, self.ui.temp_1, self.ui.wind_1, self.ui.degree_1],
            'time_1': [self.ui.time_2, self.ui.weather_2, self.ui.temp_2, self.ui.wind_2, self.ui.degree_2],
            'time_2': [self.ui.time_3, self.ui.weather_3, self.ui.temp_3, self.ui.wind_3, self.ui.degree_3],
            'time_3': [self.ui.time_4, self.ui.weather_4, self.ui.temp_4, self.ui.wind_4, self.ui.degree_4],
            'time_4': [self.ui.time_5, self.ui.weather_5, self.ui.temp_5, self.ui.wind_5, self.ui.degree_5],
            'time_5': [self.ui.time_6, self.ui.weather_6, self.ui.temp_6, self.ui.wind_6, self.ui.degree_6],
            'time_6': [self.ui.time_7, self.ui.weather_7, self.ui.temp_7, self.ui.wind_7, self.ui.degree_7],
            'time_7': [self.ui.time_8, self.ui.weather_8, self.ui.temp_8, self.ui.wind_8, self.ui.degree_8],
        }
        for k in range(8):
            t = 'time_' + str(k)
            time_wea[t][0].setText(cur[t]['time'])
            time_wea[t][1].setText(cur[t]['weather'])
            time_wea[t][2].setText(cur[t]['temperature'])
            time_wea[t][3].setText(cur[t]['wind_dir'])
            time_wea[t][4].setText(cur[t]['wind_degree'])

    def draw_future_weather(self):
        with open(file_path + 'future_weather.json', 'r', encoding='utf-8') as f:
            cur = json.load(f)
        day_wea = {
            'day_0': [self.ui.day_time_1, self.ui.day_weather_1, self.ui.day_temp_1, self.ui.day_daywind_1, self.ui.day_nightwind_1, self.ui.day_degree_1],
            'day_1': [self.ui.day_time_2, self.ui.day_weather_2, self.ui.day_temp_2, self.ui.day_daywind_2, self.ui.day_nightwind_2, self.ui.day_degree_2],
            'day_2': [self.ui.day_time_3, self.ui.day_weather_3, self.ui.day_temp_3, self.ui.day_daywind_3, self.ui.day_nightwind_3, self.ui.day_degree_3],
            'day_3': [self.ui.day_time_4, self.ui.day_weather_4, self.ui.day_temp_4, self.ui.day_daywind_4, self.ui.day_nightwind_4, self.ui.day_degree_4],
            'day_4': [self.ui.day_time_5, self.ui.day_weather_5, self.ui.day_temp_5, self.ui.day_daywind_5, self.ui.day_nightwind_5, self.ui.day_degree_5],
            'day_5': [self.ui.day_time_6, self.ui.day_weather_6, self.ui.day_temp_6, self.ui.day_daywind_6, self.ui.day_nightwind_6, self.ui.day_degree_6],
            'day_6': [self.ui.day_time_7, self.ui.day_weather_7, self.ui.day_temp_7, self.ui.day_daywind_7, self.ui.day_nightwind_7, self.ui.day_degree_7],
        }
        for k in range(7):
            t = 'day_' + str(k)
            day_wea[t][0].setText(cur[t]['day'])
            day_wea[t][1].setText(cur[t]['weather'])
            day_wea[t][2].setText(cur[t]['temperature'])
            day_wea[t][3].setText(cur[t]['day_wind'])
            day_wea[t][4].setText(cur[t]['night_wind'])
            day_wea[t][5].setText(cur[t]['wind_degree'])

app = QApplication(sys.argv)
fore = Forecast()
fore.show()
sys.exit(app.exec())

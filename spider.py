'''
Author: your name
Date: 2021-09-08 12:46:36
LastEditTime: 2021-09-09 14:28:48
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \dbpolicye:\Codes\C++\weather_forecast\spider.py
'''
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from bs4 import BeautifulSoup as bs
import requests
import json
import re
import threading
import socket
import sys

file_path = './json_data/'

def get_current_weather(url, headers):
    response = requests.get(url, headers=headers)
    soup = response.content.decode('utf-8')
    soup = bs(soup, 'lxml')

    cur_situation = dict()

    situation = soup.find("input", {"type": "hidden", "id": "hidden_title"})["value"]
    situation = situation.split(' ')
    situation = list(filter(None, situation))
    cur_situation = {'day': situation[1], 'weather': situation[2], 'temperature': situation[3]}

    situation = soup.find("input", {"type": "hidden", "id": "update_time"})["value"]
    cur_situation['update_time'] = situation

    situation = soup.find("p", {"class": "sun sunUp"}).find("span").text
    cur_situation['sunrise_time'] = situation[-5:]
    situation = soup.find("p", {"class": "sun sunDown"}).find("span").text
    cur_situation['sunfall_time'] = situation[-5:]

    with open(file_path + 'current_weather.json', 'w', encoding='utf-8') as f:
        json.dump(cur_situation, f, ensure_ascii=False)

    time_situation = dict()
    situation = soup.find_all("script")[2].string
    situation = re.findall(r"[[](.*?)[]]", str(situation))[0].split('\",')
    for k, sit in enumerate(situation[:8]):
        sit = sit.replace('\"', '').split(',')
        time_sit = {'time': sit[0], 'weather': sit[2], 'temperature': sit[3],
                    'wind_dir': sit[4], 'wind_degree': sit[5]}
        time_situation['time_' + str(k)] = time_sit
        
    with open(file_path + 'time_weather.json', 'w', encoding='utf-8') as f:
        json.dump(time_situation, f, ensure_ascii=False)

def get_future_weather(url, headers):
    response = requests.get(url, headers=headers)
    soup = response.content.decode('utf-8')
    soup = bs(soup, 'lxml')

    fut_situation = dict()

    situations = soup.find_all('li', {'class': re.compile("sky skyid lv[0-9]")})
    for k, situation in enumerate(situations):
        day = situation.find('h1').text 
        weather = situation.find('p', {'class': 'wea'}).text
        temperature = situation.find('span').text + '/' + situation.find('i').text 
        wind = situation.find_all('span', {'class': re.compile("[A-Z]*")})
        day_wind = wind[0]['title']
        night_wind = wind[1]['title']
        wind_degree = situation.find_all('i')[-1].text
        fut_situation['day_' + str(k)] = {
            'day': day, 'weather': weather, 'temperature': temperature,
            'day_wind': day_wind, 'night_wind': night_wind, 'wind_degree': wind_degree
        }
        
    with open(file_path + 'future_weather.json', 'w', encoding='utf-8') as f:
        json.dump(fut_situation, f, ensure_ascii=False)

class Spider(object):
    def __init__(self):
        self.headers = {"User-Agent": 
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }
        self.original_current_url = "http://www.weather.com.cn/weather1d/%s.shtml"
        self.original_future_url = "http://www.weather.com.cn/weather/%s.shtml" # 7 days
        self.load_city_code()

    def load_city_code(self):
        with open(file_path + "city_code.json", 'r', encoding='utf-8') as f:
            self.city_code = json.load(f)
    
    def create_url(self, city):
        code = str()
        for district in ['', '县', '市', '区', '州', '村', '省', '乡']:
            code = self.city_code.get(city + district)
            if code is not None:
                break
        
        if code is None:
            print('no such city')
            return False, False

        city_current_url = self.original_current_url % code
        city_future_url = self.original_future_url % code
        return (city_current_url, city_future_url)
    
    def sparse(self, city):
        if city == '':
            return
        cur_url, fut_url = self.create_url(city)
        if cur_url == False:
            return False
        t1 = threading.Thread(target=get_current_weather, args=(cur_url, self.headers))
        t2 = threading.Thread(target=get_future_weather, args=(fut_url, self.headers))
        t1.start()
        t2.start()
        print('Done.')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 21:35:47 2017

@author: weiqiang
"""

import json  
from urllib import request  
def weather_work(cityName):  
    cityName = str(cityName.encode('utf-8')).replace('''''\\x''','%')[2:].upper()  
    cityName = cityName[:len(cityName)-1]  
    with request.urlopen('http://api.map.baidu.com/telematics/v3/weather?location='+cityName+'&output=json&ak=nzOZroYb0jPL9G4541HVUxmS') as f:  
        data = f.read()  
        data_json = json.loads(data.decode('utf-8'))  
        if data_json['error']!=0:  
            print ('检查城市输入是否有误')  
            return  
        print (data_json['results'][0]['currentCity']+"'s weather:")  
        print (data_json['date']+"的数据"+'\n')  
        for t in data_json['results'][0]['weather_data']:  
            print (t['date']+'\n'+t['temperature']+'\n'+t['weather']+'\n'+t['wind']+'\n')  
while True:  
    cityName = input('输入城市名称（q结束）：')  
    if cityName=='q':  
        break  
    weather_work(cityName) 
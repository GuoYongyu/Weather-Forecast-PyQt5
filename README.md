# 利用PyQt5设计一个简单的天气预报查询系统

## 环境

python版本：python 3.6

第三方库：PyQt5，pygame，requests，bs4

系统：Windows10 64位

## 功能

- 启动时默认查询北京的天气
- 根据输入查询所输入地区的天气
- 可以显示当前天气，未来24小时天气，未来7天天气

## 设计思路

- 利用requests和bs4爬取并解析中国天气网的天气数据
- 利用Qt Designer绘制UI
- 将爬取到的数据解析后在UI中对应的对象里予以呈现

## 注意事项

- 将绘制的.ui文件转为.py文件指令：pyuic5 -o \*\*\*.py \*\*\*.ui

  \*\*\*即文件名，.py和.ui的文件名可以不同

- 由于需要添加图片，需要创建并使用.qrc文件，将其转为.py的指令为：pyrcc5 -o \*\*\*.py \*\*\*.qrc

  \*\*\*即文件名，.py和.qrc的文件名可以不同

  若使用.qrc文件，则必须先转为.py文件，否则.ui生成的.py文件会报错import resource_rc失败
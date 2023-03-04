#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
读取配置。这里配置文件用的yaml，也可用其他如XML,INI等，需在file_reader中添加相应的Reader进行处理。
"""
import os

# 通过当前文件的绝对路径，其父级目录一定是框架的base目录，然后确定各层的绝对路径。如果你的结构不同，可自行修改。

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
SCRCPY_FILE = os.path.join(BASE_PATH,'scrcpy')
ALLURE_FILE = os.path.join(BASE_PATH,'allure-2.17.3','bin','allure')

#项目路径
PROJECT_FILE = os.path.join(BASE_PATH,'config','Project.py')

#yamlStep目录
FEATURES_YAML = os.path.join(BASE_PATH,'featuresYaml')

LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')
HTMLREPORT_PATH = os.path.join(BASE_PATH, 'htmlReport')
SCREENSHOTS_PATH = os.path.join(BASE_PATH,"screenshots",'')
VIDEO_PATH = os.path.join(BASE_PATH, 'video')
FEATURES_FILE = os.path.join(BASE_PATH,'features')
DOWNLOAD_FILE = os.path.join(BASE_PATH,'downloadFile')
UPLOAD_FILE = os.path.join(BASE_PATH,'uploadFile')

CHROME_USER_DATA = os.path.join(BASE_PATH,'ChromeUserData')
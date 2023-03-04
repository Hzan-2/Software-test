import json
import time

from common.getPath import get_app_parameter_yaml_path
from common.globalVar import gloVar
from common.logger import logger
from config.Project import ISYAML, PROJECT
from core.Appium_operation import BasePage
from selenium.webdriver.common.by import By

from utils.file_read import YamlReader


class liviPage(BasePage):

    #选择环境
    def Science(self,Science,platformName,version=None):
        if str(platformName).lower() == 'android':
            if version is None:
                setting_switch = (By.XPATH,'//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.ScrollView[1]/android.widget.LinearLayout[1]/android.widget.Button[1]')
                logger.info('选择自动化环境%s'%Science)
                if Science == 'SIT2':
                    self.KEYCODE_BACK()
                else:
                    self.click(setting_switch)
                    setting_select = (By.XPATH,'//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.ScrollView[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.TextView[2]')
                    self.click(setting_select)
                    for i in range(1,9):
                        science_name = (By.XPATH,'//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.TextView['+str(i)+']')
                        if Science in self.get_text(science_name):
                            self.click(science_name)
                            self.offScienceVerify()
                            self.KEYCODE_BACK()
                            self.KEYCODE_BACK()
                            break
                        else:continue
            else:
                if self.elementExist((By.XPATH,'//*[contains(@content-desc, "取消")]')):
                    self.click((By.XPATH,'//*[contains(@content-desc, "取消")]'))
                elif  self.elementExist((By.XPATH,'//*[contains(@content-desc, "Cancel")]')):
                    self.click((By.XPATH,'//*[contains(@content-desc, "Cancel")]'))
                menuElement = (By.XPATH,'//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.widget.ImageView[3]')
                self.click(menuElement)
                time.sleep(3)
                versionCoordinate = self.findTextOperation('find_text','version','查找version版本元素坐标')
                self.clickOperation('click','None',versionCoordinate,'点击version版本元素坐标')
                self.Science(Science,platformName)
                return liviPage()
        else:
            if Science != 'UAT2':
                self.click((By.XPATH, "//*[contains(@name, '网络环境选择')]"))
                environment_dict = {"dev": "DEV", "sit2": "SIT_2", "uat1": "UAT_1", "uat2": "UAT_2", "uat3": "UAT_3","uat4": "UAT_4", "release": "RELEASE"}
                self.click((By.XPATH, "//*[contains(@name, '" + environment_dict[str(Science).lower()] + "')]"))
                self.click((By.XPATH,"//*[contains(@name, '开 启')]"))
            else:
                self.click((By.XPATH, "//*[contains(@name, '开 启')]"))

    #关闭环境校验跳转为测试中
    def offScienceVerify(self):
        for i in range(1,9):
            Verify_list_element = (By.XPATH,'//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.ScrollView[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout['+str(i)+']/android.widget.Switch[1]')
            if self.elementExist(Verify_list_element) and '测试中' in self.get_text(Verify_list_element) :
                continue
            elif self.elementExist(Verify_list_element) is False:
                break
            else:self.click(Verify_list_element)

    #初始化APP
    def initializationApp(self,num):
        logger.info('点击通过访问权限按钮！')
        for i in range(num):
            self.KEYCODE(20)
            self.KEYCODE(20)
            self.KEYCODE(20)
            self.KEYCODE(20)
            self.KEYCODE_ENTER()
        if num != 1:
            self.KEYCODE_BACK()
            logger.info('点击Login，进入登录界面')

    #判断登陆页面语言
    def judgeLanguage(self,element,platformName):
        if str(platformName).lower() == 'android':
            try:
                text = self.get_content_desc_text((By.XPATH, element))
                if '登录' in text:
                    return 'SimplifiedChinese'
                elif '登入' in text:
                    return 'TraditionalChinese'
                else:
                    return 'English'
            except IOError:
                logger.error('获取首页语言失败！')
        else:
            try:
                text = self.get_element_attribute((By.XPATH, element),'name')
                if '登录' in text:
                    return 'SimplifiedChinese'
                elif '登入' in text:
                    return 'TraditionalChinese'
                else:
                    return 'English'
            except IOError:
                logger.error('获取首页语言失败！')


    #处理点击操作
    def clickOperation(self,action,element,testData,fileName):
        try:
            if action == 'click':
                if '/' in element:
                    self.click((By.XPATH,element))
                elif element == 'None' and testData != 'None':
                    logger.info('检测到坐标元素，开始点击坐标！')
                    coordinates = str(testData).replace('，', ',').replace('[', '').replace(']', '').split(',')
                    self.click_coordinates(coordinates[0], coordinates[1])
                elif element == 'None' and testData == 'None':
                    logger.info('点击屏幕中心')
                    self.click_Screen_center()
                else:
                    logger.info('检测到坐标元素，开始点击坐标！')
                    coordinates = str(element).replace('，',',').replace('[','').replace(']','').split(',')
                    self.click_coordinates(coordinates[0],coordinates[1])
            elif 'click_' in action and testData != 'None':
                self.click_Dice((By.XPATH,element),int(testData),int(str(action).split('_')[1]))
            else:
                logger.error('点击操作有误！请检查！')
        except IOError:
            self.get_screent_img(fileName)
            logger.error('点击操作失败！已截图！请查看截图')

    #处理输入操作
    def inputOperation(self,action,element,testData,fileName):
        try:
            if action == 'input' and testData is not None:
                self.send_key((By.XPATH,element),testData)
            else:
                logger.error('输入操作有误或输入数据为空！请检查！')
        except IOError:
            self.get_screent_img(fileName)
            logger.error('输入操作失败！已截图！请查看截图')

    #处理获取操作
    def getOperation(self,action,element,testData,fileName):
        if action == 'get' and testData is not None:
            text = ''
            name_text = ''
            content_desc_text = ''
            #判断是否是含name属性的element，查找该属性的文本
            if '@name' in element:
                name_text = self.get_element_attribute((By.XPATH,element),'name')
            #判断是否是含content-desc属性的element，查找该属性的文本
            elif '@content-desc' in element:
                content_desc_text = self.get_content_desc_text((By.XPATH, element))
            #判断是否是含text属性的element，查找该属性的文本
            elif '@text' in element:
                text = self.get_text((By.XPATH, element))
            #不是以上几种则是绝对路径的xpath，查找该元素的文本
            else:
                parameter = YamlReader(get_app_parameter_yaml_path(ISYAML,PROJECT)).data[0]
                platformName = parameter["desired_caps"]["platformName"]
                if str(platformName).lower() == 'ios':
                    if self.get_element_attribute((By.XPATH,element),'name') != "" and self.get_element_attribute((By.XPATH,element),'name') != None :
                        name_text = self.get_element_attribute((By.XPATH, element), 'name')
                    elif self.get_text((By.XPATH, element)) != "" and self.get_text((By.XPATH, element)) != None:
                        text = self.get_text((By.XPATH, element))
                    else:
                        return False
                else:
                    if self.get_content_desc_text((By.XPATH, element)) != "" and self.get_content_desc_text((By.XPATH, element)) != None:
                        content_desc_text = self.get_content_desc_text((By.XPATH, element))
                    elif self.get_text((By.XPATH, element)) != "" and self.get_text((By.XPATH, element)) != None:
                        text = self.get_text((By.XPATH, element))
                    else:
                        return False
            #判断传参是否是一个list，判断元素文本是否在list里面，或者元素包含list的内容
            if '[' in str(testData) and ']' in str(testData):
                if str(text) != "":
                    if str(text) in str(testData):
                        logger.info('获取到的text信息为：“{}”,在testData：“{}”列表里！'.format(text, testData))
                        return True
                    elif str(testData).replace('[', '').replace(']', '').replace("'", "").replace(" ","") in str(text).replace(" ",""):
                        logger.info('获取到的text信息为：“{}”,text文本包含testData：“{}”！'.format(text, str(testData).replace('[','').replace(']', '').replace("'", "")))
                        return True
                    else:
                        logger.error('获取到的text信息为：“{}”,不在testData：“{}”列表里！'.format(text, testData))
                        self.get_screent_img(fileName)
                        return False
                elif str(name_text) != "":
                    if str(name_text) in str(testData):
                        logger.info('获取到的name文本信息为：“{}”,在testData：“{}”列表里！'.format(name_text, testData))
                        return True
                    elif str(testData).replace('[', '').replace(']', '').replace("'", "").replace(" ","") in str(name_text).replace(" ",""):
                        logger.info('获取到的name信息为：“{}”,元素name文本包含testData：“{}”！'.format(name_text,str(testData).replace('[','').replace(']', '').replace("'", "")))
                        return True
                    else:
                        logger.error('获取到的name文本信息为：“{}”,不在testData：“{}”列表里！'.format(name_text, testData))
                        self.get_screent_img(fileName)
                        return False
                else:
                    if str(content_desc_text) in str(testData):
                        logger.info('获取到的content_desc信息为：“{}”,在testData：“{}”列表里！'.format(content_desc_text, testData))
                        return True
                    elif str(testData).replace('[', '').replace(']', '').replace("'", "").replace(" ","") in str(content_desc_text).replace(" ",""):
                        logger.info('获取到的content_desc信息为：“{}”,content_desc文本包含testData：“{}”！'.format(content_desc_text,str(testData).replace('[','').replace(']', '').replace("'","")))
                        return True
                    else:
                        logger.info('获取到的content_desc信息为：“{}”,不在testData：“{}”列表里！'.format(content_desc_text, testData))
                        self.get_screent_img(fileName)
                        return False
            #传参是一个变量值，需要赋值给对象
            elif "$$" in str(testData) and "{" in str(testData) and "}" in str(testData):
                if text != "":
                    logger.info('获取到{}变量值，给该变量值赋值为：{}'.format(testData,text))
                    return text
                elif name_text != "":
                    logger.info('获取到{}变量值，给该变量值赋值为：{}'.format(testData, name_text))
                    return name_text
                else:
                    logger.info('获取到{}变量值，给该变量值赋值为：{}'.format(testData, content_desc_text))
                    return content_desc_text
            #传参非list，判断传参跟元素获取的文本做比对，看断言是否对等
            else:
                if text != "":
                    if str(text) == str(testData):
                        logger.info('获取到的text信息为：“{}”,与testData：“{}”一致！'.format(text, testData))
                        return True
                    else:
                        logger.error('获取到的text信息为：“{}”,与testData：“{}”不一致！'.format(text, testData))
                        self.get_screent_img(fileName)
                        return False
                elif content_desc_text != "":
                    if str(content_desc_text) == str(testData):
                        logger.info('获取到的content_desc信息为：“{}”,与testData：“{}”一致！'.format(content_desc_text, testData))
                        return True
                    else:
                        logger.info('获取到的content_desc信息为：“{}”,与testData：“{}”不一致！'.format(content_desc_text, testData))
                        self.get_screent_img(fileName)
                        return False
                elif name_text != "":
                    if str(name_text) == str(testData):
                        logger.info('获取到的name文本信息为：“{}”,与testData：“{}”一致！'.format(name_text, testData))
                        return True
                    else:
                        logger.error('获取到的name文本信息为：“{}”,与testData：“{}”不一致！'.format(name_text, testData))
                        self.get_screent_img(fileName)
                        return False
        else:
            raise Exception('获取/赋值操作有误或比对数据为空！请检查！')

    #处理滑动操作
    def slideOperation(self,action,element,testData,fileName):
        try:
            if action == 'slide':
                if element == 'up':
                    if testData != "None":
                        self.swipe_up(x=int(testData))
                    else:
                        self.swipe_up()
                elif element == 'down':
                    if testData != "None":
                        self.swipe_down(x=int(testData))
                    else:
                        self.swipe_down()
                elif element == 'left':
                    if testData != "None":
                        self.swipe_left(y=int(testData))
                    else:
                        self.swipe_left()
                elif element == 'right':
                    if testData != "None":
                        self.swipe_right(y=int(testData))
                    else:
                        self.swipe_right()
                elif element == 'bottom':
                    self.scoll2bottom()
                elif element == 'top':
                    self.scoll2top()
                else:
                    raise Exception('输入滑动操作错误，没有“{}”这个操作！'.format(element))
            elif 'slide_seekBar' in action :
                if '//' in element:
                    logger.info('检测到滑块元素，开始将滑块切成：{}块，滑动滑块到位置：{}'.format(str(action).split('_')[2],testData))
                    self.swipe_SeekBar((By.XPATH,element),int(testData),int(str(action).split('_')[2]))
                else:
                    logger.info('检测到滑块元素为坐标：{}，开始将滑块切成：{}块，滑动滑块到位置：{}'.format(element,str(action).split('_')[2], testData))
                    self.swipe_SeekBar(element, int(testData), int(str(action).split('_')[2]))
            elif 'slide_custom' in action:
                if '->' in testData:
                    coordinate = str(testData).split('->')
                    coordinate1 = coordinate[0].strip(' ').strip('[').strip(']').split(',')
                    coordinate2 = coordinate[1].strip(' ').strip('[').strip(']').split(',')
                    self.swipe_custom(coordinate1[0],coordinate1[1],coordinate2[0],coordinate2[1])
                else:
                    raise Exception('输入自定义滑动数据{}有误！请检查！'.format(testData))
            elif action == 'slide_space':
                if element == 'up':
                    if testData != "None":
                        self.swipe_up(distance=testData)
                    else:
                        self.swipe_up()
                elif element == 'down':
                    if testData != "None":
                        self.swipe_down(distance=testData)
                    else:
                        self.swipe_down()
                elif element == 'left':
                    if testData != "None":
                        self.swipe_left(distance=testData)
                    else:
                        self.swipe_left()
                elif element == 'right':
                    if testData != "None":
                        self.swipe_right(distance=testData)
                    else:
                        self.swipe_right()
                elif element == 'bottom':
                    self.scoll2bottom()
                else:
                    raise Exception('输入滑动操作错误，没有“{}”这个操作！'.format(element))
            else:
                logger.error('输入滑动操作有误！请检查！')
        except IOError:
            self.get_screent_img(fileName)
            logger.error('输入操作失败！已截图！请查看截图')

    #判断操作
    def judgeOperation(self,action,element,fileName):
        try:
            if action == 'judge':
                if self.elementExist((By.XPATH,element)):
                    return True
                else:
                    return False
            else:
                logger.error('判断操作有误！请检查！')
        except IOError:
            self.get_screent_img(fileName)
            logger.error('判断操作失败！已截图！请查看截图')

    #返回元素属性
    def attributeOperation(self,action,element,index,fileName):
        try:
            if action == 'attribute':
                if self.get_element_attribute((By.XPATH,element),index) == 'true':
                    return True
                else:
                    return False
            else:
                logger.error('获取元素属性操作有误！请检查！')
        except IOError:
            self.get_screent_img(fileName)
            logger.error('获取元素属性操作失败！已截图！请查看截图')

    #比较元素数值大小操作
    def compareOperation(self,action,num1,symbol,num2,fileName):
        try:
            if action == 'compare':
                try:
                    if symbol == '>':
                        if round(float(num1),2) > round(float(num2),2):
                            logger.info('比对字符为{}，左边数据为{}，右边数据为{}，结果为{}，走if分支'.format('>',round(float(num1),2),round(float(num2),2),round(float(num1),2) > round(float(num2),2)))
                        else:
                            logger.info('比对字符为{}，左边数据为{}，右边数据为{}，结果为{}，走else分支'.format('>',round(float(num1),2),round(float(num2),2),round(float(num1),2) > round(float(num2),2)))
                        return round(float(num1),2) > round(float(num2),2)
                    elif symbol == '<':
                        if round(float(num1),2) < round(float(num2),2):
                            logger.info('比对字符为{}，左边数据为{}，右边数据为{}，结果为{}，走if分支'.format('<',round(float(num1),2),round(float(num2),2),round(float(num1),2) < round(float(num2),2)))
                        else:
                            logger.info('比对字符为{}，左边数据为{}，右边数据为{}，结果为{}，走else分支'.format('<',round(float(num1),2),round(float(num2),2),round(float(num1),2) < round(float(num2),2)))
                        return round(float(num1),2) < round(float(num2),2)
                    elif symbol == '>=' or symbol == '=>':
                        if round(float(num1),2) >= round(float(num2),2):
                            logger.info('比对字符为{}，左边数据为{}，右边数据为{}，结果为{}，走if分支'.format('>=',round(float(num1),2),round(float(num2),2),round(float(num1),2) >= round(float(num2),2)))
                        else:
                            logger.info('比对字符为{}，左边数据为{}，右边数据为{}，结果为{}，走else分支'.format('>=',round(float(num1),2),round(float(num2),2),round(float(num1),2) >= round(float(num2),2)))
                        return round(float(num1),2) >= round(float(num2),2)
                    elif symbol == '<=' or symbol == '=<':
                        if round(float(num1),2) <= round(float(num2),2):
                            logger.info('比对字符为{}，左边数据为{}，右边数据为{}，结果为{}，走if分支'.format('<=',round(float(num1),2),round(float(num2),2),round(float(num1),2) <= round(float(num2),2)))
                        else:
                            logger.info('比对字符为{}，左边数据为{}，右边数据为{}，结果为{}，走else分支'.format('<=',round(float(num1),2),round(float(num2),2),round(float(num1),2) <= round(float(num2),2)))
                        return round(float(num1),2) <= round(float(num2),2)
                    elif symbol == '==':
                        if str(num1) == str(num2):
                            logger.info('比对字符为{}，左边字符串为{}，右边字符串为{}，结果为{}，走if分支'.format('==',num1,num2,True))
                            return True
                        else:
                            logger.info('比对字符为{}，左边字符串为{}，右边字符串为{}，结果为{}，走else分支'.format('==',num1,num2,False))
                            return False
                    else:
                        if round(float(num1),2) == round(float(num2),2):
                            logger.info('比对字符为{}，左边数据为{}，右边数据为{}，结果为{}，走if分支'.format('=',round(float(num1),2),round(float(num2),2),round(float(num1),2) == round(float(num2),2)))
                        else:
                            logger.info('比对字符为{}，左边数据为{}，右边数据为{}，结果为{}，走else分支'.format('=',round(float(num1),2),round(float(num2),2),round(float(num1),2) == round(float(num2),2)))
                        return round(float(num1), 2) == round(float(num2), 2)
                except IOError:
                    self.get_screent_img(fileName)
                    logger.error('数据对比出错，传参num1为{}，对比符号symbol为{}，传参num2为{}！已截图！请查看截图'.format(num1,symbol,num2))
        except IOError:
            self.get_screent_img(fileName)
            logger.error('比较元素数值大小操作失败！已截图！请查看截图')

    #返回元素所在页
    def backElementPageOperation(self,action,element,fileName):
        try:
            if action == 'backElement':
                while True:
                    if self.elementExist((By.XPATH,element)):
                        break
                    else:
                        self.KEYCODE_BACK()
            elif action == 'backHome':
                while True:
                    '''
                    1.判断是否找到首页问候语，如果找到则已经返回到首页，跳出循环
                    2.发现还未返回首页，但发现底下按钮的元素出现，则说明模块不在首页，点击进入首页，跳出循环
                    '''
                    if self.elementExist((By.XPATH,element[0])) and self.elementExist((By.XPATH,element[1])):
                        ontent_desc_text = self.get_content_desc_text((By.XPATH, element[0]))
                        if ontent_desc_text in ['早晨', '早上好', 'Good Morning', '午安', '下午好', 'Good Afternoon', '晚安', '晚上好','Good Evening', '歡迎回來', '欢迎回来', 'Welcome Back']:
                            break
                        else:
                            self.click((By.XPATH,element[1]))
                            break
                    else:
                        self.KEYCODE_BACK()
            else:
                logger.error('返回元素操作有误！请检查！')
        except IOError:
            self.get_screent_img(fileName)
            logger.error('返回元素操作失败！已截图！请查看截图')

    #流动保安编码操作
    def sotfTokenOperation(self,action,testData,fileName,platformName):
        try:
            if action == 'sotfToken_input':
                logger.info('输入流动保安编码:{}'.format(testData))
                if str(platformName).lower() == 'android':
                    for i in str(testData):
                        self.click((By.XPATH,'//*[contains(@content-desc, "'+str(i)+'")]'))
                else:
                    for i in str(testData):
                        self.click((By.XPATH,'//*[contains(@name, "'+str(i)+'")]'))
            else:
                logger.error('流动保安编码操作有误！请检查！')
        except IOError:
            self.get_screent_img(fileName)
            logger.error('流动保安编码操作失败！已截图！请查看截图')

    #等待操作
    def sleepOperation(self,action,testData,fileName):
        try:
            if action == 'sleep':
                time.sleep(int(testData))
            else:
                logger.error('停顿操作有误！请检查！')
        except IOError:
            self.get_screent_img(fileName)
            logger.error('停顿操作失败！已截图！请查看截图')

    #找文本坐标操作
    def findTextOperation(self,action,testData,fileName):
        try:
            if action == 'find_text':
                qualified_coordinates = self.find_text_in_the_picture_of_OCR(testData)
                if qualified_coordinates != []:
                    logger.info("获取到‘{}’的文本坐标为：{}".format(testData,qualified_coordinates[0]))
                    return qualified_coordinates[0]
                else:
                    return 'None'
            elif 'find_text_' in action:
                qualified_coordinates = self.find_text_in_the_picture_of_OCR(testData)
                if qualified_coordinates != []:
                    logger.info("获取到‘{}’的文本坐标列表为：{},获取第{}个坐标为：{}".format(testData,qualified_coordinates,action.split('_')[2],qualified_coordinates[int(action.split('_')[2])-1]))
                    return qualified_coordinates[int(action.split('_')[2])-1]
                else:
                    return 'None'
        except IOError:
            self.get_screent_img(fileName)
            logger.error('找文本操作失败！已截图！请查看截图')

    #启动app操作
    def startAppOperation(self,action,testData,fileName):
        try:
            if action == 'start_app':
                if 'str' in str(type(testData)):
                    testData = json.loads(testData.replace('"', '').replace("'", '"'))
                    logger.info(testData)
                self.startApp(testData['appPackage'],testData['appActivity'])
                logger.info('已启动包名为{}的app'.format(testData['appPackage']))
            else:
                logger.error('启动新的app操作有误！请检查！')
        except IOError:
            self.get_screent_img(fileName)
            logger.error('启动新的app操作有误！已截图！请查看截图')

    #切换app操作
    def switchAppOperation(self,action,testData,fileName):
        try:
            if action == 'switch_app':
                self.switchApp(testData)
                logger.info('已切换至包名为{}的app'.format(testData))
            else:
                logger.error('切换app操作有误！请检查！')
        except IOError:
            self.get_screent_img(fileName)
            logger.error('切换app操作有误！已截图！请查看截图')

    #键盘操作
    def keyboardOperation(self,action,testData,remarks,platformName):
        if str(platformName).lower() == 'android':
            try:
                if action == 'keyboard':
                    if testData == 'Enter':
                        self.KEYCODE_ENTER()
                    elif testData == 'back':
                        self.KEYCODE_BACK()
                    else:
                        for i in str(testData):
                            if i == "0":
                                self.KEYCODE(7)
                            elif i == "1":
                                self.KEYCODE(8)
                            elif i == "2":
                                self.KEYCODE(9)
                            elif i == "3":
                                self.KEYCODE(10)
                            elif i == "4":
                                self.KEYCODE(11)
                            elif i == "5":
                                self.KEYCODE(12)
                            elif i == "6":
                                self.KEYCODE(13)
                            elif i == "7":
                                self.KEYCODE(14)
                            elif i == "8":
                                self.KEYCODE(15)
                            elif i == "9":
                                self.KEYCODE(16)
                            elif i == "A" or i == "a":
                                self.KEYCODE(29)
                            elif i == "B" or i == "b":
                                self.KEYCODE(30)
                            elif i == "C" or i == "c":
                                self.KEYCODE(31)
                            elif i == "D" or i == "d":
                                self.KEYCODE(32)
                            elif i == "E" or i == "e":
                                self.KEYCODE(33)
                            elif i == "F" or i == "f":
                                self.KEYCODE(34)
                            elif i == "G" or i == "g":
                                self.KEYCODE(35)
                            elif i == "H" or i == "h":
                                self.KEYCODE(36)
                            elif i == "I" or i == "i":
                                self.KEYCODE(37)
                            elif i == "J" or i == "j":
                                self.KEYCODE(38)
                            elif i == "K" or i == "k":
                                self.KEYCODE(39)
                            elif i == "L" or i == "l":
                                self.KEYCODE(40)
                            elif i == "M" or i == "m":
                                self.KEYCODE(41)
                            elif i == "N" or i == "n":
                                self.KEYCODE(42)
                            elif i == "O" or i == "o":
                                self.KEYCODE(43)
                            elif i == "P" or i == "p":
                                self.KEYCODE(44)
                            elif i == "Q" or i == "q":
                                self.KEYCODE(45)
                            elif i == "R" or i == "r":
                                self.KEYCODE(46)
                            elif i == "S" or i == "s":
                                self.KEYCODE(47)
                            elif i == "T" or i == "t":
                                self.KEYCODE(48)
                            elif i == "U" or i == "u":
                                self.KEYCODE(49)
                            elif i == "V" or i == "v":
                                self.KEYCODE(50)
                            elif i == "W" or i == "w":
                                self.KEYCODE(51)
                            elif i == "S" or i == "s":
                                self.KEYCODE(52)
                            elif i == "Y" or i == "y":
                                self.KEYCODE(53)
                            elif i == "Z" or i == "z":
                                self.KEYCODE(54)
                elif testData == 'recovery':
                    self.KEYCODE_RECOVERY()
                else:
                    logger.error('键盘操作有误！请检查！')
                    raise
            except IOError:
                self.get_screent_img(remarks)
                logger.error('键盘操作失败！已截图！请查看截图')
        else:
            try:
                if action == 'keyboard':
                    if str(testData).isdigit():
                        for i in str(testData):
                            self.click((By.XPATH,'//XCUIElementTypeKey[@name='+i+']'))
                    elif testData == 'recovery':
                        self.KEYCODE_RECOVERY()
                    else:
                        logger.error('输入的文本非纯数字！')
                        raise Exception('输入的文本非纯数字！')
                else:
                    logger.error('键盘操作有误！请检查！')
                    raise
            except IOError:
                self.get_screent_img(remarks)
                logger.error('键盘操作失败！已截图！请查看截图')





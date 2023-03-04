import datetime
import os
import time

from selenium.webdriver.common.by import By

from common.getExcel import jugde_Excel_color, get_Excel_Text
from common.getVariable import get_time_stamp, time_formatting
from config.Config import DOWNLOAD_FILE
from core.browser_operation import Operates
from common.logger import logger
from main import delDownloadFile


class Page(Operates):

    #打开url操作
    def openUrlOperation(self,action,url,remarks):
        try:
            if action == 'open':
                self.get_url(url)
                logger.info('{}'.format(remarks))
            else:
                logger.info('点击操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('打开网页操作失败！已截图！请查看截图')

    #处理点击操作
    def clickOperation(self,action,element,testData,remarks):
        try:
            if action == 'click':
                self.click((By.XPATH,element),testData)
            elif action == 'double_click':
                self.double_click((By.XPATH,element))
            else:
                logger.info('点击操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('点击操作失败！已截图！请查看截图')

    #处理输入操作
    def inputOperation(self,action,element,testData,remarks):
        try:
            if action == 'input' and testData is not None:
                self.input_text((By.XPATH,element),testData)
            else:
                logger.info('输入操作有误或输入数据为空！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('输入操作失败！已截图！请查看截图')

    #处理获取操作
    def getOperation(self,action,element,testData,remarks):
        text = self.get_text((By.XPATH, element))
        if action == 'get' and "$$" not in str(testData):
            if str(text) == str(testData) and "[" not in str(text) and "]" not in str(text):
                logger.info('获取到元素文本为：{}，与testData的值{}相匹配，结果为True'.format(text,testData))
                return True
            elif "[" in str(text) and "]" in str(text):
                if str(text) in str(testData):
                    logger.info('获取到元素文本为：{}，在testData的列表：{}内，结果为True'.format(text, testData))
                    return True
                else:
                    logger.info('获取到元素文本为：{}，不在testData的列表：{}内，结果为False'.format(text, testData))
                    return False
            else:
                logger.info('获取到元素文本为：{}，与testData的值{}不匹配，结果为False'.format(text, testData))
                self.getImage(remarks)
                return False
        #非text文本元素，需要获取对应元素属性的值
        elif 'get_' in action and "$$" in str(testData) and "{" in str(testData) and "}" in str(testData):
            attribute = str(action).split('_')[1]
            attributeText = self.get_attribute((By.XPATH, element),attribute)
            if attributeText != "":
                logger.info('获取到{}属性的为值：{}，赋值给变量值{}'.format(attribute,attributeText,testData))
                return attributeText
            else:
                logger.info('获取不到元素{},{}属性的值！'.format(element,attribute))
                raise Exception('获取不到元素{},{}属性的值！'.format(element,attribute))
        #传参是一个变量值，需要赋值给对象
        elif action == 'get' and "$$" in str(testData) and "{" in str(testData) and "}" in str(testData):
            if text != "":
                logger.info('获取到text文本属性的为值：{}，赋值给变量值{}'.format(text,testData))
                return text
            else:
                logger.info('获取不到{}元素text值！'.format(element))
                raise Exception('获取不到{}元素text值！'.format(element))
        else:
            self.getImage(remarks)
            raise IOError('获取操作有误或比对数据为空！请检查！')

    #判断操作
    def judgeOperation(self,action,element,remarks):
        try:
            if action == 'judge':
                if self.elementExist((By.XPATH,element)):
                    return True
                else:
                    return False
            else:
                logger.info('判断操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('判断操作失败！已截图！请查看截图')

    #聚焦操作
    def focusOperation(self,action,element,remarks):
        try:
            if action == 'focus':
                self.Focus((By.XPATH,element))
            else:
                logger.info('聚焦操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('聚焦操作失败！已截图！请查看截图')

    #切入iframe操作
    def iframeOperation(self,action,element,remarks):
        try:
            if action == 'iframe':
                self.into_iframe((By.XPATH,element))
            else:
                logger.info('切入iframe操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('切入iframe操作失败！已截图！请查看截图')

    #切出iframe操作
    def q_iframeOperation(self,action,remarks):
        try:
            if action == 'q_iframe':
                self.q_iframe()
            else:
                logger.info('切出iframe操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('切出iframe操作失败！已截图！请查看截图')

    #停顿操作
    def sleepOperation(self,action,testData,remarks):
        try:
            if action == 'sleep':
                self.sleep(int(testData))
            else:
                logger.info('停顿操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('停顿操作失败！已截图！请查看截图')

    #操作键盘
    def keyboardOperation(self,action,element,testData,remarks):
        try:
            if action == 'keyboard':
                if testData == 'Enter':
                    if element != "None":
                        self.KEYCODE_ENTER((By.XPATH,element))
                    else:
                        self.PYKEYCODE_ENTER()
                elif testData == 'BackSpace':
                    self.KEYCODE_BACK_SPACE((By.XPATH,element))
                elif 'Ctrl+' in testData:
                    self.KEYCODE_CTRL_letter((By.XPATH, element),str(testData).split('+')[-1].lower())
                else:
                    self.KEYCODE(testData)
            else:
                logger.info('键盘操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('键盘操作失败！已截图！请查看截图')

    #切换窗口
    def switch_windowOperation(self,action,target_title,remarks):
        try:
            if action == 'window':
                self.switch_window(target_title)
            else:
                logger.info('切换window操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('切换window操作失败！已截图！请查看截图')

    #关闭窗口
    def close_windowOperation(self,action,remarks):
        try:
            if action == 'close':
                self.close()
            else:
                logger.info('关闭窗口操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('关闭窗口操作失败！已截图！请查看截图')

    #操作鼠标
    def mouseOperation(self,action,element,testData,remarks):
        try:
            if action == 'mouse':
                if testData == 'hover':
                    self.mouseHover((By.XPATH,element))
                elif testData == 'click':
                    self.mouseClick((By.XPATH,element))
                elif testData == 'right_click':
                    self.mouseRightClick((By.XPATH,element))
                elif testData == 'drag_and_drop':
                    elementList = str(element).split('->')
                    self.mouseDragAndDrop((By.XPATH,elementList[0]),(By.XPATH,elementList[1]))
            else:
                logger.info('鼠标操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('鼠标操作失败！已截图！请查看截图')

    #操作下拉框
    def dropDownBoxOperation(self,action,element,testData,remarks):
        try:
            if action == 'select':
                self.selectDropDownBox((By.XPATH,element),testData)
            else:
                logger.info('下拉框操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('下拉框操作失败！已截图！请查看截图')

    #关闭alert弹窗
    def popupOperation(self,action,remarks):
        try:
            if action == 'alert':
                self.closePopupAlert()
            else:
                logger.info('弹窗操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('弹窗操作失败！已截图！请查看截图')

    #执行js指令
    def jsOperation(self,action,testData,remarks):
        try:
            if action == 'js':
                self.by_js(testData)
            else:
                logger.info('js操作有误！请检查！')
        except IOError:
            self.getImage(remarks)
            logger.info('js操作失败！已截图！请查看截图')

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
                    elif symbol == '!=':
                        if str(num1) != str(num2):
                            logger.info('比对字符为{}，左边字符串为{}，右边字符串为{}，结果为{}，走if分支'.format('!=',num1,num2,True))
                            return True
                        else:
                            logger.info('比对字符为{}，左边字符串为{}，右边字符串为{}，结果为{}，走else分支'.format('!=',num1,num2,False))
                            return False
                    else:
                        if round(float(num1),2) == round(float(num2),2):
                            logger.info('比对字符为{}，左边数据为{}，右边数据为{}，结果为{}，走if分支'.format('=',round(float(num1),2),round(float(num2),2),round(float(num1),2) == round(float(num2),2)))
                        else:
                            logger.info('比对字符为{}，左边数据为{}，右边数据为{}，结果为{}，走else分支'.format('=',round(float(num1),2),round(float(num2),2),round(float(num1),2) == round(float(num2),2)))
                        return round(float(num1), 2) == round(float(num2), 2)
                except IOError:
                    self.getImage(fileName)
                    logger.error('数据对比出错，传参num1为{}，对比符号symbol为{}，传参num2为{}！已截图！请查看截图'.format(num1,symbol,num2))
        except IOError:
            self.getImage(fileName)
            logger.error('比较元素数值大小操作失败！已截图！请查看截图')

    #上传文件
    def uploadOperation(self,action,path,file,fileName):
        try:
            if action == 'upload':
                if path == 'None':
                    self.Upload(file)
                else:
                    self.Upload(file,path)
            else:
                logger.info('上传文件操作有误！请检查！')
        except IOError:
            self.getImage(fileName)
            logger.error('上传文件操作失败！已截图！请查看截图')

    #下载文件
    def downloadOperation(self,action,fileName):
        try:
            if action == 'download':
                delDownloadFile()
                self.Download()
            else:
                logger.info('下载文件操作有误！请检查！')
        except IOError:
            self.getImage(fileName)
            logger.error('下载文件操作失败！已截图！请查看截图')

    #操作日期
    def timeOperation(self,action,element,testData,fileName):
        if 'time' in action and 'get_' not in action:
            try:
                timeFormat = str(testData).split('->')[0]
                timeValue = str(testData).split('->')[1]
                timeValue = time_formatting(timeFormat,timeValue)
                newTime = datetime.datetime.utcfromtimestamp(int(time.mktime(time.strptime(timeValue, timeFormat)))+int(str(action).split('_')[1])*115300).strftime(timeFormat)
                logger.info('传入时间格式为：{},输入时间为{},需要将时间修改{}天,修改后时间为{},将新的时间赋值给{}变量！'.format(str(testData).split('->')[0],str(testData).split('->')[1],str(action).split('_')[1],newTime,str(element).replace('$','').replace('{','').replace('}','')))
                return newTime
            except IOError:
                self.getImage(fileName)
                logger.error('传入时间格式{}与提供的时间{}格式不匹配,或者输入的时间格式不正确，请检查！！！'.format(str(testData).split('->')[0],str(testData).split('->')[1]))
                logger.error('时间操作失败！已截图！请查看截图')
        #获取时间值
        elif 'get_time' in action and "$${" not in testData:
            try:
                testDataList = str(testData).split('_')
                logger.info('获取到时间为{}，赋值给变量{}'.format(get_time_stamp(testDataList[1],testDataList[0]),element))
                return get_time_stamp(testDataList[1],testDataList[0])
            except IOError:
                self.getImage(fileName)
                logger.error('获取时间失败，请检查testData参数{}！！！'.format(testData))
                logger.error('时间操作失败！已截图！请查看截图')
        else:
            logger.info('时间操作有误！请检查！')


    #文件操作
    def fileOperation(self,action,element,testData,fileName):
        try:
            if 'exists' in action:
                if element == 'None':
                    for file in os.listdir(DOWNLOAD_FILE):
                        if testData in file:
                            logger.info('downloadFile文件夹下存在文件{}，下载文件校验成功！'.format(file))
                            return True
                    logger.info('downloadFile文件夹下不存在文件{}，下载文件校验失败！'.format(testData))
                    return False
                else:
                    for file in os.listdir(element):
                        if testData in file:
                            logger.info('存在文件{}，下载文件校验成功！'.format(file))
                            return True
                    logger.info('不存在文件{}，下载文件校验失败！'.format(testData))
                    return False
            try:
                if 'excel_color' in action:
                    if '[' in element and ']' in element and len(str(action).split('_')) == 3:
                        coordinate = str(element).split(',')
                        rows = coordinate[0].replace(' ','').replace('[','')
                        column = coordinate[1].replace(' ','').replace(']','')
                        result = jugde_Excel_color(rows, column)
                        logger.info('Excel第{}行，第{}列，判断单元格底色为{}'.format(rows,column,result))
                        return jugde_Excel_color(rows,column)
                    else:
                        Sheet = str(action).split('_')[-1]
                        coordinate = str(element).split(',')
                        rows = coordinate[0].replace(' ','').replace('[','')
                        column = coordinate[1].replace(' ','').replace(']','')
                        result = jugde_Excel_color(rows,column,Sheet)
                        logger.info('Excel表单{},第{}行，第{}列，判断单元格底色为{}'.format(Sheet,rows, column, result))
                        return jugde_Excel_color(rows,column,Sheet)
            except IOError:
                self.getImage(fileName)
                logger.error('判断excel表格颜色操作失败！已截图！请查看截图')
            try:
                if 'excel_text' in action:
                    if '[' in element and ']' in element and len(str(action).split('_')) == 3:
                        coordinate = str(element).split(',')
                        rows = coordinate[0].replace(' ', '').replace('[', '')
                        column = coordinate[1].replace(' ', '').replace(']', '')
                        text = get_Excel_Text(rows,column)
                        if text == '':
                            text = None
                        logger.info('Excel第{}行，第{}列，获取文本为{}，与testData：{}比对，结果为：{}'.format(rows,column,text,testData,str(testData) == str(text)))
                        return str(testData) == str(text)
                    else:
                        Sheet = str(action).split('_')[-1]
                        coordinate = str(element).split(',')
                        rows = coordinate[0].replace(' ', '').replace('[', '')
                        column = coordinate[1].replace(' ', '').replace(']', '')
                        text = get_Excel_Text(rows, column,Sheet)
                        if text == '':
                            text = None
                        logger.info('Excel表单{},第{}行，第{}列，获取文本为{}，与testData：{}比对，结果为：{}'.format(Sheet,rows,column,text,testData,str(testData) == str(text)))
                        return str(testData) == str(text)
            except IOError:
                self.getImage(fileName)
                logger.error('判断excel表格颜色操作失败！已截图！请查看截图')
        except IOError:
            self.getImage(fileName)
            logger.error('文件操作失败！已截图！请查看截图')

    #获取验证码
    def captchaOperation(self,action, fileName):
        try:
            if 'captcha' in action:
                captcha = self.find_text_in_the_picture_of_OCR_get_Verification_Code()
                logger.info('获取到验证码为：{}'.format(captcha))
                if '登录' in captcha:
                    raise Exception('获取验证码失败')
                return captcha
        except IOError:
            self.getImage(fileName)
            logger.error('获取验证码操作失败！已截图！请查看截图')
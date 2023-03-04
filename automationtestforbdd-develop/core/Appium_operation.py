import logging
import operator
import re
import os
import signal

from paddleocr import PaddleOCR

from common.logger import logger
import time
from selenium.common.exceptions import * #导入所有的异常类
from selenium.webdriver.support.ui import WebDriverWait
from common.AppDriver import AppDriver
import subprocess
from config.Config import VIDEO_PATH, SCREENSHOTS_PATH, SCRCPY_FILE

from PIL import Image
import numpy
import cv2

from utils.AES import EncryptDecode


class BasePage(object):

    def __init__(self):
        self.driver = AppDriver().openApp()
        self.VIDEO_PATH = VIDEO_PATH
        self.SCREENSHOTS_PATH = SCREENSHOTS_PATH
        self.SCRCPY_FILE = SCRCPY_FILE

    def Start_recording_screen(self,filename):
        '''开始录制屏幕'''
        try:
            now = time.strftime("%Y-%m-%d_%H_%M_%S_")
            cmd = [self.SCRCPY_FILE+'/'+'scrcpy', '--record', self.VIDEO_PATH+'/'+filename+now+'.mkv']
            p = subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            return p
        except Exception:
            pass

    def Stop_recording_screen(self,p):
        '''停止录制屏幕'''
        try:
            logger.warning('正在保存录屏，请稍等！！！')
            time.sleep(10)
            os.kill(p.pid,signal.SIGTERM)
        except Exception:
            pass


    def find_element(self, *loc):
        try:
            # 元素可见时，返回查找到的元素；以下入参为元组的元素，需要加*
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except NoSuchElementException:
            logger.warning('找不到定位元素: %s' % loc[1])
            self.get_screent_img('找不到定位元素截图')
            raise Exception('找不到定位元素: %s' % loc[1])
        except TimeoutException:
            logger.warning('查找元素超时: %s' % loc[1])
            self.get_screent_img('查找元素超时截图')
            raise Exception('查找元素超时: %s' % loc[1])

    def find_elements(self, *loc):
        try:
            # 元素可见时，返回查找到的元素；以下入参为元组的元素，需要加*
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_elements(*loc).is_displayed())
            return self.driver.find_elements(*loc)
        except NoSuchElementException:
            logger.warning('找不到定位元素: %s' % loc[1])
            #self.log.myloggger('Can not find element: %s' % loc[1], flag=2)
            raise
        except TimeoutException:
            logger.warning('查找元素超时: %s' % loc[1])
            #self.log.myloggger('Can not find element: %s' % loc[1], flag=2)
            raise

    def get_screent_img(self,value):
        '''将页面截图下来'''
        file_path = './report/screenshot/'
        image_path = self.SCREENSHOTS_PATH
        now = time.strftime("%Y-%m-%d_%H_%M_%S_")
        screen_name = image_path+value+now+'.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)
            logger.info("页面已截图，截图的路径在项目: %s "%image_path)
        except NameError as ne:
            logger.error("失败截图 %s" % ne)
            self.get_screent_img(value)
            raise Exception("失败截图 %s" % ne)

    def send_key(self, loc, text):
        logger.info('清空文本框内容: %s...' % loc[1])
        self.find_element(*loc).clear()
        time.sleep(1)
        logger.info('输入内容方式 by %s: %s...' % (loc[0], loc[1]))
        try:
            if 'AES<<' in str(text) and '>>' in str(text):
                logger.info('输入内容: %s' % text)
                self.find_element(*loc).send_keys(EncryptDecode().decrypt(str(text).split('<<')[1].split('>>')[0]))
            elif 'password<<' in str(text) and '>>password' in str(text):
                logger.info('输入内容: %s' % ('*'*len(str(text).split('password<<')[1].split('>>password')[0])))
                self.find_element(*loc).send_keys(str(text).split('password<<')[1].split('>>password')[0])
            else:
                logger.info('输入内容: %s' % text)
                self.find_element(*loc).send_keys(str(text))
        except Exception as e:
            logger.error("输入内容失败 %s" % e)
            self.get_screent_img(str(text))
            raise Exception("输入内容失败 %s" % e)

    def click(self, loc):
        logger.info('点击元素 by %s: %s...' % (loc[0], loc[1]))
        try:
            self.find_element(*loc).click()
        except AttributeError as e:
            logger.error("无法点击元素: %s" % e)
            raise Exception("无法点击元素: %s" % e)

    def click_Dice(self,loc,num,dice_Num):
        logger.info('点击元素需要切成%s块！' % (dice_Num))
        try:
            ele_data = self.get_ele_size(loc)
            ele = ele_data[0]
            # 元素y轴中间值
            middleCoordinate_y = ele.location['y'] + ele_data[2] / 2
            #将宽分成指定份
            end_x_dice_Num = ele_data[1]/dice_Num
            #元素x轴左边
            start_x = ele.location['x']
            #指定模块的中间x坐标
            dice_middleCoordinate_x = ((end_x_dice_Num*(num) + start_x) - (end_x_dice_Num*(num-1) + start_x))/2 + (end_x_dice_Num*(num-1) + start_x)
            logger.info('点击第%s个元素块！' % (num))
            self.click_coordinates(dice_middleCoordinate_x,middleCoordinate_y)
        except AttributeError as e:
            logger.error("无法点击元素切块: %s" % e)
            raise Exception("无法点击元素切块: %s" % e)

    def clear(self,loc):
        '''输入文本框清空操作'''
        element = self.find_element(*loc)
        try:
            element.clear()
            logger.info('清空文本框内容')
        except NameError as ne:
            logger.error("清空文本框内容失败: %s" % ne)
            self.get_screent_img(ne)
            raise Exception("清空文本框内容失败: %s" % ne)

    def clean_text(self,text):
        '''使用退格键清空文本方式'''
        for i in range(len(text)):
            self.KEYCODE(67)  # 67退格键

    def wait(self,seconds):
        self.driver.implicitly_wait(seconds)
        logger.info("等待 %d 秒" % seconds)

    def get_text(self, loc):
        '''获取文本'''
        element = self.find_element(*loc)
        return element.text

    def get_content_desc_text(self, loc):
        '''获取content_desc文本'''
        element = self.find_element(*loc)
        return element.get_attribute(name='content-desc')

    def get_element_attribute(self, loc, index):
        '''获取元素属性'''
        element = self.find_element(*loc)
        return element.get_attribute(index)

    def operator(self,x,y):
        '''比较两者是否一致'''
        if operator.eq(x,y) is True:
            return True
        else:
            raise Exception(str(x),str(y) + '这两者不一致')
    def switch_to_context(self):
        logger.info(self.driver.contexts)

    def quit(self):
        """
        退出浏览器
        """
        logger.info("退出app")
        self.driver.quit()

    def KEYCODE(self,number):
        '''敲击键盘'''
        try:
            self.driver.press_keycode(number)
        except Exception as e:
            logger.error("敲击键盘失败 %s" % e)

    def KEYCODE_ENTER(self):
        '''敲击回车键'''
        self.driver.press_keycode(66)
    def KEYCODE_BACK(self):
        '''敲击返回键'''
        self.driver.press_keycode(4)
    def KEYCODE_RECOVERY(self):
        '''收回键盘'''
        size = self.get_size()
        self.click_coordinates(10,size[1]*0.4)

    def elementExist(self, loc):
        '''判断元素是否存在'''
        try:
            self.driver.find_element(*loc)
        except NoSuchElementException as e:
            return False
        else:
            return True

    def removePunctuation(self,data):
        '''去除标点符号'''
        data = str(data)
        data = re.sub(r'[^\w\s]','',data)
        return data.strip()

    def startApp(self,appPackage,appActivity):
        '''启动App'''
        try:
            self.driver.start_activity(appPackage,appActivity)
        except Exception as e:
            logger.info('启动App失败，失败原因为：{}'.format(e))

    def switchApp(self,appPackage):
        '''切换App'''
        try:
            self.driver.activate_app(appPackage)
        except Exception as e:
            logger.info('切换App失败，失败原因为：{}'.format(e))

    def get_size(self):
        # 获取窗口尺寸
        size = self.driver.get_window_size()
        x = size['width']
        y = size['height']
        return x, y

    def swipe_up(self,x=None,distance=None):
        # 向上滑动
        size = self.get_size()
        '''
        输入x坐标，可以在指导x坐标上滑
        '''
        if x is not None:
            x1 = x
        else:
            x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.7)
        y2 = int(size[1] * 0.2)
        if distance is not None:
            y = str(distance).split('->')
            self.driver.swipe(x1, int(size[1] * float(y[0].replace(' ',''))), x1, int(size[1] * float(y[1].replace(' ',''))), 500)
        else:
            self.driver.swipe(x1, y1, x1, y2, 500)

    def swipe_down(self,x=None,distance=None):
        # 向下滑动
        size = self.get_size()
        '''
        输入x坐标，可以在指导x坐标下滑
        '''
        if x is not None:
            x1 = x
        else:
            x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.2)
        y2 = int(size[1] * 0.7)
        if distance is not None:
            y = str(distance).split('->')
            self.driver.swipe(x1, int(size[1] * float(y[0].replace(' ', ''))), x1,int(size[1] * float(y[1].replace(' ', ''))), 500)
        else:
            self.driver.swipe(x1, y1, x1, y2, 500)

    def swipe_left(self,y=None,distance=None):
        # 向左滑动
        '''
        输入y坐标，可以在指导y坐标左滑
        '''
        size = self.get_size()
        x1 = int(size[0] * 0.9)
        x2 = int(size[0] * 0.1)
        if y is not None:
            y1 = y
        else:
            y1 = int(size[1] * 0.5)
        if distance is not None:
            x = str(distance).split('->')
            self.driver.swipe(int(size[1] * float(x[0].replace(' ', ''))), y1, int(size[1] * float(x[1].replace(' ', ''))), y1, 500)
        else:
            self.driver.swipe(x1, y1, x2, y1, 500)

    def swipe_right(self,y=None,distance=None):
        # 向右滑动
        '''
        输入y坐标，可以在指导y坐标右滑
        '''
        size = self.get_size()
        x1 = int(size[0] * 0.1)
        x2 = int(size[0] * 0.9)
        if y is not None:
            y1 = y
        else:
            y1 = int(size[1] * 0.5)
        if distance is not None:
            x = str(distance).split('->')
            self.driver.swipe(int(size[1] * float(x[0].replace(' ', ''))), y1, int(size[1] * float(x[1].replace(' ', ''))), y1, 500)
        else:
            self.driver.swipe(x1, y1, x2, y1, 500)

    def swipe_custom(self,x1,y1,x2,y2,time=None):
        self.driver.swipe(x1,y1,x2,y2,time)

    def click_coordinates(self,x,y):
        logger.info('点击坐标[{},{}]!!'.format(x,y))
        self.driver.tap([(x, y)])

    def click_Screen_center(self):
        xy = self.get_size()
        logger.info('点击坐标[{},{}]!!'.format(xy[0]*0.5,xy[1]*0.5))
        self.driver.tap([(xy[0]*0.5,xy[1]*0.5)])

    def calculate(self,image1, image2):
        image1 = cv2.cvtColor(numpy.asarray(image1), cv2.COLOR_RGB2BGR)
        image2 = cv2.cvtColor(numpy.asarray(image2), cv2.COLOR_RGB2BGR)
        hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
        # 计算直方图的重合度
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)
        return degree

    def cmppic(self,image1, image2, size=(256, 256)):
        image1 = Image.open(image1)
        image2 = Image.open(image2)
        # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
        image1 = cv2.cvtColor(numpy.asarray(image1), cv2.COLOR_RGB2BGR)
        image2 = cv2.cvtColor(numpy.asarray(image2), cv2.COLOR_RGB2BGR)
        image1 = cv2.resize(image1, size)
        image2 = cv2.resize(image2, size)
        sub_image1 = cv2.split(image1)
        sub_image2 = cv2.split(image2)
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += self.calculate(im1, im2)
        sub_data = sub_data / 3
        return sub_data

    def scoll2bottom(self):
        '''
        一直循环向上滑动，直到两张图片一致
        '''
        isbottom = False
        size = self.get_size()
        while not isbottom:
            self.driver.save_screenshot(os.path.join(self.SCREENSHOTS_PATH,'phone1.png'))
            self.swipe_custom(size[0]*0.5,size[1]*0.7,size[0]*0.5,size[1]*0.3,200)
            time.sleep(0.5)
            self.driver.save_screenshot(os.path.join(self.SCREENSHOTS_PATH,'phone2.png'))

            if self.cmppic(os.path.join(self.SCREENSHOTS_PATH,'phone1.png'), os.path.join(self.SCREENSHOTS_PATH,'phone2.png')) > 0.97:
                isbottom = True

    def scoll2top(self):
        '''
        一直循环向下滑动，直到两张图片一致
        '''
        isbottom = False
        size = self.get_size()
        while not isbottom:
            self.driver.save_screenshot(os.path.join(self.SCREENSHOTS_PATH,'phone1.png'))
            self.swipe_custom(size[0]*0.5,size[1]*0.3,size[0]*0.5,size[1]*0.7,200)
            time.sleep(0.5)
            self.driver.save_screenshot(os.path.join(self.SCREENSHOTS_PATH,'phone2.png'))

            if self.cmppic(os.path.join(self.SCREENSHOTS_PATH,'phone1.png'), os.path.join(self.SCREENSHOTS_PATH,'phone2.png')) > 0.97:
                isbottom = True

    def get_ele_size(self,loc):
        '''
        获取元素长宽
        Returns
        -------
        width，height
        '''
        ele = self.find_element(*loc)
        # 元素的宽
        width = ele.size['width']
        # 元素的高
        height = ele.size['height']
        return ele,width,height

    def swipe_SeekBar(self,loc,num,dice_Num):
        '''
        滑动滑块
        1、指定滑块宽的中间坐标（固定值）
        2、指定滑块长度，根据项目切分成8块
        3、先操作从右滑倒左，让滑块归零
        '''
        if '[' in loc and ']' in loc:
            size = str(loc).split('][')
            x1 = size[0].split(',')[0].replace('[','')
            x2 = size[1].split(',')[0]
            y1 = size[0].split(',')[1]
            y2 = size[1].split(',')[1].replace(']','')
            #元素y轴中间值
            middleCoordinate_y = int(y1) + ((int(y2) - int(y1))/2)
            #将宽分成指定份
            end_x_dice_Num = (int(x2) - int(x1))/dice_Num
            #将滑块滑到最左边
            for i in range(dice_Num):
                self.swipe_custom(int(x2)-int(i*end_x_dice_Num), middleCoordinate_y, x1, middleCoordinate_y)
            #通过num判断滑到哪个位置
            self.swipe_custom(x1, middleCoordinate_y, num * end_x_dice_Num, middleCoordinate_y)
        else:
            ele_data = self.get_ele_size(loc)
            ele = ele_data[0]
            #元素y轴中间值
            middleCoordinate_y = ele.location['y']+ele_data[2]/2
            #元素x轴左边
            start_x = ele.location['x']
            #元素x轴右边
            end_x = ele.location['x'] + ele_data[1]
            #将宽分成指定份
            end_x_dice_Num = ele_data[1]/dice_Num
            #将滑块滑到最左边
            for i in range(dice_Num):
                self.swipe_custom(int(end_x)-int(i*end_x_dice_Num),middleCoordinate_y,start_x,middleCoordinate_y)
            #通过num判断滑到哪个位置
            self.swipe_custom(start_x,middleCoordinate_y,num*end_x_dice_Num,middleCoordinate_y)

    def find_text_in_the_picture_of_OCR(self, text):
        '''
        截图
        根据text找到截图所在的文本坐标
        Returns：
        x,y坐标
        '''
        logging.disable(logging.DEBUG)
        img_path = os.path.join(self.SCREENSHOTS_PATH, 'ocr_png_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.png')
        self.driver.save_screenshot(img_path)
        ocr = PaddleOCR(use_angle_cls=False, use_gpu=False,enable_mkldnn=True)
        result = ocr.ocr(img_path, cls=False)
        qualified_coordinates = []
        for line in result:
            #截图上的内容
            screenshot_txt = line[1][0]
            #判断目标内容是否在截图上，在的话返回对应坐标
            if text in screenshot_txt:
               if line[1][1] > 0.8:
                   box = line[0]
                   x = (box[0][0] + box[1][0]) / 2
                   y = (box[0][1] + box[2][1]) / 2
                   qualified_coordinates.append('[' + str(x) + ',' + str(y)+']')
               else:
                   logger.info("ocr识别评分过低,source:{},target:{}".format(screenshot_txt, text))
        if qualified_coordinates == []:
            logger.info("ocr识别截图，无{}文本信息".format(text))
        else:
            return qualified_coordinates

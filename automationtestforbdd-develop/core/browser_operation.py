import logging
import os
import time
from datetime import datetime

#import pymouse as PyMouse
import pywinauto as pywinauto
import win32api
import win32con
from paddleocr import PaddleOCR
from pywinauto.keyboard import send_keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from common.logger import logger
from selenium import webdriver
from config.Config import SCREENSHOTS_PATH, DOWNLOAD_FILE, CHROME_USER_DATA, UPLOAD_FILE
from utils.AES import EncryptDecode


class Operates(object):
    # 初始化页面的操作
    def __init__(self):
        """
        构造函数，创建必要的实例变量
        """
        self.driver = None
        self.log = logger  # 初始化一个log对象


    def openBrowser(self, driver='gc'):
        """
        打开不同的浏览器
        :param driver: gc=谷歌浏览器；ff=Firefox浏览器； ie=IE浏览器
        :return:
        """
        if driver == 'gc':
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["pageLoadStrategy"] = "none"
            option = webdriver.ChromeOptions()
            # option.add_argument('--disable-popup-blocking')
            option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
            #不安全链接去除
            option.add_argument('--ignore-certificate-errors')
            #浏览器配置路径
            option.add_argument('user-data-dir='+CHROME_USER_DATA)
            self.driver = webdriver.Chrome(chrome_options=option)
            # self.driver = webdriver.Chrome()
        elif driver == 'ff':
            self.driver = webdriver.Firefox()
        elif driver == 'ie':
            self.driver = webdriver.Ie()
        else:
            self.log.info("不支持，请在此添加其他浏览器代码实现！")
            pass

        # 默认隐式等待10s
        self.driver.implicitly_wait(10)

    def find_element(self,*loc):
        try:
            # 元素可见时，返回查找到的元素；以下入参为元组的元素，需要加*
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except NoSuchElementException:
            logger.warning('找不到定位元素: %s' % loc[1])
            self.getImage('找不到定位元素截图')
            raise Exception('找不到定位元素: %s' % loc[1])
        except TimeoutException:
            logger.warning('查找元素超时: %s' % loc[1])
            self.getImage('查找元素超时截图')
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

    def sleep(self,seconds):
        try:
            self.log.info("停顿{}秒".format(str(seconds)))
            time.sleep(seconds)
        except Exception as e:
            self.log.error("停顿失败！")
            raise Exception("停顿失败: %s" % e)

    def stopLoading(self):
        win32api.keybd_event(27, 0, 0, 0)
        win32api.keybd_event(27, 0, win32con.KEYEVENTF_KEYUP, 0)
        return

    def click(self, locator,js=None):
        """
        找到元素，并点击
        :param locator: 定位器
        :return:
        """
        try:
            self.log.info('点击元素 by {}: {}...'.format(locator[0], locator[1]))
            if js != 'None' and 'window.stop()'in js:
                self.stopLoading()
                self.find_element(*locator).click()
            elif js != 'None' and 'window.stop()' not in js:
                self.by_js(js)
                self.find_element(*locator).click()
            else:
                self.find_element(*locator).click()
        except AttributeError as e:
            self.log.error("无法点击元素: %s" % e)
            raise Exception("无法点击元素: %s" % e)

    def double_click(self, locator):
        """
        找到元素，并双击
        :param locator: 定位器
        :return:
        """
        try:
            self.log.info('双击元素 by {}: {}...'.format(locator[0], locator[1]))
            ActionChains(self.driver).double_click(self.find_element(*locator)).perform()
        except AttributeError as e:
            self.log.error("无法双击元素: %s" % e)
            raise Exception("无法双击元素: %s" % e)

    def click_ele_exist(self, locator):
        """
        当定为元素出现时，定位元素，并点击
        :param locator: 定位器
        :return:
        """
        try:
            self.find_element(*locator)
            btns = self.find_elements(*locator)
            # 如果出现用户协议弹出按钮
            if btns:
                btns[0].click()
        except Exception as e:
            self.log.error("定位有时出现的点击元素失败！")
            raise Exception("无法点击元素: %s" % e)

    def input_text(self, locator, value):
        """
        定位元素，并完成输入
        :param text:
        :param locator:
        :return:
        """
        try:
            self.log.info('清空文本框内容: %s...' % locator[1])
            self.find_element(*locator).clear()
            self.log.info('输入内容方式 by {}: {}...'.format(locator[0], locator[1]))
            if 'AES<<' in str(value) and '>>' in str(value):
                self.log.info('输入内容为: {}...'.format(value))
                self.find_element(*locator).send_keys(EncryptDecode().decrypt(str(value).split('<<')[1].split('>>')[0]))
            elif 'password<<' in str(value) and '>>password' in str(value):
                self.log.info('输入内容为: {}...'.format('*'*len(str(value).split('password<<')[1].split('>>password')[0])))
                self.find_element(*locator).send_keys(str(value).split('password<<')[1].split('>>password')[0])
            else:
                self.log.info('输入内容为: {}...'.format(value))
                self.find_element(*locator).send_keys(str(value))
        except Exception as e:
            self.log.info("定位输入元素失败！")
            raise Exception("定位输入元素失败: %s" % e)

    # 根据css定位的元素
    def by_js(self, js):
        try:
            logger.info("执行js指令：%s" % js)
            self.driver.execute_script(js)
        except Exception as e:
            self.log.error("执行js指令失败！")
            raise Exception("执行js指令失败: %s" % e)

    def switch_window(self, target_title):
        """
        切换到新窗口
        :param target_title:
        :return:
        """
        try:
            win = self.driver.window_handles
            if str(target_title).isnumeric() is False:
                for handle in win:
                    self.driver.switch_to.window(handle)
                    # 判断切换到窗口句柄——-判断当前窗口的标题是否是：<header>中的<title>
                    if target_title == self.driver.title:
                        self.log.info("切换到新窗口{}".format(target_title))
                        break
            else:
                self.driver.switch_to.window(win[int(target_title)])
        except Exception as e:
            self.log.error("切换新窗口失败！")
            raise Exception("切换新窗口失败: %s" % e)

    def into_iframe(self, locator):
        """
        进入iframe
        :param locator:  ?
        :return:
        """
        try:
            self.log.info('切入iframe方式 by {}: {}...'.format(locator[0], locator[1]))
            ele = self.find_element(*locator)
            self.driver.switch_to.frame(ele)
        except Exception as e:
            self.log.error("切换框架frame失败！")
            raise Exception("切换框架frame失败: %s" % e)

    def q_iframe(self):
        """
        退出iframe至父级
        :param element:  ?
        :return:
        """
        try:
            self.log.info('退出iframe')
            self.driver.switch_to.parent_frame()
        except Exception as e:
            self.log.error("退出框架frame失败！")
            raise Exception("退出框架frame失败: %s" % e)

    def get_text(self, locator):
        """
        获取文本元素
        :param locator:
        :return:
        """
        try:
            ele = self.find_element(*locator)
        except Exception as e:
            self.log.error("获取元素文本失败！")
            raise Exception("获取元素文本失败: %s" % e)
        else:
            return ele.text

    def get_attribute(self,locator,attribute):
        """
        获取元素属性的值
        :param locator:
        :return:
        """
        try:
            ele = self.find_element(*locator)
        except Exception as e:
            self.log.error("获取元素文本失败！")
            raise Exception("获取元素文本失败: %s" % e)
        else:
            return ele.get_attribute(attribute)

    def get_url(self, url=None):
        """
        打开网站
        :param url: 网站地址
        :return:
        """
        try:
            self.log.info('打开url: {}'.format(url))
            self.driver.get(url)
            self.driver.maximize_window()
            time.sleep(2)
            win32api.keybd_event(13, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(5)
        except Exception as e:
            self.log.error("打开url失败！")
            raise Exception("打开url失败: %s" % e)

    def getImage(self, image_name):
        """
        生成用例失败的截图
        :param image_name: 截图的名称
        :return:
        """
        try:
            nowTime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            NewPicture = SCREENSHOTS_PATH + nowTime + '_' + image_name + '.png'   # 保存图片为png格式
            self.driver.get_screenshot_as_file(NewPicture)
            self.log.info("页面已截图，截图的路径在项目: {} ".format(SCREENSHOTS_PATH))
        except Exception as e:
            self.log.error(u'截图失败！')
            raise Exception("截图失败: %s" % e)

    def Focus(self,locator):
        """
        聚焦元素
        :return:
        """
        try:
            self.log.info("聚焦元素方式 by {}: {}".format(locator[0],locator[1]))
            ele = self.find_element(*locator)
            self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        except Exception as e:
            raise Exception("聚焦元素失败: %s" % e)

    def selectDropDownBox(self,locator,text):
        """
        定位select下拉框
        :param locator:
        :param text:
        :return:
        """
        try:
            self.log.info("定位select下拉框方式 by {}: {}".format(locator[0], locator[1]))
            ele = self.find_element(*locator)
            s = Select(ele)
            self.log.info("选择select下拉框内容: {}".format(text))
            s.select_by_visible_text(text)
        except Exception as e:
            raise Exception("select下拉框选择失败: %s" % e)

    def mouseHover(self,locator):
        """
        鼠标移动到指导元素
        :param locator:
        :return:
        """
        try:
            self.log.info("鼠标悬停方式 by {}: {}".format(locator[0], locator[1]))
            ele = self.find_element(*locator)
            ActionChains(self.driver).move_to_element(ele).perform()
        except Exception as e:
            raise Exception("鼠标移动到指定元素失败: %s" % e)

    def mouseClick(self,locator):
        """
        鼠标点击元素
        :param locator:
        :return:
        """
        try:
            self.log.info("鼠标点击方式 by {}: {}".format(locator[0], locator[1]))
            ele = self.find_element(*locator)
            ActionChains(self.driver).click(ele).perform()
        except Exception as e:
            raise Exception("鼠标点击指定元素失败: %s" % e)

    def mouseRightClick(self,locator):
        """
        鼠标右键点击元素,并链接另存为
        :param locator:
        :return:
        """
        try:
            self.log.info("鼠标右键点击方式 by {}: {}".format(locator[0], locator[1]))
            ele = self.find_element(*locator)
            ActionChains(self.driver).move_to_element(ele).context_click(ele).perform()
            win32api.keybd_event(75, win32con.KEYEVENTF_KEYUP, 0)
        except Exception as e:
            raise Exception("鼠标右键点击指定元素失败: %s" % e)

    def mouseClickAndHold(self,locator):
        """
        鼠标点击不释放
        """
        try:
            self.log.info("鼠标左键点击元素{}不释放".format(locator[1]))
            ele = self.find_element(*locator)
            ActionChains(self.driver).click_and_hold(ele).perform()
        except Exception as e:
            raise Exception("鼠标左键点击元素不释放失败: %s" % e)

    def mouseRelease(self,locator=None):
        """
        释放鼠标点击
        """
        try:
            self.log.info("鼠标在元素{}释放".format(locator[1]))
            if locator is not None:
                ActionChains(self.driver).release(self.find_element(*locator)).perform()
            else:
                ActionChains(self.driver).release().perform()
        except Exception as e:
            raise Exception("鼠标在元素释放失败: %s" % e)

    def mouseDragAndDrop(self,locator1,locator2):
        """
        鼠标拖拽操作 元素locator1 拖拽到 元素locator2
        :param locator1:
        :param locator2:
        """
        try:
            self.log.info("鼠标拖拽元素{} -> 元素{}".format(locator1[1],locator2[1]))
            ele1 = self.find_element(*locator1)
            ele2 = self.find_element(*locator2)
            ActionChainsDriver = ActionChains(self.driver)
            ActionChainsDriver.click_and_hold(ele1).perform()
            self.Focus(locator2)
            ActionChainsDriver.move_by_offset(ele2.location['x'],ele2.location['y']).perform()
            ActionChainsDriver.release(ele1).perform()
        except Exception as e:
            raise Exception("鼠标拖拽元素失败: %s" % e)

    def elementExist(self, locator):
        '''判断元素是否存在'''
        try:
            self.driver.find_element(*locator)
        except NoSuchElementException as e:
            return False
        else:
            return True

    def closePopupAlert(self):
        """
        关闭Alert弹窗
        :return:
        """
        try:
            self.log.info("获取alert弹窗！")
            al = self.driver.switch_to.alert
            self.log.info("关闭alert弹窗！")
            al.accept()
        except Exception as e:
            raise Exception("关闭alert弹窗失败: %s" % e)

    def close(self):
        """
        退出窗口
        :return:
        """
        try:
            self.log.info("关闭当前窗口")
            self.driver.close()
        except Exception as e:
            self.log.error("关闭窗口失败！")
            raise Exception("关闭窗口失败: %s" % e)


    def quit(self):
        """
        退出浏览器
        :return:
        """
        try:
            self.log.info("退出浏览器")
            self.driver.quit()
        except Exception as e:
            self.log.error("退出浏览器失败！")
            raise Exception("退出浏览器失败: %s" % e)

    # 后退
    def back(self):
        self.log.info("后退")
        self.driver.back()

    # 前进
    def forword(self):
        self.log.info("前进")
        self.driver.forword()

    def KEYCODE(self,text):
        '''键盘输入内容'''
        ActionChains(self.driver).send_keys(text).perform()

    def KEYCODE_ENTER(self,locator):
        '''敲击回车键'''
        self.find_element(*locator).send_keys(Keys.ENTER)

    def KEYCODE_BACK_SPACE(self,locator):
        '''敲击删除键'''
        self.find_element(*locator).send_keys(Keys.BACK_SPACE)

    def KEYCODE_CTRL_letter(self,locator,letter):
        '''敲击Ctrl+letter'''
        self.find_element(*locator).send_keys(Keys.CONTROL, letter)

    def Upload(self,file,path=None):
        '''上传文件'''
        app = pywinauto.Desktop()  # 使用pywinauto来选择文件
        dlg = app["打开"]  # 选择文件上传的窗口
        dlg["Toolbar3"].click()  # 选择文件地址输入框
        if path is None:
            send_keys(UPLOAD_FILE)
        else:
            send_keys(path)  # 键盘输入上传文件的路径
        send_keys("{VK_RETURN}")  # 键盘输入回车，打开该路径
        dlg["文件名(&N):Edit"].type_keys(file)  # 选中文件名输入框，输入文件名
        dlg["打开(&O)"].click()  # 点击打开

    def Download(self):
        '''下载文件'''
        app = pywinauto.Desktop()  # 使用pywinauto来选择文件
        dlg = app["另存为"]  # 选择文件上传的窗口
        dlg["Toolbar3"].click()  # 选择文件地址输入框
        send_keys(DOWNLOAD_FILE)
        send_keys("{VK_RETURN}")
        send_keys("{VK_RETURN}")
        # dlg["打开(&O)"].click()

    def PYKEYCODE_ENTER(self):
        '''敲击回车键，不在元素上'''
        send_keys("{VK_RETURN}")

    def find_text_in_the_picture_of_OCR_get_Verification_Code(self):
        '''
        截图
        根据text找到截图所在的文本坐标
        Returns：
        Verification Code
        '''
        logging.disable(logging.DEBUG)
        img_path = os.path.join(SCREENSHOTS_PATH, 'ocr_png_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.png')
        self.driver.save_screenshot(img_path)
        ocr = PaddleOCR(use_angle_cls=False, use_gpu=False,enable_mkldnn=True)
        result = ocr.ocr(img_path, cls=False)
        for i in range(len(result)):
            #截图上的内容
            #判断目标内容是否在截图上，在的话返回验证码
            if '验证码' in result[i][1][0]:
                return result[i+1][1][0]
# if __name__ == '__main__':
#     # ele =BasePage()
#     path = os.path.dirname(os.path.abspath('.'))
#     print(path)

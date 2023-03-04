from common.getPath import get_app_parameter_yaml_path
from common.logger import logger
from appium import webdriver

from config.Project import PROJECT, ISYAML
from utils.file_read import YamlReader


class AppDriver(object):

    def __init__(self):
        self.c = YamlReader(get_app_parameter_yaml_path(ISYAML,PROJECT)).data[0]['desired_caps']

    def openApp(self):
        logger.info("启动LiviBank")
        desired_caps = {}
        desired_caps['platformName'] = self.c["platformName"]
        # desired_caps['platformVersion'] = str(self.c["platformVersion"])
        desired_caps['deviceName'] = self.c["deviceName"]
        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True
        #默认超时等待2000s
        desired_caps['newCommandTimeout'] = 2000
        if desired_caps['platformName'].lower() == 'android':
            # autoLaunch为True时会重启app，False时不重启app，可在app继续执行步骤(仅限安卓)
            desired_caps['skipServerInstallation'] = False
            desired_caps['skipDeviceInitialization'] = False
            desired_caps['autoLaunch'] = self.c["autoLaunch"]
            desired_caps['appActivity'] = self.c["appActivity"]
            desired_caps['appPackage'] = self.c["appPackage"]
            desired_caps['noReset'] = True
        else:
            desired_caps['noReset'] = self.c["noReset"]
            desired_caps['udid'] = self.c["udid"]
            desired_caps['app'] = self.c["appPackage"]
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        return driver

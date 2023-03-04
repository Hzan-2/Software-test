import atexit
import os
import shutil

from common.getVariable import get_system
from common.updataProject import updata_project
from config.Config import REPORT_PATH, HTMLREPORT_PATH, SCREENSHOTS_PATH, VIDEO_PATH, FEATURES_YAML, FEATURES_FILE, \
    ALLURE_FILE, DOWNLOAD_FILE


def delReport():
    for fileName in os.listdir(REPORT_PATH):
        os.remove(REPORT_PATH + '/' + fileName)
    for fileName in os.listdir(HTMLREPORT_PATH):
        if '.' in fileName:
            os.remove(HTMLREPORT_PATH + '/' + fileName)
        else:
            shutil.rmtree(HTMLREPORT_PATH + '/' + fileName, ignore_errors=True)

def defScreenshots():
    for fileName in os.listdir(SCREENSHOTS_PATH):
        os.remove(SCREENSHOTS_PATH + '/' + fileName)

def delVideo():
    for fileName in os.listdir(VIDEO_PATH):
        os.remove(os.path.join(VIDEO_PATH, fileName))

def delSteps(path):
    if get_system() == 'Windows':
        for fileName in os.listdir(os.path.join(FEATURES_YAML, path.split('\\')[0], 'steps')):
            os.remove(os.path.join(os.path.join(FEATURES_YAML, path.split('\\')[0], 'steps'), fileName))
    else:
        for fileName in os.listdir(os.path.join(FEATURES_YAML, path.split('/')[0], 'steps')):
            os.remove(os.path.join(os.path.join(FEATURES_YAML, path.split('/')[0], 'steps'), fileName))

def delDownloadFile():
    for fileName in os.listdir(os.path.join(DOWNLOAD_FILE)):
        os.remove(os.path.join(DOWNLOAD_FILE,fileName))

def delData():
    delReport()
    defScreenshots()
    delVideo()
    delDownloadFile()

def generateSteps(path):
    delSteps(path)
    from common.generateStep import generateStep
    generateStep().generate_Step_File(path)

def updataProject():
    if get_system() == 'Windows':
        updata_project(project,type)
    else:
        updata_project(project,type)

def runTestCase(pathList,type):
    for path in pathList:
        if type == 'yaml':
            if '.feature' in path:
                os.system("behave -f allure_behave.formatter:AllureFormatter -o {} {}".format(REPORT_PATH, os.path.join(FEATURES_YAML,project,path)))
        else:
            if '.feature' in path:
                os.system("behave -f allure_behave.formatter:AllureFormatter -o {} {}".format(REPORT_PATH, os.path.join(FEATURES_FILE,project,path)))
    if pathList == []:
        if type == 'yaml':
            for fileName in os.listdir(os.path.join(FEATURES_YAML,project)):
                if '.feature' in fileName:
                    os.system("behave -f allure_behave.formatter:AllureFormatter -o {} {}".format(REPORT_PATH,os.path.join(FEATURES_YAML,project,fileName)))
        else:
            for fileName in os.listdir(os.path.join(FEATURES_FILE,project)):
                if '.feature' in fileName:
                    os.system("behave -f allure_behave.formatter:AllureFormatter -o {} {}".format(REPORT_PATH,os.path.join(FEATURES_FILE,project,fileName)))
    quitDriverAndopenReport()

#@atexit.register
def quitDriverAndopenReport():
    os.system(r"{} generate {} -o {}".format(ALLURE_FILE,REPORT_PATH, HTMLREPORT_PATH))
    result = os.system("{} serve {}".format(ALLURE_FILE,REPORT_PATH))
    print("result={}".format(result))

if __name__ == '__main__':
    #清除数据
    delData()
    #项目文件夹名称
    project = 'PaymentProject'
    #执行用例类型,yaml模式就填写yaml，code模式则写其它
    type = 'yaml'
    #更新项目
    updataProject()
    #生成steps
    if type == 'yaml':
        generateSteps(os.path.join(project,''))
    #执行案例
    featureList = [
        # 'test_AppLogin.feature',
        'test_livisavaMC_Web_02.feature'
    ]
    runTestCase(featureList,type)

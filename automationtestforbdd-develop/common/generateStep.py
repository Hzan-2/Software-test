import os

from common.getVariable import get_system
from common.globalVar import gloVar
from common.logger import logger
from config.Config import FEATURES_YAML
from gherkin.Scenario import get_Scenario_Paragraph
from gherkin.library import fill_library
from utils.file_read import YamlReader


def get_step_data(path):
    try:
        return YamlReader(path).data[0]
    except Exception:
        if get_system() == 'Windows':
            logger.info('{}脚本格式不正确'.format(path.split('\\')[-1]))
            return
        else:
            logger.info('{}脚本格式不正确'.format(path.split('/')[-1]))
            return



class generateStep:

    def get_Steps_File_Name(self,path):
        stepsFileNameList = []
        if get_system() == 'Windows':
            for fileName in os.listdir(os.path.join(FEATURES_YAML,path.split('\\')[0],'yaml')):
                if '.yaml' in str(fileName):
                    stepsFileNameList.append(os.path.join(os.path.join(FEATURES_YAML,path.split('\\')[0],'yaml'),fileName))
        else:
            for fileName in os.listdir(os.path.join(FEATURES_YAML,path.split('/')[0],'yaml')):
                if '.yaml' in str(fileName):
                    stepsFileNameList.append(os.path.join(os.path.join(FEATURES_YAML,path.split('/')[0],'yaml'),fileName))
        return stepsFileNameList


    def generate_Step_File(self,path):
        #填充装置
        if get_system() == 'Windows':
            with open(os.path.join(FEATURES_YAML,path.split('\\')[0],'steps','fixture.py'), 'w', encoding="utf-8") as f:
                fill_library(f)
                get_Scenario_Paragraph(f, gloVar.fixtures)
            #获取指定yaml文件夹，获取所有路径
            stepsFileNameList = self.get_Steps_File_Name(path)
            #转换指定yaml文件的steps为py格式
            for yamlFile in stepsFileNameList:
                getStepData = get_step_data(yamlFile)
                stepFileName = str(os.path.join(FEATURES_YAML,path.split('\\')[0],'steps',str(yamlFile).split('\\')[-1]).split('yaml')[0])+'py'
                with open(stepFileName,'w',encoding="utf-8") as f:
                    fill_library(f)
                    get_Scenario_Paragraph(f,getStepData)
        else:
            with open(os.path.join(FEATURES_YAML,path.split('/')[0],'steps','fixture.py'), 'w', encoding="utf-8") as f:
                fill_library(f)
                get_Scenario_Paragraph(f, gloVar.fixtures)
            #获取指定yaml文件夹，获取所有路径
            stepsFileNameList = self.get_Steps_File_Name(path)
            #转换指定yaml文件的steps为py格式
            for yamlFile in stepsFileNameList:
                getStepData = get_step_data(yamlFile)
                stepFileName = str(os.path.join(FEATURES_YAML,path.split('/')[0],'steps',str(yamlFile).split('/')[-1]).split('yaml')[0])+'py'
                with open(stepFileName,'w',encoding="utf-8") as f:
                    fill_library(f)
                    get_Scenario_Paragraph(f,getStepData)

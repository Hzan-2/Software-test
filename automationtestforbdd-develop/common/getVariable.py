import ast
import json
import os
import platform
import random
import time

from common.getPath import *
from common.logger import logger
from config.Project import PROJECT, ISYAML
from utils.file_read import YamlReader
'''
:return: 当前系统
'''
def get_system():
    return platform.system()

'''
获取API请求头
'''
def getApiMessage(fileName):
    API_MESSAGE_YAML = get_api_parameter_file_path(ISYAML,PROJECT)
    for FileName in os.listdir(API_MESSAGE_YAML):
        try:
            if fileName == FileName:
                return YamlReader(os.path.join(API_MESSAGE_YAML, fileName+'.yaml')).data[0]
        except Exception:
            logger.error('API文件夹下的{},yaml格式错误'.format(fileName))
            raise Exception('API文件夹下的{},yaml格式错误'.format(fileName))

'''
获取APP端ElementYaml路径
'''
def getAppElementYamlPath(varKey):
    APP_ELEMENT_FILE = get_app_element_file_path(ISYAML,PROJECT)
    for fileName in os.listdir(APP_ELEMENT_FILE):
        try:
            if "dict_keys(['"+varKey+"'])" == str(YamlReader(os.path.join(APP_ELEMENT_FILE,fileName)).data[0].keys()):
                return os.path.join(APP_ELEMENT_FILE,fileName)
        except Exception:
            logger.error('{}yaml格式错误'.format(fileName))
            raise Exception('{}yaml格式错误'.format(fileName))

'''
获取WEB端ElementYaml路径(ps:需要根据项目文件夹划分)
'''
def getWebElementYamlPath(varKey,Project=None):
    WEB_ELEMENT_FILE = get_web_element_file_path(ISYAML,PROJECT)
    for fileName in os.listdir(WEB_ELEMENT_FILE):
        if "dict_keys(['" + varKey + "'])" == str(YamlReader(os.path.join(WEB_ELEMENT_FILE, fileName)).data[0].keys()):
            return os.path.join(WEB_ELEMENT_FILE, fileName)

'''
根据WEB项目和全局变量的Key值找到WEB的参数yaml文件路径
'''
def get_Web_parameter_yaml(varKey,Project=None):
    WEB_PARAMETER_FILE = get_web_parameter_file_path(ISYAML,PROJECT)
    for fileName in os.listdir(os.path.join(WEB_PARAMETER_FILE)):
        if "dict_keys(['" + varKey + "'])" == str(YamlReader(os.path.join(os.path.join(WEB_PARAMETER_FILE), fileName)).data[0].keys()):
            return os.path.join(os.path.join(WEB_PARAMETER_FILE), fileName)

'''     
判断是否是变量
'''
def judge_is_variable(text):
    if "$$" not in str(text) and "{" in str(text) and "}" in str(text):
        return get_variable(text)
    else:
        return str(text)

'''
判断步骤中是否封装了变量，如果格式为$${xxx},代表是步骤中的变量
'''
def is_variable(text,project=None):
    if str(text).count("$$") == 1 and str(text)[-1:] == '}' and str(text)[:2] == '$$':
        return del_format(str(text))
    #步骤变量的拼接
    elif str(text).count("$$") >= 1:
        Var = ''
        for var in str(text).split('$${'):
            if var == '':
                continue
            elif var[-1:] != "}" and var.count("}") == 0:
                Var = Var + "+'" + del_format(var) + "'"
            elif var[-1:] != "}" and var.count("}") > 0:
                vars = var.split("}")
                Var = Var + "+" + str(vars[0]) + "+'" + str(vars[1]) + "'"
            else:
                Var = Var + "+" + del_format(var)
        return Var[1:]
    #gherkin语法的变量，格式是{var}
    elif '$' not in text and '{' in text and '}' in text:
        if str(text).split('{')[0] == '' and str(text).split('{')[1].split('}')[1] == '':
            return 'get_variable('+str(text).split('{')[1].split('}')[0]+')'
        elif str(text).split('{')[0] != '' and str(text).split('{')[1].split('}')[1] == '':
            return '"' + str(text).split('{')[0] + '"+get_variable(' + str(text).split('{')[1].split('}')[0]+')'
        elif str(text).split('{')[0] == '' and str(text).split('{')[1].split('}')[1] != '':
            return 'get_variable('+str(text).split('{')[1].split('}')[0] + ')+"' + str(text).split('{')[1].split('}')[1] + '"'
        else:
            return '"' + str(text).split('{')[0] + '"+get_variable(' + str(text).split('{')[1].split('}')[0] + ')+"' + str(text).split('{')[1].split('}')[1] + '"'
    #不是步骤变量，校验一下是不是全局变量
    else:
        if project is None:
            return 'get_variable("' + str(text) + '")'
        else:
            return 'get_variable("' + str(text) + '","'+project+'")'

'''
获取常规数据变量
'''
def get_variable(variable,project=None):
    if "random(" in variable:
        try:
            if '_$' in variable and '}_' not in variable:
                var = del_format(variable).split('_random')
                section = var[1].replace('(','').replace(')','').replace('，',',').split(',')
                num = var[0] + str(random.randint(int(section[0]),int(section[1])))
            elif '}_' in variable and '_$' not in variable:
                var = del_format(variable).split('_')
                section = var[0].replace('random(', '').replace(')', '').replace('，', ',').split(',')
                num = str(random.randint(int(section[0]), int(section[1]))) + var[1]
            elif '_$' in variable and '}_' in variable:
                var = del_format(variable).split('_random')
                section = var[1].split('_')[0].replace('(', '').replace(')', '').replace('，', ',').split(',')
                num = var[0] + str(random.randint(int(section[0]),int(section[1]))) + var[1].split('_')[1]
            else:
                var = del_format(variable).split('random')
                section = var[1].replace('(','').replace(')','').replace('，',',').split(',')
                num = str(random.randint(int(section[0]),int(section[1])))
            logger.info('生成{}位随机数，随机数为：{}'.format(len(num),num))
            return str(num)
        except Exception:
            logger.error('{}随机变量不合法'.format(variable))
            raise Exception('{}随机变量不合法'.format(variable))
    #web端的数据变量，格式${Project}${varName}
    elif '}${' in variable:
        try:
            varList = variable.split('}${')
            if varList[0].split("$")[0] != '' and varList[1].split("}")[1] != '':
                return '"' + varList[0].split("$")[0] + YamlReader(os.path.join(get_Web_parameter_yaml(del_format(varList[0].split("$")[1]),project))).data[0][del_format(varList[0].split("$")[1])][del_format(varList[1].split("}")[0])] + varList[1].split("}")[1] + '"'
            elif varList[0].split("$")[0] == '' and varList[1].split("}")[1] != '':
                return '"' + YamlReader(os.path.join(get_Web_parameter_yaml(del_format(varList[0].split("$")[1]),project))).data[0][del_format(varList[0].split("$")[1])][del_format(varList[1].split("}")[0])] + varList[1].split("}")[1] + '"'
            elif varList[0].split("$")[0] != '' and varList[1].split("}")[1] == '':
                return '"' + varList[0].split("$")[0] + YamlReader(os.path.join(get_Web_parameter_yaml(del_format(varList[0].split("$")[1]),project))).data[0][del_format(varList[0].split("$")[1])][del_format(varList[1].split("}")[0])] + '"'
            else:
                return YamlReader(os.path.join(get_Web_parameter_yaml(del_format(varList[0]),project))).data[0][del_format(varList[0])][del_format(varList[1])]
        except Exception:
            logger.error('parameter.yaml文件不存在Web端{}变量不存在'.format(variable))
            raise Exception('parameter.yaml文件不存在Web端{}变量不存在'.format(variable))
    #app端的数据变量，格式${varName}
    elif '{' in variable and '}' in variable and '$' in variable and '}${' not in variable:
        try:
            varList = variable.split('${',1)
            APP_PARAMETER_YAML = get_app_parameter_yaml_path(ISYAML,PROJECT)
            c = YamlReader(APP_PARAMETER_YAML).data[0]
            if varList[0] != '' and varList[1].split("}",1)[1] != '':
                var = '"' + varList[0] + str(c[del_format(varList[1].split("}",1)[0])]) + varList[1].split("}",1)[1] + '"'
            elif varList[0] != '' and varList[1].split("}",1)[1] == '':
                var = '"' + varList[0] + str(c[del_format(varList[1].split("}",1)[0])]) + '"'
            elif varList[0] == '' and varList[1].split("}",1)[1] != '':
                var = '"' + str(c[del_format(varList[1].split("}",1)[0])]) + varList[1].split("}",1)[1] + '"'
            else:
                var = str(c[del_format(variable)])
            if '${' in var:
                return get_variable(var.strip('"'), PROJECT)
            else:
                return var
        except Exception:
            logger.error('parameter.yaml文件不存在App端{}变量不存在'.format(variable))
            raise Exception('parameter.yaml文件不存在App端{}变量不存在'.format(variable))
    #调用MDC平台参数变量，格式${tagStr;dataGroup}${phone}  ${tagStr;dataGroup}${password}   ${tagStr;dataGroup}${pin}
    #不是变量，直接返回
    else:
        return variable


'''
获取APP_Element元素变量，获取元素
'''
def get_App_Element_variable(variable,platformName,page=None,language=None):
    try:
        if variable.count('$') != 1 and variable.count('$') != 0:
            ele_variable = variable.split('$')
            page = del_format(ele_variable[1])
            c = YamlReader(getAppElementYamlPath(page)).data[0]
            ele = c[del_format(ele_variable[1])][platformName.lower()][del_format(ele_variable[2])]
            if '$' in ele:
                ele_variable = ele.split('}')
                return get_App_Element_variable(del_format(c[page][platformName.lower()][del_format(ele_variable[0])]),platformName.lower())+ele_variable[1]
            elif len(c[del_format(ele_variable[1])][platformName.lower()][del_format(ele_variable[2])]) == 3:
                return c[del_format(ele_variable[1])][platformName.lower()][del_format(ele_variable[2])][language]
            else:
                return c[del_format(ele_variable[1])][platformName.lower()][del_format(ele_variable[2])]
        elif variable.count('$') == 1 and variable.count('{') == 1 and variable.count('}') == 1:
            c = YamlReader(getAppElementYamlPath(page)).data[0]
            if len(c[page][platformName.lower()][del_format(variable)]) == 3:
                return c[page][platformName.lower()][del_format(variable)][language]
            elif '$' in c[page][platformName.lower()][del_format(variable)]:
                ele_variable = c[page][platformName.lower()][del_format(variable)].split('}')
                return get_App_Element_variable(del_format(c[page][platformName.lower()][del_format(ele_variable[0])]),[platformName.lower()],page)+ele_variable[1]
            else:
                return c[page][platformName.lower()][del_format(variable)]
        else:
            return variable
    except Exception:
        logger.error('APP端{}变量不存在'.format(variable))
        raise Exception('APP端{}变量不存在'.format(variable))

'''
获取Web_Element元素变量，获取元素
'''
def get_web_Element_variable(variable,Project):
    try:
        '''
        获取封装好的yaml步骤，根据action找到指定的yaml路径
        '''
        if "}${" in variable:
            varList = variable.split('}${')
            return YamlReader(os.path.join(getWebElementYamlPath(del_format(varList[0]),Project))).data[0][del_format(varList[0])][del_format(varList[1])]
        else:
            return variable
    except Exception:
        logger.error('WEB端{}项目，{}变量不存在'.format(Project,variable))
        raise Exception('WEB端{}项目，{}变量不存在'.format(Project,variable))

'''
元素含变量处理
'''
def get_new_Element(variable):
    try:
        if "$${" in variable:
            return str(variable).split('$${')[0] + '"+' + str(variable).split('$${')[1].split('}')[0] + '+"' + str(variable).split('$${')[1].split('}')[1]
        else:
            return variable
    except Exception:
        logger.error('{}元素输入不规范，请检查元素'.format(variable))
        raise Exception('{}元素输入不规范，请检查元素'.format(variable))

'''
去除符号
'''
def del_format(text):
    return str(text).replace('$','').replace('{','').replace('}','')

'''
使用正则表达式，让字符串保留数字和小数点后两位
'''
def del_string(text):
    x = ''
    for i in str(text):
        if i == '.' or i.isdigit():
            x = x + i
    return round(float(x), 2)

'''
时间格式整理,格式化，去除多余空格处理
'''
def time_formatting(timeFormat,timeValue):
    if len(timeFormat) == 17:
        if timeValue.count(' ') == 1:
            pass
        else:
            x = ''
            newTimeValue = timeValue.replace(' ', '')
            for i in range(len(newTimeValue)):
                if i == 10:
                    x = x + ' ' + newTimeValue[i]
                else:
                    x = x + newTimeValue[i]
            timeValue = x
    else:
        timeValue = timeValue.replace(' ', '')
    return timeValue

'''
时间戳转换成时间
'''
def get_time_value(timeFormat,timeStamp):
    return time.strftime(timeFormat, time.localtime(timeStamp))

'''
时间转换成时间戳
'''
def get_time_stamp(timeFormat,timeValue):
    if timeValue == 'now':
        return time.strftime(timeFormat,time.localtime(time.time()))
    else:
        return int(time.mktime(time.strptime(time_formatting(timeFormat,timeValue),timeFormat)))

'''
校验时间格式
'''
def check_time_format(timeValue):
    if len(str(timeValue).replace(' ','')) == 10:
        return str(timeValue).replace(' ','')
    else:
        raise Exception('加减时间的长度不正确，请输入正确的时间格式！！！（如：yyyy/mm/dd或者yyyy-mm-dd)')

if __name__ == '__main__':
    data = get_variable({'appPackage': 'hkicl.com.hk.fps_merchant', 'appActivity': '.activity.MainActivity'})
    print(data)


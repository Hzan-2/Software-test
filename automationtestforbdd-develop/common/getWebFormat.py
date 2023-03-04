from common.getVarCalcuation import var_calculation
from common.getVariable import is_variable, del_format, get_new_Element


def insert_Step(f,stepsData,Space=''):
    '''
    调取函数写入独立分支操作
    stepsData长度为5的时候，说明只有个分支
    stepsData长度为6的时候，说明需要判断进行哪个分支
    '''
    if len(stepsData) == 5:
        webFormat(f,stepsData[4],Space)
    else:
        webFormat(f,stepsData[4],Space)
        f.write(Space+'else:')
        f.write('\n')
        webFormat(f,stepsData[5],Space)



def var_time_calculation(f,stepsData,Space=''):
    '''
    插入时间计算的步骤，只有加减，（单位：天）
    例：
    2022/07/26 + 2022/07/27 = 2
    2022/07/27 - 2022/07/26 = 1
    2022/07/26 - 1 = 2022/07/25
    2022/07/26 + 1 = 2022/07/27
    '''
    if "+" in stepsData[2]:
        testDataList = str(stepsData[2]).split('+')
        f.write('    ' + Space + 'if '+is_variable(testDataList[0]) +'.replace(" ","").isdigit():')
        f.write('\n')
        # 时间格式为：yyyy-mm-dd
        f.write('        ' + Space + 'if "-" in check_time_format('+is_variable(testDataList[1]) +'):')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = get_time_value("%Y-%m-%d",get_time_stamp("%Y-%m-%d",check_time_format('+is_variable(testDataList[1]) +'))+86400*(int('+is_variable(testDataList[0]) +'.replace(" ",""))))')
        f.write('\n')
        # 时间格式为：yyyy/mm/dd
        f.write('    ' + Space + 'else:')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = get_time_value("%Y/%m/%d",get_time_stamp("%Y/%m/%d",check_time_format('+is_variable(testDataList[1]) +'))+86400*(int('+is_variable(testDataList[0]) +'.replace(" ",""))))')
        f.write('\n')
        f.write('    ' + Space + 'elif '+is_variable(testDataList[1]) +'.replace(" ","").isdigit():')
        f.write('\n')
        # 时间格式为：yyyy-mm-dd
        f.write('        ' + Space + 'if "-" in check_time_format('+is_variable(testDataList[0]) +'):')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = get_time_value("%Y-%m-%d",get_time_stamp("%Y-%m-%d",check_time_format('+is_variable(testDataList[0]) +'))+86400*(int('+is_variable(testDataList[1]) +'.replace(" ",""))))')
        f.write('\n')
        # 时间格式为：yyyy/mm/dd
        f.write('        ' + Space + 'else:')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = get_time_value("%Y/%m/%d",get_time_stamp("%Y/%m/%d",check_time_format('+is_variable(testDataList[0]) +'))+86400*(int('+is_variable(testDataList[1]) +'.replace(" ",""))))')
        f.write('\n')
        f.write('    ' + Space + 'else:')
        f.write('\n')
        # 时间格式为：yyyy-mm-dd + yyyy-mm-dd
        f.write('        ' + Space + 'if "-" in check_time_format('+is_variable(testDataList[0]) +') and  "-" in check_time_format('+is_variable(testDataList[1]) +'):')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = int((get_time_stamp("%Y-%m-%d",check_time_format('+is_variable(testDataList[0]) +')) + get_time_stamp("%Y-%m-%d",check_time_format('+is_variable(testDataList[1]) +')))/86400)')
        f.write('\n')
        # 时间格式为：yyyy/mm/dd + yyyy/mm/dd
        f.write('        ' + Space + 'elif "/" in check_time_format('+is_variable(testDataList[0]) +') and  "/" in check_time_format('+is_variable(testDataList[1]) +'):')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = int((get_time_stamp("%Y/%m/%d",check_time_format('+is_variable(testDataList[0]) +')) + get_time_stamp("%Y/%m/%d",check_time_format('+is_variable(testDataList[1]) +')))/86400)')
        f.write('\n')
        # 时间格式为：yyyy/mm/dd + yyyy-mm-dd
        f.write('        ' + Space + 'elif "/" in check_time_format('+is_variable(testDataList[0]) +') and  "-" in check_time_format('+is_variable(testDataList[1]) +'):')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = int((get_time_stamp("%Y/%m/%d",check_time_format('+is_variable(testDataList[0]) +')) + get_time_stamp("%Y-%m-%d",check_time_format('+is_variable(testDataList[1]) +')))/86400)')
        f.write('\n')
        #时间格式为：yyyy-mm-dd + yyyy/mm/dd
        f.write('        ' + Space + 'else:')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = int((get_time_stamp("%Y-%m-%d",check_time_format('+is_variable(testDataList[0]) +')) + get_time_stamp("%Y/%m/%d",check_time_format('+is_variable(testDataList[1]) +')))/86400)')
        f.write('\n')
    else:
        testDataList = str(stepsData[2]).split('--')
        f.write('    ' + Space + 'if '+is_variable(testDataList[0]) +'.replace(" ","").isdigit():')
        f.write('\n')
        # 时间格式为：yyyy-mm-dd
        f.write('        ' + Space + 'if "-" in check_time_format('+is_variable(testDataList[1]) +'):')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = get_time_value("%Y-%m-%d",get_time_stamp("%Y-%m-%d",check_time_format('+is_variable(testDataList[1]) +'))-86400*(int('+is_variable(testDataList[0]) +'.replace(" ",""))))')
        f.write('\n')
        # 时间格式为：yyyy/mm/dd
        f.write('        ' + Space + 'else:')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = get_time_value("%Y/%m/%d",get_time_stamp("%Y/%m/%d",check_time_format('+is_variable(testDataList[1]) +'))-86400*(int('+is_variable(testDataList[0]) +'.replace(" ",""))))')
        f.write('\n')
        f.write('    ' + Space + 'elif '+is_variable(testDataList[1]) +'.replace(" ","").isdigit():')
        f.write('\n')
        # 时间格式为：yyyy-mm-dd
        f.write('        ' + Space + 'if "-" in check_time_format('+is_variable(testDataList[0]) +'):')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = get_time_value("%Y-%m-%d",get_time_stamp("%Y-%m-%d",check_time_format('+is_variable(testDataList[0]) +'))-86400*(int('+is_variable(testDataList[1]) +'.replace(" ",""))))')
        f.write('\n')
        # 时间格式为：yyyy/mm/dd
        f.write('        ' + Space + 'else:')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = get_time_value("%Y/%m/%d",get_time_stamp("%Y/%m/%d",check_time_format('+is_variable(testDataList[0]) +'))-86400*(int('+is_variable(testDataList[1]) +'.replace(" ",""))))')
        f.write('\n')
        f.write('    ' + Space + 'else:')
        f.write('\n')
        # 时间格式为：yyyy-mm-dd + yyyy-mm-dd
        f.write('        ' + Space + 'if "-" in check_time_format('+is_variable(testDataList[0]) +') and  "-" in check_time_format('+is_variable(testDataList[1]) +'):')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = int((get_time_stamp("%Y-%m-%d",check_time_format('+is_variable(testDataList[0]) +')) - get_time_stamp("%Y-%m-%d",check_time_format('+is_variable(testDataList[1]) +')))/86400)')
        f.write('\n')
        # 时间格式为：yyyy/mm/dd + yyyy/mm/dd
        f.write('        ' + Space + 'elif "/" in check_time_format('+is_variable(testDataList[0]) +') and  "/" in check_time_format('+is_variable(testDataList[1]) +'):')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = int((get_time_stamp("%Y/%m/%d",check_time_format('+is_variable(testDataList[0]) +')) - get_time_stamp("%Y/%m/%d",check_time_format('+is_variable(testDataList[1]) +')))/86400)')
        f.write('\n')
        # 时间格式为：yyyy/mm/dd + yyyy-mm-dd
        f.write('        ' + Space + 'elif "/" in check_time_format('+is_variable(testDataList[0]) +') and  "-" in check_time_format('+is_variable(testDataList[1]) +'):')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = int((get_time_stamp("%Y/%m/%d",check_time_format('+is_variable(testDataList[0]) +')) - get_time_stamp("%Y-%m-%d",check_time_format('+is_variable(testDataList[1]) +')))/86400)')
        f.write('\n')
        #时间格式为：yyyy-mm-dd + yyyy/mm/dd
        f.write('        ' + Space + 'else:')
        f.write('\n')
        f.write('            ' + Space + del_format(stepsData[1]) + ' = int((get_time_stamp("%Y-%m-%d",check_time_format('+is_variable(testDataList[0]) +')) - get_time_stamp("%Y/%m/%d",check_time_format('+is_variable(testDataList[1]) +')))/86400)')
        f.write('\n')

def var_compare(f,stepsData,Space=''):
    try:
        if stepsData[1] == 'None' and '>=' in stepsData[2] or '=>' in stepsData[2]:
            if '>=' in stepsData[2]:
                numList = str(stepsData[2]).split('>=')
            else:
                numList = str(stepsData[2]).split('=>')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",del_string(' + is_variable(numList[0].replace(' ', '')) + '),">=",del_string(' + is_variable(numList[1].replace(' ', '')) + '),"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f, stepsData,Space+'    ')
        elif stepsData[1] == 'None' and '<=' in stepsData[2] or '=<' in stepsData[2]:
            if '<=' in stepsData[2]:
                numList = str(stepsData[2]).split('<=')
            else:
                numList = str(stepsData[2]).split('=<')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",del_string(' + is_variable(numList[0].replace(' ', '')) + '),"=<",del_string(' + is_variable(numList[1].replace(' ', '')) + '),"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f, stepsData,Space+'    ')
        elif stepsData[1] == 'None' and '<' in stepsData[2] and '<=' not in stepsData[2] and '=<' not in stepsData[2]:
            numList = str(stepsData[2]).split('<')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",del_string(' + is_variable(numList[0].replace(' ', '')) + '),"<",del_string(' + is_variable(numList[1].replace(' ', '')) + '),"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f, stepsData,Space+'    ')
        elif stepsData[1] == 'None' and '>' in stepsData[2] and '=>' not in stepsData[2] and '>=' not in stepsData[2]:
            numList = str(stepsData[2]).split('>')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",del_string(' + is_variable(numList[0].replace(' ', '')) + '),">",del_string(' + is_variable(numList[1].replace(' ', '')) + '),"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f, stepsData,Space+'    ')
        elif stepsData[1] == 'None' and '==' in stepsData[2]:
            numList = str(stepsData[2]).split('==')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",' + is_variable(numList[0].replace(' ', '')) + ',"==",' + is_variable(numList[1].replace(' ', '')) + ',"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f, stepsData,Space+'    ')
        elif stepsData[1] == 'None' and '!=' in stepsData[2]:
            numList = str(stepsData[2]).split('!=')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",' + is_variable(numList[0].replace(' ', '')) + ',"!=",' + is_variable(numList[1].replace(' ', '')) + ',"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f, stepsData,Space+'    ')
        elif '%' in stepsData[1]:
            var_compare_time(f,stepsData,Space)
        else:
            numList = str(stepsData[2]).split('=')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",del_string(' + is_variable(numList[0].replace(' ', '')) + '),"=",del_string(' + is_variable(numList[1].replace(' ', '')) + '),"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f, stepsData,Space+'    ')
    except Exception:
        raise Exception('{}为非法的比较方式'.format(stepsData[1]))

def var_compare_time(f,stepsData,Space=''):
    try:
        if '>=' in stepsData[2] or '=>' in stepsData[2]:
            if '>=' in stepsData[2]:
                numList = str(stepsData[2]).split('>=')
            else:
                numList = str(stepsData[2]).split('=>')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",del_string(str(get_time_stamp(get_web_Element_variable("' + stepsData[1] + '",gloVar.project),' + is_variable(numList[0]) + '))),">=",del_string(str(get_time_stamp(get_web_Element_variable("' + stepsData[1] + '",gloVar.project),' + is_variable(numList[1]) + '))),"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f, stepsData,Space+'    ')
        elif '<=' in stepsData[2] or '=<' in stepsData[2]:
            if '<=' in stepsData[2]:
                numList = str(stepsData[2]).split('>=')
            else:
                numList = str(stepsData[2]).split('=<')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",del_string(str(get_time_stamp(get_web_Element_variable("' + stepsData[1] + '",gloVar.project),' + is_variable(numList[0]) + '))),"=<",del_string(str(get_time_stamp(get_web_Element_variable("' + stepsData[1] + '",gloVar.project),' + is_variable(numList[1]) + '))),"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f,stepsData,Space+'    ')
        elif '<' in stepsData[2] and '<=' not in stepsData[2] and '=<' not in stepsData[2]:
            numList = str(stepsData[2]).split('<')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",del_string(str(get_time_stamp(get_web_Element_variable("' + stepsData[1] + '",gloVar.project),' + is_variable(numList[0]) + '))),"<",del_string(str(get_time_stamp(get_web_Element_variable("' + stepsData[1] + '",gloVar.project),' + is_variable(numList[1]) + '))),"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f,stepsData,Space+'    ')
        elif '>' in stepsData[2] and '>=' not in stepsData[2] and '=>' not in stepsData[2]:
            numList = str(stepsData[2]).split('>')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",del_string(str(get_time_stamp(get_web_Element_variable("' + stepsData[1] + '",gloVar.project),' + is_variable(numList[0]) + '))),">",del_string(str(get_time_stamp(get_web_Element_variable("' + stepsData[1] + '",gloVar.project),' + is_variable(numList[1]) + '))),"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f, stepsData,Space+'    ')
        elif '!=' in stepsData[2]:
            numList = str(stepsData[2]).split('>')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",del_string(str(get_time_stamp(get_web_Element_variable("' + stepsData[1] + '",gloVar.project),' + is_variable(numList[0]) + '))),">",del_string(str(get_time_stamp(get_web_Element_variable("' + stepsData[1] + '",gloVar.project),' + is_variable(numList[1]) + '))),"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f,stepsData,Space+'    ')
        else:
            numList = str(stepsData[2]).split('=')
            f.write('    ' + Space + 'if gloVar.browserContext.compareOperation("' + stepsData[0] + '",del_string(str(get_time_stamp(get_web_Element_variable("' + stepsData[1] + '",gloVar.project),' + is_variable(numList[0]) + '))),"=",del_string(str(get_time_stamp(get_web_Element_variable("' + stepsData[1] + '",gloVar.project),' + is_variable(numList[1]) + '))),"比对数据失败截图' + '"):')
            f.write('\n')
            insert_Step(f,stepsData,Space+'    ')
    except Exception:
        raise Exception('{}为非法的比较方式'.format(stepsData[2]))

def webFormat(f,Process,Space):
    for process in Process:
        if 'open' == process[0]:
            f.write('    '+Space+'gloVar.browserContext.openUrlOperation("' + process[0] + '",get_variable("'+process[2]+'",gloVar.project),get_variable("'+process[3]+'",gloVar.project))')
            f.write('\n')
        elif 'click' in process[0] and 'judge' not in process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.clickOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),get_variable("' + process[2] + '",gloVar.project),"点击失败截图' + '")')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
                f.write('    '+Space+'gloVar.browserContext.clickOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),'+is_variable(process[2])+',"点击失败截图' + '")')
                f.write('\n')
        elif 'input' == process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.inputOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),get_variable("'+process[2]+'",gloVar.project),"输入失败截图' + '")')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.inputOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),'+is_variable(process[2])+',"输入失败截图' + '")')
                f.write('\n')
        elif 'get' in process[0] and 'judge' not in process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
                if 'get' == process[0]:
                    f.write('    ' + Space + 'assert gloVar.browserContext.getOperation("' + process[0] + '",get_web_Element_variable("' + get_new_Element(process[1]) + '",gloVar.project),get_variable("'+process[2]+'",gloVar.project),"断言失败截图' + '") is True')
                    f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
                if 'get' == process[0]:
                    f.write('    ' + Space + 'assert gloVar.browserContext.getOperation("' + process[0] + '",get_web_Element_variable("' + get_new_Element(process[1]) + '",gloVar.project),'+is_variable(process[2])+',"断言失败截图' + '") is True')
                    f.write('\n')
            if 'get_text' == process[0]:
                if "$${" in process[1]:
                    var_calculation(f, process, Space)
                else:
                    f.write('    ' + Space + del_format(process[2]) + ' = gloVar.browserContext.getOperation("get",get_web_Element_variable("' + process[1] + '",gloVar.project),"' + str(process[2]) + '","赋值失败截图' + '")')
                    f.write('\n')
            elif 'get_global' == process[0]:
                if "$${" in process[2]:
                    f.write('    ' + Space+'global ' + del_format(process[2]))
                    f.write('\n')
            elif 'get_time' == process[0] and '_' in process[2]:
                f.write('    ' + Space + del_format(process[1]) + ' = gloVar.browserContext.timeOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),"' + str(process[2]) + '","时间赋值失败截图' + '")')
                f.write('\n')
            elif 'get_time' == process[0] and '_' not in process[2]:
                var_time_calculation(f, process, Space)
            elif 'get_' in process[0] and 'get_text' != process[0]:
                f.write('    ' + Space + del_format(process[2]) + ' = gloVar.browserContext.getOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),"' + str(process[2]) + '","赋值失败截图' + '")')
                f.write('\n')
            elif 'captcha' in process[0]:
                f.write('    ' + Space + del_format(process[1]) + ' = driver.captchaOperation("captcha","' + process + '获取验证码失败截图' + '")')
                f.write('\n')
        elif 'sleep' == process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.sleepOperation("' + process[0] + '",get_variable("'+process[2]+'",gloVar.project),"停顿失败截图' + '")')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.sleepOperation("' + process[0] + '",' + is_variable(process[2]) + ',"停顿失败截图' + '")')
                f.write('\n')
        elif 'focus' == process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
            f.write('    ' + Space + 'gloVar.browserContext.focusOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),"聚焦元素失败截图' + '")')
            f.write('\n')
        elif 'iframe' == process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
            f.write('    ' + Space + 'gloVar.browserContext.iframeOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),"切入iframe失败截图' + '")')
            f.write('\n')
        elif 'q_iframe' == process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
            f.write('    ' + Space + 'gloVar.browserContext.q_iframeOperation("' + process[0] + '","退出iframe失败截图' + '")')
            f.write('\n')
        elif 'window' == process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.switch_windowOperation("' + process[0] + '",get_variable("' + process[2] + '",gloVar.project),"切换窗口失败截图' + '")')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.switch_windowOperation("' + process[0] + '",' + is_variable(process[2]) + ',"切换窗口失败截图' + '")')
                f.write('\n')
        elif 'close' == process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
            f.write('    ' + Space + 'gloVar.browserContext.close_windowOperation("' + process[0] + '","关闭窗口失败截图' + '")')
            f.write('\n')
        elif 'keyboard' == process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.keyboardOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),get_variable("' + process[2] + '",gloVar.project),"键盘操作失败截图' + '")')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.keyboardOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),' + is_variable(process[2]) + ',"键盘操作失败截图' + '")')
                f.write('\n')
        elif 'mouse' == process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.mouseOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),get_variable("' + process[2] + '",gloVar.project),"鼠标操作失败截图' + '")')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.mouseOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),' + is_variable(process[2]) + ',"鼠标操作失败截图' + '")')
                f.write('\n')
        elif 'select' == process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.dropDownBoxOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),get_variable("' + process[2] + '",gloVar.project),"select下拉框操作失败截图' + '")')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.dropDownBoxOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),'+is_variable(process[2])+',"select下拉框操作失败截图' + '")')
                f.write('\n')
        elif 'alert' == process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
            f.write('    ' + Space + 'gloVar.browserContext.popupOperation("' + process[0] + '","alert弹窗操作失败截图' + '")')
            f.write('\n')
        elif 'js' == process[0]:
            if '$' in process[3]:
                f.write('    '+Space+'logger.info(get_variable("'+process[3]+'",gloVar.project))')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.jsOperation("' + process[0] + '",get_variable("'+process[2]+'",gloVar.project),"执行js失败截图' + '")')
                f.write('\n')
            else:
                f.write('    '+Space+'logger.info('+is_variable(process[3])+')')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.jsOperation("' + process[0] + '",'+is_variable(process[2])+',"执行js失败截图' + '")')
                f.write('\n')
        elif 'upload' == process[0]:
            if '$' in process[3]:
                f.write('    ' + Space + 'logger.info(get_variable("' + process[3] + '",gloVar.project))')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.uploadOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),get_variable("'+process[2]+'",gloVar.project),"上传文件失败截图' + '")')
                f.write('\n')
            else:
                f.write('    ' + Space + 'logger.info(' + is_variable(process[3]) + ')')
                f.write('\n')
                f.write('    ' + Space + 'gloVar.browserContext.uploadOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),'+is_variable(process[2])+',"上传文件失败截图' + '")')
                f.write('\n')
        elif 'download' == process[0]:
            if '$' in process[3]:
                f.write('    ' + Space + 'logger.info(get_variable("' + process[3] + '",gloVar.project))')
                f.write('\n')
            else:
                f.write('    ' + Space + 'logger.info(' + is_variable(process[3]) + ')')
                f.write('\n')
            f.write('    ' + Space + 'gloVar.browserContext.downloadOperation("' + process[0] + '","上传文件失败截图' + '")')
            f.write('\n')
        elif 'compare' == process[0]:
            if '$' in process[3]:
                f.write('    ' + Space + 'logger.info(get_variable("' + process[3] + '",gloVar.project))')
                f.write('\n')
            else:
                f.write('    ' + Space + 'logger.info(' + is_variable(process[3]) + ')')
                f.write('\n')
            var_compare(f,process,Space)
        elif 'time' in process[0]:
            if '$' in process[3]:
                f.write('    ' + Space + 'logger.info(get_variable("' + process[3] + '",gloVar.project))')
                f.write('\n')
                f.write('    ' + Space + is_variable(process[1]) + '= gloVar.browserContext.timeOperation("' + process[0] + '","' + process[1] + '",get_variable("'+process[2]+'",gloVar.project),"操作时间失败截图' + '")')
                f.write('\n')
            else:
                f.write('    ' + Space + 'logger.info(' + is_variable(process[3]) + ')')
                f.write('\n')
                f.write('    ' + Space + is_variable(process[1]) + '= gloVar.browserContext.timeOperation("' + process[0] + '","' + process[1] + '",'+is_variable(process[2])+',"操作时间失败截图' + '")')
                f.write('\n')
        elif 'file' in process[0]:
            if '$' in process[3]:
                f.write('    ' + Space + 'logger.info(get_variable("' + process[3] + '",gloVar.project))')
                f.write('\n')
                if '_exists' in process[0]:
                    f.write('    ' + Space + 'assert gloVar.browserContext.fileOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),get_variable("' + process[2] + '",gloVar.project),"判断文件失败截图") is True')
                    f.write('\n')
                elif '_excel_color' in process[0]:
                    f.write('    ' + Space + 'assert gloVar.browserContext.fileOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),get_variable("' + process[2] + '",gloVar.project),"判断excel文件表格颜色失败截图") is ' + process[2])
                    f.write('\n')
                elif '_excel_text' in process[0]:
                    f.write('    ' + Space + 'assert gloVar.browserContext.fileOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),get_variable("' + process[2] + '",gloVar.project),"判断excel文件表格文本失败截图") is True')
                    f.write('\n')
            else:
                f.write('    ' + Space + 'logger.info(' + is_variable(process[3]) + ')')
                f.write('\n')
                if '_exists' in process[0]:
                    f.write('    ' + Space + 'assert gloVar.browserContext.fileOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),'+is_variable(process[2])+',"判断文件失败截图") is True')
                    f.write('\n')
                elif '_excel_color' in process[0]:
                    f.write('    ' + Space + 'assert gloVar.browserContext.fileOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),'+is_variable(process[2])+',"判断excel文件表格颜色失败截图") is ' + process[2])
                    f.write('\n')
                elif '_excel_text' in process[0]:
                    f.write('    ' + Space + 'assert gloVar.browserContext.fileOperation("' + process[0] + '",get_web_Element_variable("' + process[1] + '",gloVar.project),'+is_variable(process[2])+',"判断excel文件表格文本失败截图") is True')
                    f.write('\n')
        elif 'loop' == process[0]:
            if '$' in process[3]:
                f.write('    ' + Space + 'logger.info(get_variable("' + process[3] + '",gloVar.project))')
                f.write('\n')
                f.write('    ' + Space + 'while True:')
                f.write('\n')
                f.write('        ' + Space + 'if ' + del_format(process[1]) + ' == get_variable("'+process[2]+'",gloVar.project):')
                f.write('\n')
                f.write('            ' + Space + 'break')
                f.write('\n')
                f.write('        ' + Space + 'else:')
                f.write('\n')
                insert_Step(f, process,'        ' + Space)
            else:
                f.write('    ' + Space + 'logger.info(' + is_variable(process[3]) + ')')
                f.write('\n')
                f.write('    ' + Space + 'while True:')
                f.write('\n')
                f.write('        ' + Space + 'if ' + del_format(process[1]) + ' == '+is_variable(process[2])+':')
                f.write('\n')
                f.write('            ' + Space + 'break')
                f.write('\n')
                f.write('        ' + Space + 'else:')
                f.write('\n')
                insert_Step(f, process,'        ' + Space)
        elif 'judge' == process[0]:
            if '$' in process[3]:
                f.write('    ' + Space + 'logger.info(get_variable("' + process[3] + '",gloVar.project))')
                f.write('\n')
            else:
                f.write('    ' + Space + 'logger.info(' + is_variable(process[3]) + ')')
                f.write('\n')
            f.write('    ' + Space + 'if gloVar.browserContext.judgeOperation("judge",get_web_Element_variable("' + process[1] + '",gloVar.project),"判断失败截图' + '") is ' + process[2] + ':')
            f.write('\n')
            f.write('        ' + Space + 'if ' + process[2] + ' is True:')
            f.write('\n')
            f.write('            ' + Space + 'logger.info("判断"+get_web_Element_variable("' + process[1] + '",gloVar.project)+"元素存在成功！")')
            f.write('\n')
            f.write('        ' + Space + 'else:')
            f.write('\n')
            f.write('            ' + Space + 'logger.info("判断"+get_web_Element_variable("' + process[1] + '",gloVar.project)+"元素不存在成功！")')
            f.write('\n')
            f.write('    ' + Space + 'else:')
            f.write('\n')
            f.write('        ' + Space + 'raise Exception("判断"+get_web_Element_variable("' + process[1] + '",gloVar.project)+"元素不满足条件，用例终止！")')
            f.write('\n')
        elif 'judge' in process[0] and 'judge' != process[0]:
            if '$' in process[3]:
                f.write('    ' + Space + 'logger.info(get_variable("' + process[3] + '",gloVar.project))')
                f.write('\n')
                f.write('    ' + Space + 'if gloVar.browserContext.judgeOperation("judge",get_web_Element_variable("' + process[1] + '",gloVar.project),"判断失败截图' + '"):')
                f.write('\n')
                if 'click' in process[0]:
                    f.write('        ' + Space + 'gloVar.browserContext.clickOperation("click",get_web_Element_variable("' +process[1] + '",gloVar.project),get_variable("'+process[2]+'",gloVar.project),"点击失败截图' + '")')
                    f.write('\n')
                elif 'input' in process[0]:
                    f.write('        ' + Space + 'gloVar.browserContext.inputOperation("input",get_web_Element_variable("' +process[1] + '",gloVar.project),get_variable("'+process[2]+'",gloVar.project),"输入失败截图' + '")')
                    f.write('\n')
                elif 'branch' in process[0]:
                    insert_Step(f, process,'    ' + Space)
            else:
                f.write('    ' + Space + 'logger.info(' + is_variable(process[3]) + ')')
                f.write('\n')
                f.write('    ' + Space + 'if gloVar.browserContext.judgeOperation("judge",get_web_Element_variable("' + process[1] + '",gloVar.project),"判断失败截图' + '"):')
                f.write('\n')
                if 'click' in process[0]:
                    f.write('        ' + Space + 'gloVar.browserContext.clickOperation("click",get_web_Element_variable("' +process[1] + '",gloVar.project),'+is_variable(process[2])+',"点击失败截图' + '")')
                    f.write('\n')
                elif 'input' in process[0]:
                    f.write('        ' + Space + 'gloVar.browserContext.inputOperation("input",get_web_Element_variable("' +process[1] + '",gloVar.project),'+is_variable(process[2])+',"输入失败截图' + '")')
                    f.write('\n')
                elif 'branch' in process[0]:
                    insert_Step(f, process,'    ' + Space)
        else:
            raise Exception('不存在该{}的Action，请检查！'.format(process[0]))

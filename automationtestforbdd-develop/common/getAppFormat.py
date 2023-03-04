from common.getVarCalcuation import var_calculation
from common.getVariable import del_format, is_variable, get_new_Element


def insert_Step(f,stepsData,Space=''):
    '''
    调取函数写入独立分支操作
    stepsData长度为5的时候，说明只有个分支
    stepsData长度为6的时候，说明需要判断进行哪个分支
    '''
    if len(stepsData) == 5:
        appFormat(f,stepsData[4],Space)
    else:
        appFormat(f,stepsData[4],Space)
        f.write(Space+'else:')
        f.write('\n')
        appFormat(f,stepsData[5],Space)

def var_compare(f, stepsData,Space=''):
    if '>=' in stepsData[2] or '=>' in stepsData[2]:
        if '>=' in stepsData[2]:
            numList = str(stepsData[2]).split('>=')
        else:
            numList = str(stepsData[2]).split('=>')
        f.write('    ' + Space + 'if gloVar.driverContext.compareOperation("' + stepsData[0] + '",del_string(' + is_variable(numList[0].replace(' ', '')) + '),">=",del_string(' + is_variable(numList[1].replace(' ', '')) + '),"比对数据失败截图' + '"):')
        f.write('\n')
        insert_Step(f,stepsData,Space+'    ')
    elif '<=' in stepsData[2] or '=<' in stepsData[2]:
        if '<=' in stepsData[2]:
            numList = str(stepsData[2]).split('<=')
        else:
            numList = str(stepsData[2]).split('=<')
        f.write('    ' + Space + 'if gloVar.driverContext.compareOperation("' + stepsData[0] + '",del_string(' + is_variable(numList[0].replace(' ', '')) + '),"=<",del_string(' + is_variable(numList[1].replace(' ', '')) + '),"比对数据失败截图' + '"):')
        f.write('\n')
        insert_Step(f,stepsData,Space+'    ')
    elif '<' in stepsData[2] and '<=' not in stepsData[2] and '=<' not in stepsData[2]:
        numList = str(stepsData[2]).split('<')
        f.write('    ' + Space + 'if gloVar.driverContext.compareOperation("' + stepsData[0] + '",del_string(' + is_variable(numList[0].replace(' ', '')) + '),"<",del_string(' + is_variable(numList[1].replace(' ', '')) + '),"比对数据失败截图' + '"):')
        f.write('\n')
        insert_Step(f,stepsData,Space+'    ')
    elif '>' in stepsData[2] and '=>' not in stepsData[2] and '>=' not in stepsData[2]:
        numList = str(stepsData[2]).split('>')
        f.write('    ' + Space + 'if gloVar.driverContext.compareOperation("' + stepsData[0] + '",del_string(' + is_variable(numList[0].replace(' ', '')) + '),">",del_string(' + is_variable(numList[1].replace(' ', '')) + '),"比对数据失败截图' + '"):')
        f.write('\n')
        insert_Step(f,stepsData,Space+'    ')
    elif '==' in stepsData[2]:
        numList = str(stepsData[2]).split('==')
        f.write('    ' + Space + 'if gloVar.driverContext.compareOperation("' + stepsData[0] + '",' + is_variable(numList[0].replace(' ', '')) + ',"==",' + is_variable(numList[1].replace(' ', '')) + ',"比对数据失败截图' + '"):')
        f.write('\n')
        insert_Step(f,stepsData,Space+'    ')
    elif '!=' in stepsData[2]:
        numList = str(stepsData[2]).split('!=')
        f.write('    ' + Space + 'if gloVar.driverContext.compareOperation("' + stepsData[0] + '",' + is_variable(numList[0].replace(' ', '')) + ',"!=",' + is_variable(numList[1].replace(' ', '')) + ',"比对数据失败截图' + '"):')
        f.write('\n')
        insert_Step(f,stepsData,Space+'    ')
    elif 'similar' in stepsData[1]:
        f.write('    ' + Space + 'if gloVar.driverContext.compareOperation("' + stepsData[0] + '",' + is_variable(stepsData[2]) + ',"similar","","比对图像失败截图' + '"):')
        f.write('\n')
        insert_Step(f,stepsData,Space+'    ')
    else:
        numList = str(stepsData[2]).split('=')
        f.write('    ' + Space + 'if gloVar.driverContext.compareOperation("' + stepsData[0] + '",del_string(' + is_variable(numList[0].replace(' ', '')) + '),"=",del_string(' + is_variable(numList[1].replace(' ', '')) + '),"比对数据失败截图' + '"):')
        f.write('\n')
        insert_Step(f,stepsData,Space+'    ')

def appFormat(f,Process,Space,page=None):
    for process in Process:
        if 'click' in process[0] and 'judge' not in process[0] and 'Element_' not in process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+Space+'gloVar.driverContext.clickOperation("' + process[0] + '",get_App_Element_variable("'+process[1]+'",gloVar.platformName,"'+str(page)+'",gloVar.language),'+ is_variable(process[2]) +',"点击失败截图")')
            f.write('\n')
        elif 'input' == process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+Space+'gloVar.driverContext.inputOperation("' + process[0] + '",get_App_Element_variable("'+process[1]+'",gloVar.platformName,"'+str(page)+'",gloVar.language),' + is_variable(process[2]) + ',"输入失败截图")')
            f.write('\n')
        elif 'get' in process[0] and 'judge' not in process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            if 'get' == process[0]:
                f.write('    '+Space+'assert gloVar.driverContext.getOperation("' + process[0] + '",get_App_Element_variable("'+get_new_Element(process[1])+'",gloVar.platformName,"'+str(page)+'",gloVar.language),' + is_variable(process[2]) + ',"断言失败截图") is True')
                f.write('\n')
            elif 'get_text' == process[0]:
                if "$${" in process[1]:
                    var_calculation(f,process,Space)
                else:
                    f.write('    '+Space+''+del_format(process[2])+' = gloVar.driverContext.getOperation("get",get_App_Element_variable("'+process[1]+'",gloVar.platformName,"'+str(page)+'",gloVar.language),"' + str(process[2]) + '","赋值失败截图")')
                    f.write('\n')
            elif 'get_split_' in process[0]:
                f.write('    ' + Space + '' + del_format(process[1]) + ' = ' + del_format(process[1]) + '.split('+ is_variable(process[2]) +')[' + str(process[0]).split('_')[-1] + '-1]')
                f.write('\n')
                f.write('    ' + Space + 'logger.info("变量'+ del_format(process[1]) +'获取到切割的值为:{}".format(' + del_format(process[1]) + '))')
                f.write('\n')
            elif 'get_global' == process[0]:
                if "$${" in process[2]:
                    f.write('    '+Space+'global '+del_format(process[2]))
                    f.write('\n')
        elif 'slide' in process[0] and 'judge' not in process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+Space+'gloVar.driverContext.slideOperation("' + process[0] + '",get_App_Element_variable("'+process[1]+'",gloVar.platformName,"'+str(page)+'",gloVar.language),' + is_variable(process[2]) + ',"滑动失败截图")')
            f.write('\n')
        elif 'keyboard' == process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+Space+'gloVar.driverContext.keyboardOperation("' + process[0] + '",' + is_variable(process[2]) + ',"键盘敲击失败截图",gloVar.platformName)')
            f.write('\n')
        elif 'backHome' == process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+Space+'gloVar.driverContext.backElementPageOperation("' + process[0] + '",[get_App_Element_variable("${HomePage}${greetingsElement}",gloVar.platformName,"'+str(page)+'",gloVar.language),get_App_Element_variable("${HomePage}${underHomeButtonElement}",gloVar.platformName,"'+str(page)+'",gloVar.language)],"返回首页失败截图")')
            f.write('\n')
        elif 'sleep' == process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+Space+'gloVar.driverContext.sleepOperation("sleep",' + is_variable(process[2]) + ',"停顿"+' + is_variable(process[2]) + '+"秒")')
            f.write('\n')
        elif 'sotfToken_input' == process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+Space+'gloVar.driverContext.sotfTokenOperation("' + process[0] + '",' + is_variable(process[2]) + ',"返回首页失败截图",gloVar.platformName)')
            f.write('\n')
        elif 'start_app' == process[0]:
            f.write('    ' + Space + 'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    ' + Space + 'gloVar.driverContext.startAppOperation("' + process[0] + '",get_variable(' + process[2] + '),"启动app失败截图")')
            f.write('\n')
        elif 'switch_app' == process[0]:
            f.write('    ' + Space + 'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    ' + Space + 'gloVar.driverContext.switchAppOperation("' + process[0] + '",' + is_variable(process[2]) + ',"切换app失败截图")')
            f.write('\n')
        elif 'find' in process[0] and 'judge' not in process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+ Space + del_format(process[1]) + ' = gloVar.driverContext.findTextOperation("' + process[0] + '",' + is_variable(process[2]) + ',"找文本失败截图' + '")')
            f.write('\n')
        elif 'compare' == process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            var_compare(f, process,Space)
        elif 'language' == process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+Space+'if gloVar.language == "'+ process[2] +'":')
            f.write('\n')
            insert_Step(f, process,'    '+Space)
        elif 'empowerment' == process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+Space+'gloVar.driverContext.initializationApp(' + process[2]+')')
            f.write('\n')
        elif 'loop' == process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+Space+'while True:')
            f.write('\n')
            f.write('        '+Space+'if '+del_format(process[1])+' == '+ is_variable(process[2]) +':')
            f.write('\n')
            f.write('            '+Space+'break')
            f.write('\n')
            f.write('        '+Space+'else:')
            f.write('\n')
            insert_Step(f, process,'        '+Space)
        elif 'Element_' in process[0] and 'judge' not in process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    ' + Space + 'if gloVar.driverContext.attributeOperation("attribute",get_App_Element_variable("' + process[1] + '",gloVar.platformName,"' + str(page) + '",gloVar.language),"' + process[0].split('_')[1] + '","元素属性判断失败截图") is ' + process[2] + ':')
            f.write('\n')
            f.write('        ' + Space + 'if '+process[2]+' is True:')
            f.write('\n')
            f.write('            ' + Space + 'logger.info("判断"+get_App_Element_variable("' + process[1] + '",gloVar.platformName,"' + str(page) + '",gloVar.language)+"元素属性为True成功！")')
            f.write('\n')
            f.write('        ' + Space + 'else:')
            f.write('\n')
            f.write('            ' + Space + 'logger.info("判断"+get_App_Element_variable("' + process[1] + '",gloVar.platformName,"' + str(page) + '",gloVar.language)+"元素属性为False成功！")')
            f.write('\n')
            f.write('    ' + Space + 'else:')
            f.write('\n')
            f.write('        ' + Space + 'raise Exception("判断"+get_App_Element_variable("'+process[1]+'",gloVar.platformName,"'+str(page)+'",gloVar.language)+"元素属性不满足条件，用例终止！")')
            f.write('\n')
        elif 'judge' == process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+Space+'if gloVar.driverContext.judgeOperation("judge",get_App_Element_variable("'+process[1]+'",gloVar.platformName,"'+str(page)+'",gloVar.language)' + ',"判断失败截图' + '") is ' + process[2] + ':')
            f.write('\n')
            f.write('        '+Space+'if '+process[2]+' is True:')
            f.write('\n')
            f.write('            '+Space+'logger.info("判断"+get_App_Element_variable("' + process[1] + '",gloVar.platformName,"' + str(page) + '",gloVar.language)+"元素存在成功！")')
            f.write('\n')
            f.write('        '+Space+'else:')
            f.write('\n')
            f.write('            '+Space+'logger.info("判断"+get_App_Element_variable("' + process[1] + '",gloVar.platformName,"' + str(page) + '",gloVar.language)+"元素不存在成功！")')
            f.write('\n')
            f.write('    '+Space+'else:')
            f.write('\n')
            f.write('        '+Space+'raise Exception("判断"+get_App_Element_variable("'+process[1]+'",gloVar.platformName,"'+str(page)+'",gloVar.language)+"元素不满足条件，用例终止！")')
            f.write('\n')
        elif 'judge' in process[0] and 'judge' != process[0]:
            f.write('    '+Space+'logger.info(' + is_variable(process[3]) + ')')
            f.write('\n')
            f.write('    '+Space+'if gloVar.driverContext.judgeOperation("judge",get_App_Element_variable("'+process[1]+'",gloVar.platformName,"'+str(page)+'",gloVar.language)' + ',"判断失败截图' + '"):')
            f.write('\n')
            if 'click' in process[0]:
                f.write('        '+Space+'gloVar.driverContext.clickOperation("'+ process[0].split(',')[1] +'",get_App_Element_variable("'+process[1]+'",gloVar.platformName,"'+str(page)+'",gloVar.language),' + is_variable(process[2]) + ',"点击失败截图")')
                f.write('\n')
            elif 'input' in process[0]:
                f.write('        '+Space+'gloVar.driverContext.inputOperation("input",get_App_Element_variable("'+process[1]+'",gloVar.platformName,"'+str(page)+'",gloVar.language),' + is_variable(process[2]) + ',"输入失败截图' + '")')
                f.write('\n')
            elif 'get' in process[0]:
                if 'get' == process[0]:
                    f.write('        '+Space+'assert gloVar.driverContext.getOperation("get",get_App_Element_variable("'+get_new_Element(process[1])+'",gloVar.platformName,"'+str(page)+'",gloVar.language),' + is_variable(process[2]) + ',"断言失败截图' + '") is True')
                    f.write('\n')
                elif 'get_text' == process[0]:
                    if "$${" in process[1]:
                        var_calculation(f, process)
                    else:
                        f.write('        '+Space+'' + del_format(process[2]) + ' = gloVar.driverContext.getOperation("get",get_App_Element_variable("' + process[1] + '",gloVar.platformName,"' + str(page) + '",gloVar.language),"' + str(process[2]) + '","赋值失败截图' + '")')
                        f.write('\n')
                elif 'get_split_' in process[0]:
                    f.write('        ' + Space + '' + del_format(process[1]) + ' = ' + del_format(process[1]) + '.split(' + is_variable(process[2]) + ')[' + str(process[0]).split('_')[-1] + '-1]')
                    f.write('\n')
                    f.write('        ' + Space + 'logger.info("变量' + del_format(process[1]) + '获取到切割的值为:{}".format(' + del_format(process[1]) + '))')
                    f.write('\n')
            elif 'keyboard' in process[0]:
                f.write('        '+Space+'gloVar.driverContext.keyboardOperation("keyboard",' + is_variable(process[2]) + ',"键盘敲击失败截图' + '",gloVar.platformName)')
                f.write('\n')
            elif 'backHome' == process[0]:
                f.write('        '+Space+'gloVar.driverContext.backElementPageOperation("backHome",[get_App_Element_variable("${HomePage}${greetingsElement}",gloVar.platformName,"' + str(page) + '",gloVar.language),get_App_Element_variable("${HomePage}${underHomeButtonElement}",gloVar.platformName,"' + str(page) + '",gloVar.language)],"返回首页失败截图' + '")')
                f.write('\n')
            elif 'sotfToken_input' == process[0]:
                f.write('        '+Space+'gloVar.driverContext.sotfTokenOperation("sotfToken_input",' + is_variable(process[2]) + ',"返回首页失败截图' + '",gloVar.platformName)')
                f.write('\n')
            elif 'find' in process[0]:
                f.write('        '+Space+del_format(process[1]) + ' = gloVar.driverContext.findTextOperation("' + process[0] + '",' + is_variable(process[2]) + ',"找文本失败截图' + '")')
                f.write('\n')
            elif 'compare' == process[0]:
                var_compare(f, process, '    '+Space)
            elif 'language' == process[0]:
                f.write('        ' + Space + 'if gloVar.language == "' + process[2] + '":')
                f.write('\n')
                insert_Step(f, process, '    '+Space)
            elif 'loop' == process[0]:
                f.write('            '+Space+'while True:')
                f.write('\n')
                f.write('                '+Space+'if ' + del_format(process[1]) + ' == ' + is_variable(process[2]) + ':')
                f.write('\n')
                f.write('                    '+Space+'break')
                f.write('\n')
                f.write('                '+Space+'else:')
                f.write('\n')
                insert_Step(f, process, '        '+Space)
            elif 'branch' in process[0]:
                insert_Step(f,process,Space+'    ')
            elif 'Element_' in process[0]:
                f.write('        '+Space+'if gloVar.driverContext.attributeOperation("attribute",get_App_Element_variable("'+process[1]+'",gloVar.platformName,"'+str(page)+'",gloVar.language),"' + process[0].split('_')[1] + '","元素属性判断失败截图' + '") is ' + process[2] + ':')
                f.write('\n')
                insert_Step(f,process,'        '+Space)
            elif 'platform' in process[0]:
                f.write('        '+Space+'pass')
                f.write('\n')
                f.write('    '+Space+'if gloVar.platformName.lower() == "'+ str(process[2]).lower() +'":')
                f.write('\n')
                insert_Step(f,process,'    '+Space)
        else:
            raise Exception('不存在该{}的Action，请检查！'.format(process[0]))
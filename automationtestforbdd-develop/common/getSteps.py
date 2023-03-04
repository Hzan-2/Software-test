def get_step_4(steps):
    '''
    Parameters
    长度为4的步骤，无分支，添加进list
    stepList：当前list的对象
    steps：当前步骤对象

    Returns
    将添加进list的内容，再返回
    '''
    stepList = []
    stepList.append(str(steps['Action']))
    stepList.append(str(steps['Element']))
    stepList.append(str(steps['TestData']))
    stepList.append(str(steps['Remarks']))
    return stepList

def get_step_5(steps,type):
    '''
    Parameters
    长度为5的步骤，含有独立分支，添加进list
    stepList：当前list的对象
    steps：当前步骤对象

    Returns
    将添加进list的内容，再返回
    '''
    stepList = []
    stepList.append(str(steps['Action']))
    stepList.append(str(steps['Element']))
    stepList.append(str(steps['TestData']))
    stepList.append(str(steps['Remarks']))
    branchProcessList = []
    if type == 'dict':
        for Step in steps['branchProcess']:
            if len(steps['branchProcess'][Step]) == 4:
                branchProcessList.append(get_step_4(steps['branchProcess'][Step]))
            elif len(steps['branchProcess'][Step]) == 5:
                branchProcessList.append(get_step_5(steps['branchProcess'][Step],type))
            else:
                branchProcessList.append(get_step_6(steps['branchProcess'][Step],type))
        stepList.append(branchProcessList)
    else:
        for Step in steps['branchProcess']:
            if len(Step) == 4:
                branchProcessList.append(get_step_4(Step))
            elif len(Step) == 5:
                branchProcessList.append(get_step_5(Step,type))
            else:
                branchProcessList.append(get_step_6(Step,type))
        stepList.append(branchProcessList)
    return stepList

def get_step_6(steps,type):
    '''
    Parameters
    长度为6的步骤，含有多分支，添加进list
    stepList：当前list的对象
    steps：当前步骤对象

    Returns
    将添加进list的内容，再返回
    '''
    stepList = []
    stepList.append(str(steps['Action']))
    stepList.append(str(steps['Element']))
    stepList.append(str(steps['TestData']))
    stepList.append(str(steps['Remarks']))
    ifbranchProcessList = []
    elsebranchProcessList = []
    if type == 'dict':
        for Step in steps['ifbranchProcess']:
            if len(steps['ifbranchProcess'][Step]) == 4:
                ifbranchProcessList.append(get_step_4(steps['ifbranchProcess'][Step]))
            elif len(steps['ifbranchProcess'][Step]) == 5:
                ifbranchProcessList.append(get_step_5(steps['ifbranchProcess'][Step],type))
            else:
                ifbranchProcessList.append(get_step_6(steps['ifbranchProcess'][Step],type))
        stepList.append(ifbranchProcessList)
        for Step in steps['elsebranchProcess']:
            if len(steps['elsebranchProcess'][Step]) == 4:
                elsebranchProcessList.append(get_step_4(steps['elsebranchProcess'][Step]))
            elif len(steps['elsebranchProcess'][Step]) == 5:
                elsebranchProcessList.append(get_step_5(steps['elsebranchProcess'][Step],type))
            else:
                elsebranchProcessList.append(get_step_6(steps['elsebranchProcess'][Step],type))
        stepList.append(elsebranchProcessList)
    else:
        for Step in steps['ifbranchProcess']:
            if len(Step) == 4:
                ifbranchProcessList.append(get_step_4(Step))
            elif len(Step) == 5:
                ifbranchProcessList.append(get_step_5(Step,type))
            else:
                ifbranchProcessList.append(get_step_6(Step,type))
        stepList.append(ifbranchProcessList)
        for Step in steps['elsebranchProcess']:
            if len(Step) == 4:
                elsebranchProcessList.append(get_step_4(Step))
            elif len(Step) == 5:
                elsebranchProcessList.append(get_step_5(Step,type))
            else:
                elsebranchProcessList.append(get_step_6(Step,type))
        stepList.append(elsebranchProcessList)
    return stepList

def get_steps(steps):
    '''
    获取yaml案例的步骤，并进行字段归类
    '''
    stepsList = []
    if 'dict' in str(type(steps)):
        for step in steps:
            if len(steps[step]) == 4:
                stepsList.append(get_step_4(steps[step]))
            elif len(steps[step]) == 5:
                stepsList.append(get_step_5(steps[step],'dict'))
            else:
                stepsList.append(get_step_6(steps[step],'dict'))
    else:
        for step in steps:
            if len(step) == 4:
                stepsList.append(get_step_4(step))
            elif len(step) == 5:
                stepsList.append(get_step_5(step,'list'))
            else:
                stepsList.append(get_step_6(step,'list'))
    return stepsList
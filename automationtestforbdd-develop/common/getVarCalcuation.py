from common.getVariable import del_format, is_variable

'''
插入参数计算的步骤
'''
def var_calculation(f,stepsData,Space=''):
    if "+" in stepsData[2] or ("-" in stepsData[2] and stepsData[2].count("-") == 1) or "*" in stepsData[2] or ("/" in stepsData[2] and stepsData[2].count("/") == 1):
        if "+" in stepsData[2]:
            numList = stepsData[2].split("+")
            f.write('    ' + Space + del_format(stepsData[1]) + ' = str(Decimal(del_string(' + is_variable(numList[0]).replace(' ','') + '))+Decimal(del_string(' + is_variable(numList[1]).replace(' ', '') + ')))')
            f.write('\n')
        elif "-" in stepsData[2]:
            numList = stepsData[2].split("-")
            f.write('    ' + Space + del_format(stepsData[1]) + ' = str(Decimal(del_string(' + is_variable(numList[0]).replace(' ','') + '))-Decimal(del_string(' + is_variable(numList[1]).replace(' ', '') + ')))')
            f.write('\n')
        elif "*" in stepsData[2]:
            numList = stepsData[2].split("*")
            f.write('    ' + Space + del_format(stepsData[1]) + ' = str(Decimal(del_string(' + is_variable(numList[0]).replace(' ','') + '))*Decimal(del_string(' + is_variable(numList[1]).replace(' ', '') + ')))')
            f.write('\n')
        else:
            numList = stepsData[2].split("/")
            f.write('    ' + Space + del_format(stepsData[1]) + ' = str(Decimal(del_string(' + is_variable(numList[0]).replace(' ','') + '))/Decimal(del_string(' + is_variable(numList[1]).replace(' ', '') + ')))')
            f.write('\n')
    else:
        f.write('    ' + Space + del_format(stepsData[1]) + ' = ' + is_variable(stepsData[2]))
        f.write('\n')

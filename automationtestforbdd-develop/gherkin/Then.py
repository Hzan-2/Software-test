'''
填充Than段落的steps
'''
from common.getAppFormat import appFormat
from common.getWebFormat import webFormat
from common.getSteps import get_steps


def fill_Then_Paragraph(f,paragraph):
    f.write('@then("'+paragraph['Text']+'")')
    f.write('\n')
    var = ''
    if paragraph['Text'].count('{') >= 1:
        for i in paragraph['Text'].split('{'):
            if '}' in i:
                var = var + ',' + i.split('}')[0]
        f.write('def step_impl(context'+ var +'):')
        f.write('\n')
    else:
        f.write('def step_impl(context):')
        f.write('\n')
    if paragraph['Fixture'].lower() == 'app':
        appFormat(f, get_steps(paragraph['Process']), '')
    else:
        webFormat(f, get_steps(paragraph['Process']), '')

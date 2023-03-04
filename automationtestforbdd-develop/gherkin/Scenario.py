from gherkin.And import fill_And_Paragraph
from gherkin.Given import fill_Given_Paragraph
from gherkin.Quit import fill_Quit_Paragraph
from gherkin.Then import fill_Then_Paragraph
from gherkin.When import fill_When_Paragraph

'''
获取到场景段落
'''
def get_Scenario_Paragraph(f,ScenarioList):
    for Scenario in ScenarioList:
        if Scenario['Step'] == 'Given':
            fill_Given_Paragraph(f,Scenario)
        elif Scenario['Step'] == 'Then':
            fill_Then_Paragraph(f,Scenario)
        elif Scenario['Step'] == 'When':
            fill_When_Paragraph(f,Scenario)
        elif Scenario['Step'] == 'And':
            fill_And_Paragraph(f,Scenario)
        else:
            fill_Quit_Paragraph(f)


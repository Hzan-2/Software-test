from config.Config import PROJECT_FILE


def updata_project(project,type):
    with open(PROJECT_FILE,'w',encoding="utf-8") as f:
        f.write('PROJECT = "'+ project +'"')
        f.write('\n')
        f.write('ISYAML = "' + type + '"')
        f.write('\n')



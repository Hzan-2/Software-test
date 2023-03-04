from common.getFeatureExample import *
from common.getYamlExample import *
from config.Config import *


def create_project(project,type):
    if not os.path.exists(HTMLREPORT_PATH):
        os.makedirs(HTMLREPORT_PATH)
    if not os.path.exists(REPORT_PATH):
        os.makedirs(REPORT_PATH)
    if not os.path.exists(SCREENSHOTS_PATH):
        os.makedirs(SCREENSHOTS_PATH)
    if not os.path.exists(VIDEO_PATH):
        os.makedirs(VIDEO_PATH)
    if not os.path.exists(DOWNLOAD_FILE):
        os.makedirs(DOWNLOAD_FILE)
    if not os.path.exists(UPLOAD_FILE):
        os.makedirs(UPLOAD_FILE)
    if type == 'yaml':
        if os.path.exists(os.path.join(BASE_PATH,'featuresYaml',project)):
            print('featureYaml文件夹，已存在{}该项目，请忽重新创建！'.format(project))
        else:
            #创建项目文件夹
            os.makedirs(os.path.join(BASE_PATH,'featuresYaml',project))
            os.makedirs(os.path.join(BASE_PATH,'featuresYaml',project,'data'))
            os.makedirs(os.path.join(BASE_PATH,'featuresYaml',project,'elementData'))
            os.makedirs(os.path.join(BASE_PATH,'featuresYaml',project,'steps'))
            os.makedirs(os.path.join(BASE_PATH,'featuresYaml',project,'yaml'))
            #创建data目录下的api、app、web三个文件夹
            os.makedirs(os.path.join(BASE_PATH,'featuresYaml',project,'data','api'))
            os.makedirs(os.path.join(BASE_PATH,'featuresYaml',project,'data','app'))
            os.makedirs(os.path.join(BASE_PATH,'featuresYaml',project,'data','web'))
            #创建elementData目录下的AppElementData、WebElementData三个文件夹
            os.makedirs(os.path.join(BASE_PATH,'featuresYaml',project,'elementData','AppElementData'))
            os.makedirs(os.path.join(BASE_PATH,'featuresYaml',project,'elementData','WebElementData'))
            #创建文件夹下的yaml示例
            get_yaml_example_of_app(os.path.join(BASE_PATH,'featuresYaml',project,'data','app'))
            get_yaml_example_of_web(os.path.join(BASE_PATH,'featuresYaml',project,'data','web'))
            get_yaml_example_of_app_element(os.path.join(BASE_PATH,'featuresYaml',project,'elementData','AppElementData'))
            get_yaml_example_of_web_element(os.path.join(BASE_PATH,'featuresYaml',project,'elementData','WebElementData'))
            get_yaml_example_of_gherkin(os.path.join(BASE_PATH,'featuresYaml',project,'yaml'))
            #创建文件夹下feature示例
            get_feature_app_case_example(os.path.join(BASE_PATH,'featuresYaml',project))
            get_feature_first_app_case_example(os.path.join(BASE_PATH,'featuresYaml',project))
            get_feature_web_case_example(os.path.join(BASE_PATH,'featuresYaml',project))
            get_feature_web_and_app_case_example(os.path.join(BASE_PATH,'featuresYaml',project))
            get_feature_web_and_first_app_case_example(os.path.join(BASE_PATH,'featuresYaml',project))
    else:
        if os.path.exists(os.path.join(BASE_PATH,'features',project)):
            print('feature文件夹，已存在{}该项目，请忽重新创建！'.format(project))
        else:
            os.makedirs(os.path.join(BASE_PATH,'features',project))
            os.makedirs(os.path.join(BASE_PATH,'features',project,'data'))
            os.makedirs(os.path.join(BASE_PATH,'features',project,'elementData'))
            os.makedirs(os.path.join(BASE_PATH,'features',project,'steps'))
            #创建data目录下的api、app、web三个文件夹
            os.makedirs(os.path.join(BASE_PATH,'features',project,'data','api'))
            os.makedirs(os.path.join(BASE_PATH,'features',project,'data','app'))
            os.makedirs(os.path.join(BASE_PATH,'features',project,'data','web'))
            #创建elementData目录下的AppElementData、WebElementData三个文件夹
            os.makedirs(os.path.join(BASE_PATH,'features',project,'elementData','AppElementData'))
            os.makedirs(os.path.join(BASE_PATH,'features',project,'elementData','WebElementData'))
            #创建文件夹下的yaml示例
            get_yaml_example_of_app(os.path.join(BASE_PATH,'features',project,'data','app'))
            get_yaml_example_of_web(os.path.join(BASE_PATH,'features',project,'data','web'))
            get_yaml_example_of_app_element(os.path.join(BASE_PATH,'features',project,'elementData','AppElementData'))
            get_yaml_example_of_web_element(os.path.join(BASE_PATH,'features',project,'elementData','WebElementData'))
            #创建文件夹下feature示例
            get_feature_app_case_example(os.path.join(BASE_PATH,'features',project))
            get_feature_first_app_case_example(os.path.join(BASE_PATH,'features',project))
            get_feature_web_case_example(os.path.join(BASE_PATH,'features',project))
            get_feature_web_and_app_case_example(os.path.join(BASE_PATH,'features',project))
            get_feature_web_and_first_app_case_example(os.path.join(BASE_PATH,'features',project))

if __name__ == '__main__':
    type = input("请输入你要创建的项目类型：")
    project = input("请输入你要创建的项目名称：")
    create_project(project,type)
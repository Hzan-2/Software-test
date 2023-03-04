import os

#App装置的feature案例
def get_feature_app_case_example(path):
    with open(os.path.join(path, 'AppCase.feature'), 'w', encoding="utf-8") as f:
        f.write("Feature: 启动app并登录")
        f.write('\n')
        f.write("    Background: 你要启动什么装置来执行场景呢？")
        f.write('\n')
        f.write("        Given 我启动了app装置")
        f.write('\n')
        f.write("    Scenario: 我是场景的描述说明")
        f.write('\n')
        f.write("        Given 我是Given的描述说明")
        f.write('\n')
        f.write("        When 我是When的描述说明")
        f.write('\n')
        f.write("        And 我是And的描述说明")
        f.write('\n')
        f.write("        Then 我是Then的描述说明")
        f.write('\n')

#第一次打开App装置的feature案例
def get_feature_first_app_case_example(path):
    with open(os.path.join(path, 'FirstAppCase.feature'), 'w', encoding="utf-8") as f:
        f.write("Feature: 启动app并登录")
        f.write('\n')
        f.write("    Background: 你要启动什么装置来执行场景呢？")
        f.write('\n')
        f.write("        Given 我启动了app装置,并且第一次打开app")
        f.write('\n')
        f.write("    Scenario: 我是场景的描述说明")
        f.write('\n')
        f.write("        Given 我是Given的描述说明")
        f.write('\n')
        f.write("        When 我是When的描述说明")
        f.write('\n')
        f.write("        And 我是And的描述说明")
        f.write('\n')
        f.write("        Then 我是Then的描述说明")
        f.write('\n')

#Web装置的feature案例
def get_feature_web_case_example(path):
    with open(os.path.join(path, 'WebCase.feature'), 'w', encoding="utf-8") as f:
        f.write("Feature: 启动app并登录")
        f.write('\n')
        f.write("    Background: 你要启动什么装置来执行场景呢？")
        f.write('\n')
        f.write("        Given 我启动了web装置")
        f.write('\n')
        f.write("    Scenario: 我是场景的描述说明")
        f.write('\n')
        f.write("        Given 我是Given的描述说明")
        f.write('\n')
        f.write("        When 我是When的描述说明")
        f.write('\n')
        f.write("        And 我是And的描述说明")
        f.write('\n')
        f.write("        Then 我是Then的描述说明")
        f.write('\n')

#同时启动Web&App装置的feature案例
def get_feature_web_and_app_case_example(path):
    with open(os.path.join(path, 'WebAndAppCase.feature'), 'w', encoding="utf-8") as f:
        f.write("Feature: 启动app并登录")
        f.write('\n')
        f.write("    Background: 你要启动什么装置来执行场景呢？")
        f.write('\n')
        f.write("        Given 我同时启动了app、web装置")
        f.write('\n')
        f.write("    Scenario: 我是场景的描述说明")
        f.write('\n')
        f.write("        Given 我是Given的描述说明")
        f.write('\n')
        f.write("        When 我是When的描述说明")
        f.write('\n')
        f.write("        And 我是And的描述说明")
        f.write('\n')
        f.write("        Then 我是Then的描述说明")
        f.write('\n')

#同时启动Web&App装置，并且第一次打开app的feature案例
def get_feature_web_and_first_app_case_example(path):
    with open(os.path.join(path, 'WebAndFirstAppCase.feature'), 'w', encoding="utf-8") as f:
        f.write("Feature: 启动app并登录")
        f.write('\n')
        f.write("    Background: 你要启动什么装置来执行场景呢？")
        f.write('\n')
        f.write("        Given 我同时启动了app、web装置,并且第一次打开app")
        f.write('\n')
        f.write("    Scenario: 我是场景的描述说明")
        f.write('\n')
        f.write("        Given 我是Given的描述说明")
        f.write('\n')
        f.write("        When 我是When的描述说明")
        f.write('\n')
        f.write("        And 我是And的描述说明")
        f.write('\n')
        f.write("        Then 我是Then的描述说明")
        f.write('\n')
import time

from selenium import webdriver
from behave import given,step,when,then
from selenium.webdriver.common.by import By

@given('我启动了web装置,来执行{Project}项目')
def step_Process(context,Project):
    global browser
    browser = webdriver.Chrome()
    browser.maximize_window()

@given('我打开百度网址')
def step_Process(context):
    browser.get('http://www.baidu.com')


@step('我在输入框输入python')
def step_Process(context):
    browser.find_element_by_id('kw').send_keys('python')


@when('我点击百度一下')
def step_Process(context):
    browser.find_element_by_id('su').click()
    time.sleep(5)


@then('我能看到搜索出python的内容')
def step_Process(context):
    text = browser.find_element(By.XPATH,'//em').text
    print(text)
    if text == 'Python':
        browser.quit()
    else:
        browser.quit()
        raise Exception(text)
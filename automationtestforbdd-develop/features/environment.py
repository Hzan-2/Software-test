import requests
from behave import fixture
from page.webPage import Page
from page.appPage import liviPage


@fixture
def selenium_browser_chrome(context):
    context.browser = Page()
    return context.browser

@fixture
def appium_device_app(context):
    context.driver = liviPage()
    return context.driver

@fixture
def requests_test_api(context):
    context.requests = requests
    yield context.requests


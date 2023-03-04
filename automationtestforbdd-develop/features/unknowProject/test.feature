Feature: 打开baidu，搜索python

    Background: 你要启动什么装置来执行场景呢？
        Given 我启动了web装置,来执行baiduProject项目

    Scenario: 打开百度，搜索python
        Given 我打开百度网址
        And 我在输入框输入python
        When 我点击百度一下
        Then 我能看到搜索出python的内容
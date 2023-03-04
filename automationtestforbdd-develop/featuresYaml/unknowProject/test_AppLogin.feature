Feature: 启动app并登录

    Background: 你要启动什么装置来执行场景呢？
        Given 我启动了app装置

    Scenario: Livi Bank登录并且登录成功
        Given Livi Bank登录48924771账号AES<<a50ddfb1ec4155c28b912b49ab593537>>AES密码
        Then 我将登录成功，并且进入了Livi Bank主页
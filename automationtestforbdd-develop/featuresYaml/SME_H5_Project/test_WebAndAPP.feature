Feature: 测试app、web装置互相使用场景

    Background: 你要启动什么装置来执行场景呢？
        Given 我同时启动了app、web装置

    Scenario: 登录保险后管系统并验证
        Given 我登录保险后管系统
        Then 我能够看到页面左上角的logo显示为Livi Bank

    Scenario: Livi Bank登录并且登录成功
        Given Livi Bank登录48924771账号AES<<a50ddfb1ec4155c28b912b49ab593537>>密码
        Then 我将登录成功，并且进入了Livi Bank主页

    Scenario: 筛选Application的TRAVEL记录
        Given 我进入Application管理页面之后
        When 我筛选policy_Type为TRAVEL
        Then 我预期能够看到Application的列表中policy_Type都为TRAVEL

    Scenario: 退出Livi Bank的账号且退出成功
        Given 我进入Livi Bank的个人中心
        When 我点击了右上角的退出按钮
        And 我点击了确定
        Then 我可以正常的退出到登录界面

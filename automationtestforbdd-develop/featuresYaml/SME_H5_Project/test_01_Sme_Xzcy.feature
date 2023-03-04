Feature: 启动app并登录

    Background: 你要启动什么装置来执行场景呢？
        Given 我启动了app装置
    Scenario: Livi Bank登录并且登录成功
        Given Livi Bank登录88334154账号AES<<a50ddfb1ec4155c28b912b49ab593537>>AES密码
        Then 登录成功，并且进入了Livi Bank主页2
    Scenario: save零售成功切换SME首页
        Given 点击左上角切换至对公跳转页面2
        Then 切换成功，并且成功进入SME首页2
    Scenario: 点击设置页成功进入SME新增公司成员页面2
        Given SME首页点击设置页，进入SME设置页2
        And 选择公司成员按钮，进入成员设定页面2
        And 选择商业账户，点击进入公司成员页面2
        And 点击右上角添加成员，进入新增公司成员页面2
        Then 成功发起指示流程2




Feature:PayLater销户申请

    Background: 你要启动什么装置来执行场景呢？
        Given 我同时启动了app、web装置
#        我同时启动了app、web装置


    Scenario: 登录LOS后管系统进行审批
        Given 我使用账户${userName_jiang},密码${password_jiang}登录LOS后管系统
        Then 我能够看到页面左上角的logo显示为我的信息


    Scenario: Livi Bank登录并且登录成功
        Given Livi Bank登录${phone_L3}账号AES<<a50ddfb1ec4155c28b912b49ab593537>>密码
        Then 我将登录成功，并且进入了Livi Bank主页


    Scenario: PayLater销户
        Given App端进行PayLater销户操作
        Then 我能看到web端该额度状态为终止
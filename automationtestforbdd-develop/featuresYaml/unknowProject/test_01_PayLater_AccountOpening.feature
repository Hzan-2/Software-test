Feature:PayLater开户申请


    Background: 你要启动什么装置来执行场景呢？
        Given 我同时启动了app、web装置
#        我同时启动了app、web装置

    Scenario: 登录LOS后管系统进行审批
        Given 我使用账户${userName_jiang},密码${password_jiang}登录LOS后管系统
        Then 我能够看到页面左上角的logo显示为我的信息

    Scenario: Livi Bank登录并且登录成功
        Given Livi Bank登录${phone_L3}账号AES<<a50ddfb1ec4155c28b912b49ab593537>>密码
        Then 我将登录成功，并且进入了Livi Bank主页
#
    Scenario: 设置softtoken密码
        Given 进入个人设置中心，设置PIN码为${sotfTokenPIN}
        Then 我能看到PIN码设置成功页面

    Scenario: 申请PayLater
        Given 进入卡设置页面
        And 点击申请PayLater
        Then 我能看到PayLater正在申请处理中

    Scenario: 查询PayLater审批节点
        Given 获取当前账户${CustomerId}对应的审批节点
        Then 我能看到PayLater申请节点

    Scenario: 进行审批操作
        Given 进行PCSM人工审批
        And 进行PCSM复核
        And 进行反欺诈人审
        And 进行提交材料复核
        Then 我能看到PayLater申请节点为待客户确认

#    Scenario: 取消PayLater申请
#        Given 取消PayLater申请
#        Then 我看不到查看结果
#        Then 我能看到web端该额度状态为未生效
    Scenario: 接受PayLater额度
        Given 接受PayLater申请
        Then 我在卡设置页面能看到详细资料按钮
        Then 我能看到web端该额度状态为正常

#    Scenario: PayLater销户
#        Given App端进行PayLater销户操作
#        Then 我能看到web端该额度状态为终止

    #待调试
#    Scenario: PayLater开户成功，进行消费
#        Given 进入Pay后管查询MC卡信息，获取Reference
#        And  Web端使用模拟器进行PayLater消费${ConsumptionAmount}
#        Then 我能在LOS后管看到消费的借据
#        Then 我能在app端看到消费记录

#    Scenario: 停用MC卡
#        Given App端停用MC卡1
#        Then 我能看到MC卡状态为停用
#
#    Scenario: 启用MC卡
#        Given App端启用MC卡1
#        Then 我能看到MC卡状态为正常

# TODO 设置分期期数为3期
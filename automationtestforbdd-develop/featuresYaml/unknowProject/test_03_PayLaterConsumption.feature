Feature:PayLater消费


    Background: 你要启动什么装置来执行场景呢？
      Given 我同时启动了app、web装置
#      我同时启动了app、web装置

    Scenario: 登录pay后管查询MC卡信息
      Given 我使用账户${userName_jiang},密码${password_jiang}登录pay后管系统
      Then 我能够看到页面左上角的logo显示为LiviPay Transaction Portal

    Scenario: 获取MC卡信息
        Given 查询客户对应的MC卡
        Then 我能获取到卡片的信息

    Scenario: PayLater开户成功，且获取卡片信息成功，进行消费
        Given 登录web端模拟器
        And   进行PayLater消费
        Then  我能看到消费成功，返回码为1


    Scenario: PayLater消费成功，进入LOS后管，查看借据信息
        Given 进入LOS后管，查询借据
        And   进入贷款台账菜单，该客户对应的${CustomerId}查询借据信息
        Then  我能看到借据信息，借据状态，消费金额，还款计划等信息展示正确


    Scenario: PayLater消费成功，登录App，查看消费记录
        Given Livi Bank登录${phone_L3}账号AES<<a50ddfb1ec4155c28b912b49ab593537>>密码
        And   进入account页面，查看消费信息
        And   进入卡设置页面，查看消费记录
        Then  我能在APP端看到借据信息，借据状态，消费金额，还款计划等信息展示正确
Feature: 能够在后管菜单提供旅游保险相关资料

    Background: 你要启动什么装置来执行场景呢？
        Given 我启动了web装置

    Scenario: 登录保险后管系统并验证
        Given 我登录保险后管系统
        Then 我能够看到页面左上角的logo显示为Livi Bank

    Scenario: 筛选Application的TRAVEL记录
        Given 我进入Application管理页面之后
        When 我筛选policy_Type为TRAVEL
        Then 我预期能够看到Application的列表中policy_Type都为TRAVEL

    Scenario: 查看Application的TRAVEL状态信息
        Given 我进入Application管理页面之后
        When 我筛选policy_Type为TRAVEL
        And 我去查看Application的TRAVEL申请单ID时
        Then 我可以正常的查看到旅游保险的状态信息

    Scenario: export Application的记录
        Given 我进入Application管理页面之后
        When 我去export所有记录时
        Then 我在下载的文件夹中能找到export的文件
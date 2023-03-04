class gloVar():
    driverContext = None
    browserContext = None
    p = None
    platformName = None
    language = None
    project = None
    fixtures = [{
        'Step': 'Given',
        'Text': '我启动了web装置',
        'Fixture': 'web',
        'Process': []
    }, {
        'Step': 'Given',
        'Text': '我启动了app装置',
        'Fixture': 'app',
        'Process': []
    }, {
        'Step': 'Given',
        'Text': '我启动了app装置,并且第一次打开app',
        'Fixture': 'app',
        'Process': []
    }, {
        'Step': 'Given',
        'Text': '我同时启动了app、web装置',
        'Fixture': None,
        'Process': []
    }, {
        'Step': 'Given',
        'Text': '我同时启动了app、web装置,并且第一次打开app',
        'Fixture': None,
        'Process': []
    }, {
        'Step': 'quit',
        'Text': None,
        'Fixture': None,
        'Process': []
    }]
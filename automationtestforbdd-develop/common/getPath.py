import os
from config.Config import FEATURES_YAML, FEATURES_FILE


def get_app_parameter_yaml_path(type,project):
    if type == 'yaml':
        return os.path.join(FEATURES_YAML,project, 'data', 'app', 'parameter.yaml')
    else:
        return os.path.join(FEATURES_FILE,project, 'data', 'app', 'parameter.yaml')

def get_web_parameter_file_path(type,project):
    if type == 'yaml':
        return os.path.join(FEATURES_YAML,project, 'data', 'web')
    else:
        return os.path.join(FEATURES_FILE,project, 'data', 'web')

def get_api_parameter_file_path(type,project):
    if type == 'yaml':
        return os.path.join(FEATURES_YAML,project, 'data', 'api')
    else:
        return os.path.join(FEATURES_FILE,project, 'data', 'api')

def get_app_element_file_path(type,project):
    if type == 'yaml':
        return os.path.join(FEATURES_YAML,project, 'elementData', 'AppElementData')
    else:
        return os.path.join(FEATURES_FILE,project, 'elementData', 'AppElementData')

def get_web_element_file_path(type,project):
    if type == 'yaml':
        return os.path.join(FEATURES_YAML,project, 'elementData', 'WebElementData')
    else:
        return os.path.join(FEATURES_FILE,project, 'elementData', 'WebElementData')

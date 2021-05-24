import os
import sys
import yaml
import logging
from . import constant

class Config:
    def __init__(self, yaml_config_file = None, default_config_dict = constant.default_configs):
        '''
        Load configuration into a configuration dictionary
        All defaults are defined in the code utils/constant.py
        However, you can overwrite configuration server by providing a config file
        from command line, alternatively you can define environment variables.
        '''
        # 1. default configuration from built-in constants
        self.config_dict = default_config_dict

        # 2. read configuration from command line config file
        self.read_config_file(yaml_config_file)
        
        # 3. inject environment variables
        self.inject_env()


    def read_config_file(self, yaml_config_file):
        if yaml_config_file and  os.path.exists(yaml_config_file):
            try:
                with open(yaml_config_file, 'r') as f:
                    yaml_dict = yaml.load(f.read(), Loader=yaml.FullLoader)
                    self.dict_merge(self.config_dict, yaml_dict)
            except:
                logging.info('Open configuration file error {}'.format(sys.exc_info()[0]))

    def inject_env(self):
        value = ''
        def loop_dict(config_dict, v):
            for key in config_dict:
                tenv = v + '_' if v else v
                tenv += key.upper()
                if isinstance(config_dict[key], dict):
                    loop_dict(config_dict[key], tenv)
                elif tenv in os.environ:
                    config_dict[key] = os.getenv(tenv)
        loop_dict(self.config_dict, value)


    @staticmethod
    def dict_merge(a, b):
        "merges b into a"
        if not b:
            return a
    
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    dict_merge(a[key], b[key])
                elif b[key] is not None:
                    a[key] = b[key]
            else:
                a[key] = b[key]
        return a

config = None
"""
解析配置文件
"""
import logging
import os.path
import sys

import toml
from prompt_toolkit import prompt

"""
预期配置文件格式
"""
required_structure = {
    'Console': {
        'user_name': str,
        'time_zone': str,
        'type': str,
    },
    'Console.Log': {
        'debug': bool,
        'log_level': str,
    },
    'Console.Update': {
        'auto_update': bool,
        'interval': int,
        'server': list,
    },
    'Bot.*': {
        'name': str,
        'connect_type': str,
        'token': str,
        'port': int,
        'public_key': str,
        'private_key': str,
        'owner': str,
    },
    'Plugin': {
        'auto_update': bool,
        'interval': int,
        'server': list,
    },
    'Plugin.Registry': {
        'registry': list,
    }
}

class ParseConfig:
    def __init__(self, path: str = "Config.toml"):
        self.path = path
    def create(self):
        pass
    def check(self):
        # 判断配置文件是否存在
        if not os.path.isfile(self.path):
            logging.warning("找不到配置文件！")
            self.create()
        # 判断配置文件格式是否符合 TOML 格式、加载 TOML 文件
        try:
            config = toml.load(self.path)
        except toml.TomlDecodeError:
            logging.error("配置文件不符合 TOML 格式！")
            logging.info("是否重置配置文件？")
            logging.info("[ Y ] 重置文件    [ N ] 退出 Console")
            for _ in range(3):
                choose = prompt("[Y/N]").upper()
                if choose == "Y":
                    self.create()
                elif choose == "N":
                    logging.error("退出 Console！")
                    sys.exit(1)
                else:
                    logging.error(f"输入错误！[{_}/3]")
            logging.error("退出 Console！")
            sys.exit(1)
        # 校验配置文件格式
        for section, options in required_structure.items():
            sub_config = config
            for key in section.split('.'):
                sub_config = sub_config.get(key)
                if sub_config is None:
                    logging.error("此项不存在: {section}！")


            for option, expected_type in options.items():
                value = sub_config.get(option)
                if not isinstance(value, expected_type):
                    logging.error(f" {section} 中的 {option} 与预期不符！预期为： {expected_type.__name__}, got {type(value).__name__}")

        return True, "Config is valid"

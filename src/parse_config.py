import os

import pytz
import rtoml
# from sanic
from log import Log; log = Log()
from ask import ask
import shutil
import sys
import re
from typing import Dict, Any

"""配置文件内容"""
CONFIG = """# DingMeta 配置文件 0.0.2
# 修改前务必阅读注释

# 控制台配置
[Console]
user_name = "-"                     # 用户名
time_zone = "Asia/Shanghai"         # 时区（默认：Asia/Shanghai「上海时间」）
type = "Standard"                   # 版本（默认：Standard，可选 Standard「稳定版」/Beta「开发版」；此配置影响自动更新）

[Console.Log]
# 调试模式（默认：false，可选 true/false；开启调试模式后，日志等级将修改为 debug）
# 请在提交 bug 之前设置为 true
debug = false
log_mode = "file"                   # 日志模式（默认：file，可选 file「写入文件」/memory「写入内存」；请在报告 bug 之前设置为 file）
log_level = "info"                  # 日志等级（默认：info，可选 info/debug，请在提交 bug 之前设置为 debug）

# 更新配置
[Console.Update]
auto_update = true                  # 自动更新（默认：true，可选 true/false）
interval = 60                       # 更新间隔（默认：60，单位：分钟，范围：10-1000000）
# 更新服务器（不分先后）
server = ["https://gitcode.com/KirsminX/DingMeta","https://gitlab.com/KirsminX/DingMeta","https://github.com/KirsminX/DingMeta"]
# 默认服务器（在首次启动时会自动选择最优服务器）
# 如果你认为自动选择的服务器速度慢，请使用命令 update server 重新自动选择服务器
# 或者使用命令 update server <server_url> 手动选择服务器
default_server = "https://gitcode.com/KirsminX/DingMeta"

# 机器人配置
[Bot]
# 可添加多个机器人，例如 [Bot.XiaoMing]；注意每一个代码块的格式必须严格匹配
# Bot的子键是机器人的标识符，请使用英文。不可重复或包含非法字符（空格、/、:、*、?、"、<、>、|）
# 以下是示例代码块
#    [Bot.XiaoQiang]
#    name = "XiaoQiang"          # 机器人名称（请修改）
#    connect_type = "http"       # 连接方式（默认：http） 注意：stream 模式目前没有计划添加，如有需求请提出 issue
#    # 机器人密钥（请修改） 注意：报告bug时请不要公开此字段，妥善保存密钥
#    token = "-"
#    port = 8018                 # 端口（默认：8018） 注意：端口不能被占用（包括其他机器人）
#    # SSL 设置
#    # HTTP 已不再被支持。若你希望使用受信任的SSL证书，你需要在将密钥、公钥放在/Config下，分别命名为 key.pem 和 cert.pem
#    # 手动设置证书请将 no_generate_certs 设置为 true，避免被覆盖
#     generate_certs = false  # 不自动生成证书（默认：false，可选 true/false）

# 插件配置
[Plugin]
auto_update = true                  # 自动更新插件（默认：true，可选 true/false）
interval = 60                       # 更新间隔（默认：60，单位：分钟，范围：10-1000000）
# 插件服务器（不分先后）
server = ["https://gitcode.com/KirsminX/DingMeta/Plugins","https://gitlab.com/KirsminX/DingMeta/Plugins","https://github.com/KirsminX/DingMeta/Plugins"]
# 插件注册表（请勿修改！以下字段自动生成）
# 插件管理命令可以在 Console 中使用 help plugin 查看
[Plugin.Registry]
registry =[{name = "Ping", version = "1.0.0", description = "网络测试插件", author = "Kirsmin", license = "MIT", time = "2024/8/19 19:12"}]"""


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.data = None
            self.__initialize_config__()
            self.initialized = True

    def __initialize_config__(self):
        if not os.path.exists("Config.toml"):
            self.__create_config__()
        self.__load_config__()
        self.validate()

    def __load_config__(self):
        try:
            with open("Config.toml", "r", encoding="utf-8") as conf:
                self.data = rtoml.load(conf)
        except (PermissionError, FileNotFoundError):
            log.error("配置文件权限错误或不存在！请手动修复后再启动 Console")
            sys.exit(1)
        except (UnicodeDecodeError, IsADirectoryError, rtoml.TomlParsingError) as e:
            log.error(f"配置文件无法正确解析，错误信息：{e}")
            self.__handle_invalid_config__()

    def __handle_invalid_config__(self):
        user_action = ask("处理错误", {"1": "退出 Console", "2": "重置配置文件"})
        if user_action == "1":
            sys.exit(1)
        else:
            if os.path.isdir("Config.toml"):
                shutil.rmtree("Config.toml")
                log.warning("删除目录「Config.toml」并重新创建配置文件！")
            else:
                os.remove("Config.toml")
                log.warning("删除配置文件并重新创建配置文件！")
            self.__create_config__()
            self.__load_config__()

    def getter(self, table: str, key: str = None):
        try:
            return self.data[table] if key is None else self.data[table][key]
        except KeyError:
            log.error(f"无法找到配置项：[{table}][{key}]")
            return None

    def validate(self):
        errors = []
        errors.extend(self.__validate_structure__())
        errors.extend(self.__validate_values__())
        errors.extend(self.__validate_bot__())

        if errors:
            log.error("配置文件格式不正确！以下是错误信息：")
            for error in errors:
                log.error(error)
            self.__handle_invalid_config__()

    def __validate_structure__(self):
        expected_schema = {
            "Console": {
                "user_name": str,
                "time_zone": str,
                "type": str,
                "Log": {
                    "debug": bool,
                    "log_mode": str,
                },
                "Update": {
                    "auto_update": bool,
                    "interval": int,
                    "server": list
                }
            },
            "Plugin": {
                "auto_update": bool,
                "interval": int,
                "server": list,
                "Registry": {
                    "registry": list
                }
            }
        }
        return self.__validate_section__(self.data, expected_schema)

    def __validate_section__(self, data: Dict[str, Any], schema: Dict[str, Any], path: str = "") -> list:
        errors = []
        for key, expected_type in schema.items():
            current_path = f"{path}.{key}" if path else key
            if key not in data:
                errors.append(f"缺少键：{current_path}")
            elif isinstance(expected_type, dict):
                errors.extend(self.__validate_section__(data[key], expected_type, current_path))
            elif not isinstance(data[key], expected_type):
                errors.append(f"{current_path} 类型错误：期望 {expected_type.__name__}，实际 {type(data[key]).__name__}")
        return errors

    def __validate_values__(self):
        errors = []
        url_pattern = re.compile(r'^https?://[^\s/]+(?:\.[^\s/]+)+(?::\d{1,5})?(?:/\S*)?$')

        if self.data.get('Console', {}).get('time_zone') not in pytz.all_timezones:
            errors.append(f"无效的时区：{self.data['Console']['time_zone']}")

        console_log = self.data.get('Console', {}).get('Log', {})
        if console_log.get('log_level') not in ['info', 'debug']:
            errors.append(f"无效的日志级别：{console_log.get('log_level')}")
        if console_log.get('log_mode') not in ['file', 'memory']:
            errors.append(f"无效的日志模式：{console_log.get('log_mode')}")

        update = self.data.get('Console', {}).get('Update', {})
        if update.get('interval', 0) <= 10:
            errors.append(f"无效的更新间隔：{update.get('interval')}")
        for url in update.get('server', []):
            if not url_pattern.match(url):
                errors.append(f"无效的服务器地址：{url}")
            elif url.endswith('/'):
                errors.append(f"无效的服务器地址（尾随 /）：{url}")

        plugin = self.data.get('Plugin', {})
        if plugin.get('interval', 0) <= 10:
            errors.append(f"无效的插件间隔：{plugin.get('interval')}")
        for url in plugin.get('server', []):
            if not url_pattern.match(url):
                errors.append(f"无效的服务器地址：{url}")
            elif url.endswith('/'):
                errors.append(f"无效的服务器地址（尾随 /）：{url}")

        return errors

    def __validate_bot__(self):
        errors = []
        bot_schema = {
            "name": str,
            "connect_type": str,
            "token": str,
            "port": int,
            "generate_certs": bool
        }
        for bot_name, bot_data in self.data.get('Bot', {}).items():
            bot_errors = self.__validate_section__(bot_data, bot_schema, f"Bot.{bot_name}")
            errors.extend(bot_errors)

            if bot_data.get('connect_type') not in ['http', 'stream']:
                errors.append(f"无效的连接类型：{bot_data.get('connect_type')}（Bot.{bot_name}）")
            if not 0 <= bot_data.get('port', -1) < 65536:
                errors.append(f"无效的端口号：{bot_data.get('port')}（Bot.{bot_name}）")

        return errors

    @staticmethod
    def __create_config__():
        with open("Config.toml", "w", encoding="utf-8") as conf:
            conf.write(CONFIG)

    def change(self, table: str, key: str, value: Any):
        try:
            if key is None:
                self.data[table] = value
            else:
                self.data[table][key] = value
            self.__save_config__()
            self.__load_config__()
        except KeyError:
            log.error(f"无法找到配置项：[{table}][{key}]")

    def __save_config__(self):
        try:
            with open("Config.toml", "w", encoding="utf-8") as conf:
                rtoml.dump(self.data, conf)
        except (PermissionError, FileNotFoundError) as e:
            log.error(f"无法保存配置文件，错误信息：{e}")
            sys.exit(1)

if __name__ == "__main__":
    config = Config()
import os

import pytz
import rtoml
# from sanic
from log import Log; log = Log()
from ask import ask
import shutil
import sys
import re

"""配置文件内容"""
CONFIG = """# DingMeta 配置文件 0.0.1
# 修改前务必阅读注释

# 控制台配置
[Console]
user_name = "-"                     # 用户名（请修改）
time_zone = "Asia/Shanghai"         # 时区（默认：Asia/Shanghai「上海时间」）
type = "Standard"                   # 版本（默认：Standard，可选 Standard「稳定版」/Beta「开发版」；此配置影响自动更新）

[Console.Log]
debug = false                       # 调试模式（默认：false，可选 true/false；请在报告 bug 之前设置为 true）
log_level = "info"                  # 日志级别（默认：info，可选 info/debug；请在报告 bug 之前设置为 debug）
log_mode = "file"                   # 日志模式（默认：file，可选 file「写入文件」/memory「写入内存」；请在报告 bug 之前设置为 file）

# 更新配置
[Console.Update]
auto_update = true          # 自动更新（默认：true，可选 true/false）
interval = 500              # 更新间隔（默认：500，单位：秒）
# 更新服务器（默认使用第一个）
# 目前已经配置自动镜像，大概2分钟左右同步一次
server = ["https://gitcode.com/KirsminX/DingMet","https://gitlab.com/KirsminX/dingmeta","https://github.com/KirsminX/DingMeta"]

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
#     no_generate_certs = false  # 不自动生成证书（默认：false，可选 true/false）

# 插件配置
[Plugin]
auto_update = true                  # 自动更新插件（默认：true，可选 true/false）
interval = 500                      # 更新间隔（默认：500，单位：秒）
# 插件服务器（不分先后）
server = ["https://gitcode/KirsminX/DingMeta/Plugins","https://gitlab.com/KirsminX/DingMeta/Plugins","https://github.com/KirsminX/DingMeta/Plugins"]
# 插件注册表（请勿修改！以下字段自动生成）
# 插件管理命令可以在 Console 中使用 help plugin 查看
[Plugin.Registry]
registry =[{name = "Ping", version = "1.0.0", description = "网络测试插件", author = "Kirsmin", license = "MIT", time = "2024/8/19 19:12"}]
"""


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
            log.error(f"配置文件权限错误或不存在！请手动修复后再启动 Console")
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
                log.warning(f"删除目录「Config.toml」并重新创建配置文件！")
            else:
                os.remove("Config.toml")
                log.warning(f"删除配置文件并重新创建配置文件！")
            self.__create_config__()
            self.__load_config__()

    def getter(self, table: str, key: str = None):
        try:
            return self.data[table] if key is None else self.data[table][key]
        except KeyError:
            log.error(f"无法找到配置项: [{table}][{key}]")
            return None

    def validate(self):
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
        errors = self.__validate_section__(self.data, expected_schema)
        if errors:
            log.error("配置文件格式不正确！以下是错误信息：")
            for error in errors:
                log.error(error)
            self.__handle_invalid_config__()

    def __validate_section__(self, data, schema, section_name=""):
        errors = []
        for key, expected_type in schema.items():
            if key not in data:
                errors.append(f"缺少键 {section_name}.{key}")
            elif isinstance(expected_type, dict):
                errors += self.__validate_section__(data[key], expected_type, f"{section_name}.{key}")
            elif not isinstance(data[key], expected_type):
                errors.append(
                    f"{section_name}.{key} 类型错误：期望 {expected_type.__name__}, 实际 {type(data[key]).__name__}")
        # 匹配网址
        url_pattern = re.compile(r'^https?://[^\s/]+(?:\.[^\s/]+)+(:\d{1,5})?(?:\S*[^/\s])?$')

        # 验证 Console 部分
        if (tz := self.data.get('Console', {}).get('time_zone', '')) not in pytz.all_timezones:
            errors.append(f"无效的时区: {tz}")

        # 验证 Console.Log 部分
        console_log = self.data.get('Console', {}).get('Log', {})
        if (level := console_log.get('log_level', '')) not in ['info', 'debug']:
            errors.append(f"无效的日志级别: {level}")
        if (mode := console_log.get('log_mode', '')) not in ['file', 'memory']:
            errors.append(f"无效的日志模式: {mode}")

        # 验证 Console.Update 部分
        update = self.data.get('Console', {}).get('Update', {})
        if (interval := update.get('interval', 0)) <= 10:
            errors.append(f"无效的更新间隔: {interval}")
        for url in update.get('server', []):
            if not url or not url_pattern.match(url):
                errors.append(f"无效的服务器地址: {url}")

        # 验证 Plugin 部分
        if (interval := self.data.get('Plugin', {}).get('interval', 0)) <= 10:
            errors.append(f"无效的插件间隔: {interval}")
        for url in self.data.get('Plugin', {}).get('server', []):
            if not url or not url_pattern.match(url):
                errors.append(f"无效的服务器地址: {url}")

        # 验证 Bot.* 部分
        for bot_name, bot_data in self.data.get('Bot', {}).items():
            if (connect_type := bot_data.get('connect_type', '')) not in ['http', 'stream']:
                errors.append(f"无效的连接类型: {connect_type} ({bot_name})")
            if (port := bot_data.get('port', -1)) not in range(65536):
                errors.append(f"无效的端口号: {port} ({bot_name})")

        # 对错误信息进行去重
        errors = list(set(errors))
        return errors
    @staticmethod
    def __create_config__():
        with open("Config.toml", "w", encoding="utf-8") as conf:
            conf.write(CONFIG)
if __name__ == "__main__":
    config = Config()
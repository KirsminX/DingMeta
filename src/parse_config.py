import os
import rtoml
# from sanic
from log import Log; log = Log()
from console import ask_prompt
import shutil
import sys

"""配置文件内容"""
CONFIG = """
# DingMeta 配置文件 0.0.1
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
    def __init__(self):
        self.data = None
        self.__get_config__()
    def getter(self, table: str, key: str = None):
        if key is None:
            return self.data[table]
        return self.data[table][key]
    def __get_config__(self):
        try:
            with open ("Config.toml", "r", encoding="utf-8") as config:
                self.data = rtoml.load(config)
        except PermissionError:
            log.error("无权限读取 Config.toml！请正确配置权限后再运行 Console")
            sys.exit(1)
        except FileNotFoundError:
            Config.__create_config__()
        except UnicodeDecodeError:
            log.error("Config.toml 的编码格式不正确！请使用 UTF-8 编码")
            user_agent = ask_prompt("处理错误", {"1": "退出 Console", "2": "删除文件、重新创建配置文件"}, "1")
            if user_agent == "1":
                sys.exit(1)
            else:
                os.remove("Config.toml")
                Config.__create_config__()
                log.info("创建配置文件！")
        except IsADirectoryError:
            log.error("Config.toml 是一个目录，而不是配置文件！")
            user_choose = ask_prompt("处理错误", {"1": "退出 Console", "2": "删除目录、重新创建配置文件"}, "1")
            if user_choose == "1":
                sys.exit(1)
            else:
                shutil.rmtree("Config.toml")
                log.warning("删除目录！")
                Config.__create_config__()
                log.info("创建配置文件！")
        except rtoml.TomlParsingError:
            log.error("Config.toml 格式不正确！")
            user_choose = ask_prompt("处理错误", {"1": "退出 Console", "2": "删除文件、重新创建配置文件"}, "1")
            if user_choose == "1":
                sys.exit(1)
            else:
                os.remove("Config.toml")
                Config.__create_config__()
                log.info("创建配置文件！")

    def validate(self):
        errors = []

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
                    "registry": list  # 这里应该是字典列表
                }
            }
        }

        if "Console" in self.data:
            errors += self.__validate_section__(self.data["Console"], expected_schema["Console"], "Console")
        else:
            errors.append("缺少部分: Console")

        if "Plugin" in self.data:
            errors += self.__validate_section__(self.data["Plugin"], expected_schema["Plugin"], "Plugin")
        else:
            errors.append("缺少部分: Plugin")
        if "Bot" in self.data:
            for bot_name, bot_config in self.data["Bot"].items():
                errors += self.__validate_bot__(bot_name, bot_config)
        return errors
    def __validate_section__(self, data, schema, section_name):
        errors = []
        for key, expected_type in schema.items():
            if key not in data:
                errors.append(f"缺少键: {section_name}.{key}")
            else:
                if isinstance(expected_type, dict):
                    errors += self.__validate_section__(data[key], expected_type, f"{section_name}.{key}")
                elif not isinstance(data[key], expected_type):
                    errors.append(
                        f"{section_name}.{key} 类型错误: 期望 {expected_type.__name__}, 实际 {type(data[key]).__name__}")
        return errors
    @staticmethod
    def __validate_bot__(bot_name, bot_config):
        errors = []
        bot_schema = {
            "name": str,
            "connect_type": str,
            "token": str,
            "port": int,
            "no_generate_certs": bool
        }

        if not isinstance(bot_config, dict):
            errors.append(f"无效的 Bot 配置: {bot_name} 不是一个字典")
            return errors
        for key, expected_type in bot_schema.items():
            if key not in bot_config:
                errors.append(f"Bot.{bot_name} 缺少键: {key}")
            else:
                if not isinstance(bot_config[key], expected_type):
                    errors.append(
                        f"Bot.{bot_name}.{key} 类型错误: 期望 {expected_type.__name__}, 实际 {type(bot_config[key]).__name__}")

        return errors
    @staticmethod
    def __create_config__():
        with open("Config.toml", "w", encoding="utf-8") as config:
            config.write(CONFIG)
from log import Log; log = Log()
from datetime import datetime
import pytz
from parse_config import Config
from prompt_toolkit import PromptSession

"""
控制台主类
* 用于控制台的初始化、启动、控制台命令管理、插件系统调用
"""
class Console:
    def __init__(self):
        self.config = Config()
        self.console_config = self.config.getter("Console")
        self.plugin_config = self.config.getter("Plugin")
        self.session = PromptSession()
        self.console_command = {
            "help": "帮助",
            "update": "更新",
            "user": {
                "description": "用户",
                "commands": {
                    "add": ["添加用户", "<用户名>"],
                    "delete": ["删除用户", "<用户名>"],
                    "list": {
                        "description": "显示用户列表",
                        "options": {
                            "group": ["组", "<组名>"],
                            "user": ["用户", "<用户名>"],
                            "permission": ["权限", "<权限组>"]
                        }
                    },
                    "password": {
                        "description": "用户密码",
                        "options": {
                            "reset": ["重置密码", "<用户名>"],
                            "validate" : ["验证密码", "<用户名>"]
                        }
                    }
                    ,
                    "rename": ["重命名用户", "<旧用户名>（注意：重命名控制台用户请填写「console」）", "<新用户名>"],
                    "group": {
                        "description": "用户组",
                        "commands": {
                            "add": ["添加用户组", "<组名>"],
                            "delete": ["删除用户组", "<组名>"],
                            "list": "显示所有用户组",
                            "rename": ["重命名用户组", "<旧组名>", "<新组名>"],
                            "permission": ["修改用户组权限", "<组名>", "<权限设置>"]
                        }
                    }
                }
            },
            "plugin": {
                "description": "插件",
                "commands": {
                    "update": ["更新插件", "<插件名>"],
                    "list": "显示插件列表",
                    "add": ["安装插件", "<插件名>"],
                    "remove": ["卸载插件", "<插件名>"],
                    "update_list": "手动更新插件源",
                    "enable": ["启用插件", "<插件名>"],
                    "disable": ["禁用插件", "<插件名>"]
                }
            }
        }

    def print_logo(self):
        time_zone = self.config.getter("Console", "time_zone")
        current_time = datetime.now(pytz.timezone(time_zone))
        am_pm = "上午" if current_time.strftime("%p") == "AM" else "下午"
        formatted_time = current_time.strftime(f"%Y/%m/%d {am_pm} %I:%M:%S")
        logo_color_code = "\033[38;2;17;45;78m"
        divider_color_code = "\033[38;2;57;62;70m"
        reset_code = "\033[0m"
        print(f"""
{logo_color_code}
    ██████╗  ██╗ ███╗   ██╗  ██████╗     ███╗   ███╗ ███████╗ ████████╗  █████╗ 
    ██╔══██╗ ██║ ████╗  ██║ ██╔════╝     ████╗ ████║ ██╔════╝ ╚══██╔══╝ ██╔══██╗
    ██║  ██║ ██║ ██╔██╗ ██ ║██║  ███╗    ██╔████╔██║ █████╗      ██║    ███████║
    ██║  ██║ ██║ ██║╚██╗██║ ██║   ██║    ██║╚██╔╝██║ ██╔══╝      ██║    ██╔══██║
    ██████╔╝ ██║ ██║ ╚████║ ╚██████╔╝    ██║ ╚═╝ ██║ ███████╗    ██║    ██║  ██║
    ╚═════╝  ╚═╝ ╚═╝  ╚═══╝  ╚═════╝     ╚═╝     ╚═╝ ╚══════╝    ╚═╝    ╚═╝  ╚═╝
{reset_code}
{divider_color_code}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{reset_code}      DingMeta Console    版本：Alpha    时间：{formatted_time}
""")
    def warn(self):
        if self.console_config["user_name"] == "-":
            log.warning("用户名未修改，建议使用命令 user rename 重命名")
            self.console_config["user_name"] = ""
        if not self.console_config["Update"]["server"]:
            log.warning("未设置 Console 更新服务器，建议使用命令 update server default 设置为默认更新服务器")
        if not self.plugin_config["server"]:
            log.warning("未设置插件更新服务器，建议使用命令 plugin server default 设置为默认更新服务器")
    def console_prompt(self) -> str:
        return self.session.prompt(f"{self.console_config['user_name']} φ ")


if __name__ == "__main__":
    console = Console()
    console.print_logo()
    console.warn()
    while True:
        print(console.console_prompt())
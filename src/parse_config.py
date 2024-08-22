import logging
import os.path
import sys
import time
import toml

from ask import ask

# 日志模块
logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y/%m/%d %H:%M", level=logging.INFO); logging.Formatter.converter = time.gmtime
"""默认配置文件"""
default_config = """[Console]
user_name = "-"             # 用户名（请修改）
time_zone = "Asia/Shanghai" # 时区（默认：Asia/Shanghai「上海时间」）
type = "Standard"           # 版本（默认：Standard，可选 Standard/Beta；此配置影响自动更新）

[Console.Log]
debug = false               # 调试模式（默认：false，可选 true/false；请在报告 bug 之前设置为 true）
log_level = "info"          # 日志级别（默认：info，可选 info/debug 请在报告 bug 之前设置为 debug）

[Console.Update]
auto_update = true          # 自动更新（默认：true，可选 true/false）
interval = 500              # 更新间隔（默认：500，单位：秒）
# 更新服务器（默认使用第一个）
server = ["https://github.com/KirsminX/DingMeta"]

[Bot]
# 可添加多个机器人，例如 [Bot.XiaoMing]；注意每一个代码块的格式必须严格匹配
#  [Bot.XiaoQiang]
#  name = "XiaoQiang"          # 机器人名称（请修改）
#  connect_type = "http"       # 连接方式（默认：http） 注意：stream 模式目前没有计划添加，如有需求请提出 issue
# 机器人密钥（请修改） 注意：反馈问题时请删除此字段，妥善保存密钥
#  token = "-"
#  port = 8018                 # 端口（默认：8018） 注意：端口不能被占用（包括其他机器人）
# SSL 设置
# HTTP 不再被支持，若 /Config 目录下无证书将自动生成证书
# 公钥路径（请将证书放置在 /Config 下，默认情况下不需要修改此字段）
#  public_key = "public.pem"
# 密钥路径（请将证书放置在 /Config 下，默认情况下不需要修改此字段）
#  private_key = "private.pem"
# 所有者（填写 uid，留空使用 -）
#  owner = "-"

[Plugin]
auto_update = true          # 自动更新（默认：true，可选 true/false）
interval = 500              # 更新间隔（默认：500，单位：秒）
# 插件服务器（不分先后）
server = ["https://github.com/KirsminX/DingMeta/Plugins"]
# 插件注册表（请勿修改！以下字段自动生成）
# 插件管理命令可以在 Console 中使用 /help plugin 查看
[Plugin.Registry]
registry =[{name = "Ping", version = "1.0.0", description = "网络测试插件", author = "Kirsmin", license = "MIT", time = "2024/8/19 19:12"}]"""
"""
# 解析配置文件
"""

class Config:
    def __init__(self, path: str = "Config.toml"):
        self.path = path
    def create(self):
        if os.path.isfile(self.path):
            ask_status = ask("覆盖配置文件", "warning", "覆盖配置文件", "退出 Console")
            if ask_status:
                with open(self.path, "w", encoding="utf-8") as f:
                    f.write(default_config)
                logging.info("覆盖配置文件！")
            else:
                logging.error("退出 Console！")
                sys.exit(1)
        else:
            ask_status = ask("创建配置文件", "info", "创建配置文件", "退出 Console")
            if ask_status:
                with open(self.path, "w", encoding="utf-8") as f:
                    f.write(default_config)
                logging.info("创建配置文件！")
            else:
                logging.error("退出 Console！")
                sys.exit(1)
    def check(self):
        # 判断配置文件是否存在
        if not os.path.isfile(self.path):
            logging.warning("找不到配置文件！")
            self.create()
        # 判断配置文件格式是否符合 TOML 格式、加载 TOML 文件
        try:
            toml.load(self.path)
        except toml.TomlDecodeError:
            logging.error("配置文件不符合 TOML 格式！")
            self.create()

    def get(self, _type: str, key: str, int_key: str = None):
        _config = toml.load(self.path)
        if int_key is None:
            try:
                return _config[_type][key]
            except KeyError:
                logging.error(f"找不到 {type} -> {key}！")
                self.create()
        else:
            try:
                return _config[_type][key][int_key]
            except KeyError:
                logging.error(f"找不到 {type}！")
                self.create()
if __name__ == "__main__":
    Config().check()
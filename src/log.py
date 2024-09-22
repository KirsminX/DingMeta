import os
from datetime import datetime
import pytz

"""
日志
使用方法：
# 导入日志模块
from log import Log
# 实例化
log = Log(debug = True, written = True, memorize = True, timezone = "Asia/Shanghai"  
# 记录日志（类型可选 debug/info/warning/error）
log.log("info","普通日志")
也可以使用
log.info("普通日志)
（可替换为 debug/warning/error）
"""

class Log:
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if Log.__instance__ is None:
            Log.__instance__ = object.__new__(cls)
        return Log.__instance__

    def __init__(self, debug: bool, written: bool = True, memorize: bool = True, timezone: str = "Asia/Shanghai"):
        self.written = written
        self.memorize = memorize
        self.logs = []
        self.debug_statu = debug
        self.timezone = timezone

        self.color = {
            "DEBUG": "\033[38;2;135;133;162m[调试]\033[0m",
            "INFO": "\033[38;2;0;184;169m[信息]\033[0m",
            "WARNING": "\033[38;2;255;222;125m[警告]\033[0m",
            "ERROR": "\033[38;2;246;65;108m[错误]\033[0m"
        }
        self.time_periods = {
            "子": (23, 1),
            "丑": (1, 3),
            "寅": (3, 5),
            "卯": (5, 7),
            "辰": (7, 9),
            "巳": (9, 11),
            "午": (11, 13),
            "未": (13, 15),
            "申": (15, 17),
            "酉": (17, 19),
            "戌": (19, 21),
            "亥": (21, 23)
        }
        if self.written and not os.path.isfile("Log"):
            open("Log", "w").close()

    def __get_formatted_time__(self) -> str:
        current_time = datetime.now(pytz.timezone(self.timezone))
        hour = current_time.hour
        minute = current_time.minute
        second = current_time.second
        period = next((p for p, (start, end) in self.time_periods.items()
                       if start <= hour < end or (start == 23 and hour == 0)), "")
        am_pm = "上午" if hour < 12 else "下午"
        hour_12 = hour % 12 or 12
        return f"{current_time.year}/{current_time.month}/{current_time.day} {am_pm} {hour_12}:{minute}:{second} 「{period}」"

    @staticmethod
    def __write__(msg: str):
        with open("Log", "a") as file:
            file.write(f"{msg}\n")

    def log(self, level: str, msg: str):
        formatted_msg = self.__get_msg__(level, msg)
        print(self.__get_display_msg__(level, msg))
        if self.written:
            self.__write__(formatted_msg)
        if self.memorize:
            self.logs.append(formatted_msg)

    def info(self, msg: str):
        self.log("INFO", msg)

    def debug(self, msg: str):
        if self.debug_statu:
            self.log("DEBUG", msg)

    def warning(self, msg: str):
        self.log("WARNING", msg)

    def error(self, msg: str):
        self.log("ERROR", msg)

    def __get_msg__(self, level: str, message: str) -> str:
        return f"{self.__get_formatted_time__()} [{level}] {message}"

    def __get_display_msg__(self, level: str, message: str) -> str:
        return f"{self.__get_formatted_time__()} {self.color[level]} {message}"

"""
日志记录模块
输入值
"""
import os
from datetime import datetime

import pytz
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import HTML


class Log:
    def __init__(self, debug: bool, written: bool = True, memorize: bool = True, timezone: str = "Asia/Shanghai"):
        self.written = written
        self.memorize = memorize
        self.logs = []
        self.debug_statu = debug
        self.timezone = timezone
        self.time_periods = {
            "子时": (23, 1),
            "丑时": (1, 3),
            "寅时": (3, 5),
            "卯时": (5, 7),
            "辰时": (7, 9),
            "巳时": (9, 11),
            "午时": (11, 13),
            "未时": (13, 15),
            "申时": (15, 17),
            "酉时": (17, 19),
            "戌时": (19, 21),
            "亥时": (21, 23)
        }
        self.color = {
            "DEBUG": '<p style="color: rgb(135, 133, 162);">[调试]</p>',
            "INFO": '<p style="color: rgb(0, 184, 169);">[信息]</p>',
            "WARNING": '<p style="color: rgb(255, 222, 125);">[警告]</p>',
            "ERROR": '<p style="color: rgb(246, 65, 108);">[错误]</p>'
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
    def __get_display_msg__(self, level: str, message: str) -> HTML:
        return HTML(f"{self.__get_formatted_time__()} {self.color[level]} {message}")
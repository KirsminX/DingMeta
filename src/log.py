"""
日志记录模块
输入值
"""
import os
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import HTML
import pytz
from datetime import datetime

class Log:
    def __init__(self, debug: bool,written: bool = True, memorize: bool = True, timezone: str = "Asia/Shanghai"):
        if written and not os.path.isfile("Log"):
            open("Log", "w").close()
        self.written = written
        self.memorize = memorize
        self.logs = []
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
            "DEBUG": '<p style="color: rgb(135, 133, 162);"[调试]</p>',
            "INFO": '<p style="color: rgb(0, 184, 169);">[信息]</p>',
            "WARNING": '<p style="color: rgb(255, 222, 125);">[警告]</p>',
            "ERROR": '<p style="color: rgb(246, 65, 108);">[错误]</p>'
        }
        self.debug_statu = debug
        self.timezone = timezone
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
        if not os.path.isfile("Log"):
            open("Log", "w").close()
        with open("Log", "a") as file:
            file.write(f"{msg}\n")
    @staticmethod
    def info(self, msg: str):
        print(f"{self.__get_display_msg__('INFO', msg)}")
        if self.written:
            self.__write__(f"[信息] {msg}")
        if self.memorize:
            self.logs.append(f"[信息] {msg}")

    def debug(self, msg: str):
        if self.debug_statu:
            print(f"{self.__get_display_msg__('DEBUG', msg)}")
            if self.written:
                self.__write__(f"[调试] {msg}")
            if self.memorize:
                self.logs.append(f"[调试] {msg}")

    def warning(self, msg: str):
        print(f"{self.__get_display_msg__('WARNING', msg)}")
        if self.written:
            self.__write__(f"[警告] {msg}")
        if self.memorize:
            self.logs.append(f"[警告] {msg}")

    def error(self, msg: str):
        print(f"{self.__get_display_msg__('ERROR', msg)}")
        if self.written:
            self.__write__(f"[错误] {msg}")
        if self.memorize:
            self.logs.append(f"[错误] {msg}")

    def __get_msg__(self, level: str, message: str):
        return f"{self.__get_formatted_time__()} {level} {message}"

    def __get_display_msg__(self, level: str, message: str):
        return HTML(f"{self.__get_formatted_time__()} {self.color[level]} {message}")
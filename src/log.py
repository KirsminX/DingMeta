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
    def __init__(self, written: bool = True, memorize: bool = True, timezone: str = "Asia/Shanghai"):
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
            "INFO": '<p style="color: rgb(0, 184, 169);">[信息]</p>',
            "WARNING": '<p style="color: rgb(255, 222, 125);">[警告]</p>',
            "ERROR": '<p style="color: rgb(246, 65, 108);">[错误]</p>'
        }

    def __get_formatted_time__(self, timezone: str = "Asia/Shanghai") -> str:
        current_time = datetime.now(pytz.timezone(timezone))
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
        print(HTML(f"{self.color['INFO']}{msg}"))
        if self.written:
            self.__write__(f"[INFO] {msg}")
        if self.memorize:
            self.logs.append(f"[INFO] {msg}")

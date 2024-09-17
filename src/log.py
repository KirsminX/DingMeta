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

    def __get_formatted_time__(self, timezone: str = "Asia/Shanghai") -> str:
        time = datetime.now(pytz.timezone(timezone))
        time_periods = self.time_periods
        period = ""
        for period, (start_hour, end_hour) in time_periods.items():
            if start_hour <= time.hour < end_hour or (start_hour == 23 and time.hour == 0):
                break
        am_pm = "上午" if time.hour < 12 else "下午"
        hour_12 = time.hour % 12
        if hour_12 == 0:
            hour_12 = 12
        return f"{time.year}/{time.month}/{time.day} {am_pm} {hour_12}:{time.minute}:{time.second} 「{period}」 "
    @staticmethod
    def __write__(msg: str):
        if not os.path.isfile("Log"):
            open("Log", "w").close()
        with open("Log", "a") as file:
            file.write(f"{msg}\n")
    @staticmethod
    def info(self, msg: str):
        html_msg = f'<p style="color: rgb(0, 184, 169);">[INFO]</p><p>{msg}</p>'
        print(HTML(html_msg))
        if self.written:
            self.__write__(f"[INFO] {msg}")
        if self.memorize:
            self.logs.append(f"[INFO] {msg}")

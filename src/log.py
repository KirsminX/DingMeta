import os
from datetime import datetime
import pytz

"""
日志模块
"""
class Log:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, debug: bool = False, written: bool = True, memorize: bool = True,
                 timezone: str = "Asia/Shanghai"):
        if not hasattr(self, 'initialized'):
            self.written = written
            self.memorize = memorize
            self.logs = []
            self.debug_statu = debug
            self.timezone = timezone
            self.log_file = "Log"
            self.color = {
                "DEBUG": "\033[38;2;135;133;162m[调试]\033[0m",
                "INFO": "\033[38;2;0;184;169m[信息]\033[0m",
                "WARNING": "\033[38;2;255;222;125m[警告]\033[0m",
                "ERROR": "\033[38;2;246;65;108m[错误]\033[0m"
            }
            self.time_periods = {
                "子": (23, 1), "丑": (1, 3), "寅": (3, 5), "卯": (5, 7),
                "辰": (7, 9), "巳": (9, 11), "午": (11, 13), "未": (13, 15),
                "申": (15, 17), "酉": (17, 19), "戌": (19, 21), "亥": (21, 23)
            }
            self.level_mapping = {
                "INFO": "信息",
                "WARNING": "警告",
                "ERROR": "错误",
                "DEBUG": "调试"
            }
            if self.written and not os.path.isfile(self.log_file):
                open(self.log_file, "w").close()
            self.initialized = True

    def __get_formatted_time__(self) -> str:
        current_time = datetime.now(pytz.timezone(self.timezone))
        hour = current_time.hour
        period = next(
            (p for p, (start, end) in self.time_periods.items()
             if (start <= hour < end) or (start > end and (hour >= start or hour < end))),
            ""
        )

        am_pm = "上午" if current_time.strftime("%p") == "AM" else "下午"
        return current_time.strftime(f"%Y/%m/%d {am_pm} %I:%M:%S 「{period}」")

    def __write__(self, msg: str):
        with open(self.log_file, "a") as file:
            file.write(f"{msg}\n")

    def log(self, level: str, msg: str):
        level = level.upper()
        if level not in self.color:
            raise ValueError(f"不允许未知日志级别 {level}")

        formatted_time = self.__get_formatted_time__()
        formatted_msg = f"{formatted_time} [{self.level_mapping[level]}] {msg}"
        display_msg = f"{formatted_time} {self.color[level]} {msg}"

        print(display_msg)

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

# 示例使用
if __name__ == "__main__":
    log = Log(debug=True, written=True, memorize=True, timezone="Asia/Shanghai")
    log.debug("这是调试信息")
    log.info("这是普通信息")
    log.warning("这是警告信息")
    log.error("这是错误信息")
    log.log("INFO", "- END -")
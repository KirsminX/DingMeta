from prompt_toolkit import prompt
from log import Log; log = Log()
import sys


class Console:
    def __init__(self):
        pass

"""
质询函数
输入值
question            问题
option              以字典形式的选项
default             默认值
parse_error         可选「Break」（直接返回）或者「Quit」（退出）
返回
None                用户输入空值而没有默认值
str                 用户输入结果
"""
def ask_prompt(question: str, option: dict, default: str = None, parse_error: str = "Break") -> str or None:
    log.log("info", question)
    for key, value in option.items():
        log.log("info", f"[ {key} ] {value}")
    for _ in range(3):
        if default is None:
            answer = prompt(f"->")
        else:
            answer = prompt(default)
        if answer in option:
            return answer
        if answer == "" and default is not None:
            log.log("info", f"使用默认值 「{default}」")
            return default
        log.log("warning", "输入错误！请重新输入")
    log.log("error", "错误 3 次")
    if parse_error == "Quit":
        sys.exit(1)
    else:
        return
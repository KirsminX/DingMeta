from prompt_toolkit import prompt
from log import Log; log = Log()
import error

"""质询问题"""
def ask(question: str, options: dict, default: str = None, level: str = "info",try_max_length: int = 3) -> str:
    if level == "warning":
        log.warning(f"- {question} -")
    elif level == "error":
        log.error(f"- {question} -")
    elif level == "info":
        log.info(f"- {question} -")
    else:
        raise error.InputError(f"不存在该等级：{level}")
    for key, value in options.items():
        log.info(f"[ {key} ] {value}")
    option_key = "/".join(list(options.keys()))
    for _ in range(try_max_length):
        answer = prompt(f"[{option_key}] →")
        if answer in options:
            return answer
        if answer == "" and default is not None:
            log.info(f"使用默认值 「{default}」")
            return default
        log.warning(f"输入值不正确！[{_+1}/{try_max_length}")
    log.error(f"错误 {try_max_length} 次")

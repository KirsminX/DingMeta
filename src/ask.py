from prompt_toolkit import prompt
from log import Log; log = Log()
import error

"""质询问题"""
def ask(question: str, _type_: str = "info", yes: str = None, no: str = None, default: str = None, try_max_length: int = 3) -> bool or None:
    if _type_ == "warning":
        log.warning(f"{question}？")
    elif _type_ == "info":
        log.info(f"{question}？")
    if yes and no is not None:
        question += f"[ Y ] {yes}\n[ N ]{no}"
    else:
        raise error.InputError(f"质询问题类型错误！期望值「warning/info」得到「{_type_}」")
    for i in range(try_max_length - 1):
        if default is not None:
            answer = prompt(f"[Y/N] (默认 「{default}」").upper()
        else:
            answer = prompt(f"[Y/N]").upper()
        if answer == "Y":
            return True
        elif answer == "N":
            return False
        elif default is not None:
            log.info(f"使用默认值 「{default}」")
            return default
        else:
            if i < 4:
                log.warning(f"输入值无效！[{i + 1}/{try_max_length}]")

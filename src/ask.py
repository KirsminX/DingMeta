from prompt_toolkit import prompt
from log import Log; log = Log()
import error

"""质询问题"""
def ask(question: str, _type_: str = "info", yes: str = None, no: str = None, try_max_length: int = 3):
    if _type_ == "warning":
        log.warning(f"{question}？")
    elif _type_ == "info":
        log.info(f"{question}？")
    if yes and no is not None:
        question += f"[ Y ] {yes}\n[ N ]{no}"
    else:
        raise error.InputError(f"质询问题类型错误！期望值「warning/info」得到「{_type_}」")
    for i in range(try_max_length - 1):
        answer = prompt("[Y/N]").upper()
        if answer == "Y":
            return True
        elif answer == "N":
            return False
        else:
            if i < 4:
                log.warning(f"输入值无效！[{i + 1}/{try_max_length}]")
    return None     # 用户输入无效，返回None
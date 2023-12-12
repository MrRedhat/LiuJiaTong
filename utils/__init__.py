import os
import threading

def str_to_int(c=''):
    if '3' <= c <= '9':
        return int(c)
    elif c == 'B':
        return 10
    elif c == 'J':
        return 11
    elif c == 'Q':
        return 12
    elif c == 'K':
        return 13
    elif c == 'A':
        return 14
    elif c == '2':
        return 15
    elif c == '0':  # joker
        return 16
    elif c == '1':
        return 17
    elif c == 'F':  # skip this round
        return 0
    return -1


def int_to_str(x=-1):
    if 3 <= x <= 9:
        return str(x)
    elif x == 10:
        return 'B'
    elif x == 11:
        return 'J'
    elif x == 12:
        return 'Q'
    elif x == 13:
        return 'K'
    elif x == 14:
        return 'A'
    elif x == 15:
        return '2'
    elif x == 16:  # joker
        return '0'
    elif x == 17:
        return '1'
    elif x == 0:  # skip this round
        return 'F'
    return '-'


# 返回上一位出牌玩家下标
def last_played(played_cards, player):
    i = (player - 1 + 6) % 6
    while i != player:
        if len(played_cards[i]) != 0:
            return i
        i = (i - 1 + 6) % 6
    return player

def columns(string: str) -> int:
    columns = 0
    for ch in string:
        if '\u4e00' <= ch <= '\u9fff':
            columns += 2 #中文字符占两格
        else:
            columns += 1
    return columns

def user_confirm(prompt: str, default: bool):
    while True:
        print(prompt, end='')
        print("[Y/n]" if default is True else "[y/N]", end='')
        print(": ", end='')
        while True:
            try:
                resp = input().upper()
            except EOFError:
                pass
            else:
                break
        if resp == '':
            return default
        elif resp == 'Y':
            return True
        elif resp == 'N':
            return False
        else:
            print(f"非法输入，", end='')

def register_signal_handler(ctrl_c_handler):
    if os.name == "posix":
        import signal
        def console_ctrl_handler(sig, frame):
            threading.Thread(target=ctrl_c_handler).start()
        signal.signal(signal.SIGINT, console_ctrl_handler)
    elif os.name == "nt":
        import win32api
        import win32con
        def console_ctrl_handler(ctrl_type):
            if ctrl_type == win32con.CTRL_C_EVENT:
                threading.Thread(target=ctrl_c_handler).start()
                return True
        # 注册控制台事件处理程序
        win32api.SetConsoleCtrlHandler(console_ctrl_handler, True)
    else:
        raise RuntimeError("Unknown os")
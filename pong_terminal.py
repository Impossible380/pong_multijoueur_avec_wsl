erase_screen = lambda: print("\x1b[40;1m\x1b[2J", end="", flush=True)
hide_cursor = lambda: print('\x1b[?25l', end="", flush=True)
reset_cursor = lambda: print("\x1b[H", end="", flush=True)
set_cursor = lambda x,y: print(f"\x1b[{y+1};{x+1}H", end="", flush=True)
print_ball = lambda x,y: print(f"\x1b[{y+1};{x+1}H\x1b[43;1m  ", end="", flush=True)
erase_ball = lambda x,y: print(f"\x1b[{y+1};{x+1}H\x1b[40;1m  ", end="", flush=True)
move_up = lambda n: print(f"\x1b[{n}A", end="", flush=True)
move_down = lambda n: print(f"\x1b[{n}B", end="", flush=True)
move_right = lambda n: print(f"\x1b[{n}C", end="", flush=True)
move_left = lambda n: print(f"\x1b[{n}D", end="", flush=True)


def print_racket(color_str,x,y):
    color_code = "41" if color_str == "red" else "46"
    s = "".join([f"\x1b[{y+1+i};{x+1}H\x1b[{color_code};1m \x1b[{y+1-i};{x+1}H\x1b[{color_code};1m " for i in range(3)])
    print(s, end="", flush=True)


def erase_racket(x,y):
    s = "".join([f"\x1b[{y+1+i};{x+1}H\x1b[40;1m \x1b[{y+1-i};{x+1}H\x1b[40;1m " for i in range(3)])
    print(s, end="", flush=True)
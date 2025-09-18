#!/usr/bin/env python3
# This script translates the keymap so that it's usable for dvorak layout
# 2025 Leana

CANGJIE_3_PATH = "./tables/cangjie3.txt"

qwerty_layout = ("qwertyuiop"
                 "asdfghjkl"
                 "zxcvbnm")

dvorak_layout = ("',.pyfgcrl"
                 "aoeuidhtn"
                 ";qjkxbm")

trans_map = dict(zip(qwerty_layout, dvorak_layout))

def translate(s: str) -> str :
    return s.translate(str.maketrans(trans_map))


with open(CANGJIE_3_PATH, mode="r+") as f:
    lines = f.read().splitlines()

    lines = [ translate(line) for line in lines ]
    output_content = "\n".join(lines)

    f.seek(0)
    f.write(output_content)

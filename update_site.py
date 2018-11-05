#!/usr/bin/env python
# API to update the bathroom key webpage

import re

index = "/home/pi/bathroom-key-dev/html/index.html"
right_key_avail = True
left_key_avail  = True

# background colors
both_color = "#3ddb40"
one_color = "#f4be41"
neither_color = "#f45042"

def toggle_key(key):
    global right_key_avail, left_key_avail

    if key == "right":
        key_avail = right_key_avail
        right_key_avail = not right_key_avail
    elif key == "left":
        key_avail = left_key_avail
        left_key_avail = not left_key_avail

    if key_avail:
        state = "Unavailable"
    else:
        state = "Available"

    update_html()

def set_key(key, key_avail):
    global right_key_avail, left_key_avail

    if key == "right":
        right_key_avail = key_avail
    elif key == "left":
        left_key_avail = key_avail

    if key_avail:
        state = "Available"
    else:
        state = "Unavailable"

    update_html()

def update_html():
    if (right_key_avail and left_key_avail):
        color = both_color
    elif (right_key_avail or left_key_avail):
        color = one_color
    else:
        color = neither_color
    set_bg_color(color)

def set_bg_color(color):
    global index

    with open(index, "r") as fd:
        read_data = fd.read()
        write_data = re.sub("bgcolor=\"#[a-z0-9]{6}\"",
                            "bgcolor=\"" + color + "\"",
                            read_data)

    with open(index, "w") as fd:
        fd.write(write_data)

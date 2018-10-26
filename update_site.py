#!/usr/bin/env python
# API to update the bathroom key webpage

from bs4 import BeautifulSoup

index = "/home/pi/bathroom-key/html/index.html"
right_key_avail = True
left_key_avail  = True

def toggle_key(key):
    global right_key_avail, left_key_avail

    soup = read()

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

    update_html(key_id, state, soup)
    write(soup)

def set_key(key, key_avail):
    global right_key_avail, left_key_avail

    soup = read()

    if key == "right":
        right_key_avail = key_avail
    elif key == "left":
        left_key_avail = key_avail

    if key_avail:
        state = "Available"
    else:
        state = "Unavailable"

    update_html(key, state, soup)
    write(soup)

def read():
    with open(index) as fp:
        soup = BeautifulSoup(fp)
    return soup

def write(soup):
    with open(index, "w") as fp:
        fp.write(unicode(soup))

def update_html(key, state, soup):
    key_name_id = key + "-key-name"
    key_state_id = key + "-key-state"

    key_name = soup.find(id=key_name_id)
    key_state = soup.find(id=key_state_id)

    key_name['class'] = state
    key_state['class'] = state
    key_state.string = state

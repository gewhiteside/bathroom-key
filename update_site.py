#!/usr/bin/env python
# API to update the bathroom key webpage

from bs4 import BeautifulSoup

index = "/home/pi/bathroom-key/index.html"
right_key_avail = True
left_key_avail  = True

def toggle_key(key):
    soup = read()

    # TODO(whiteside): use only one global keyword for both variables
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

    update_span(key_id, state, soup)
    write(soup)

def set_key(key, key_avail):
    soup = read()

    global right_key_avail, left_key_avail

    if key == "right":
        right_key_avail = key_avail
    elif key == "left":
        left_key_avail = key_avail

    if key_avail:
        state = "Available"
    else:
        state = "Unavailable"

    update_span(key, state, soup)
    write(soup)

def read():
    with open(index) as fp:
        soup = BeautifulSoup(fp)
    return soup

def write(soup):
    with open(index, "w") as fp:
        fp.write(unicode(soup))

def update_span(key, state, soup):
    key_id = key + "-key"
    key_span = soup.find(id=key_id)
    key_span.string = state
    key_span['class'] = state

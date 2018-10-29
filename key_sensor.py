#!/usr/bin/env python
# Checks the ultrasonic proximity sensors and updates the website
# Used the following guide:
# www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

import RPi.GPIO as GPIO
import signal
import time
import update_site

# GPIO numbers
LTRIG = 23
LECHO = 24
RTRIG = 17
RECHO = 27

continue_reading = True

def setup():
    global RTRIG, RECHO, LTRIG, LECHO

    # set up GPIOs
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RTRIG,GPIO.OUT)
    GPIO.setup(RECHO,GPIO.IN)
    GPIO.setup(LTRIG,GPIO.OUT)
    GPIO.setup(LECHO,GPIO.IN)

    signal.signal(signal.SIGINT, end_read)
    signal.signal(signal.SIGTERM, end_read)

def end_read(signal, frame):
    global continue_reading

    print "[", time.ctime(), "]", "[END] Ending read loop"
    continue_reading = False
    GPIO.cleanup()

def read_loop():
    global RTRIG, RECHO, LTRIG, LECHO
    global continue_reading

    print "[", time.ctime(), "]", "[START] Starting read loop"

    right = True
    while (continue_reading):
        if right:
            key = "right"
            TRIG = RTRIG
            ECHO = RECHO
        else:
            key = "left"
            TRIG = LTRIG
            ECHO = LECHO
        right = not right

        GPIO.output(TRIG, False)
        time.sleep(2)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        print "[", time.ctime(), "]", "[CHECK] Checking for " + key + " key"
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        if distance < 10:
            key_avail = True
            print "[", time.ctime(), "]", "[RESULT] Key available"
        else:
            key_avail = False
            print "[", time.ctime(), "]", "[RESULT] Key missing"

        update_site.set_key(key, key_avail)

setup()
read_loop()

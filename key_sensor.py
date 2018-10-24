#!/usr/bin/env python
# Checks the ultrasonic proximity sensors and updates the website

import RPi.GPIO as GPIO
import signal
import time
import update_site

# GPIO numbers
RTRIG = 23
RECHO = 24
LTRIG = 17
LECHO = 27

continue_reading = True

def setup():
    global RTRIG, RECHO, LTRIG, LECHO

    # set up GPIOs
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RTRIG,GPIO.OUT)
    GPIO.setup(RECHO,GPIO.IN)
    GPIO.setup(LTRIG,GPIO.OUT)
    GPIO.setup(LECHO,GPIO.IN)

    # hook SIGINT for cleanup when the script is aborted
    signal.signal(signal.SIGINT, end_read)

def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read loop"
    continue_reading = False
    GPIO.cleanup()

def read_loop():
    global RTRIG, RECHO, LTRIG, LECHO
    global continue_reading

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
        print "Waiting for sensor to settle"
        time.sleep(2)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        print "Checking for " + key + " key"
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        if distance < 10:
            key_avail = True
            print "Key available"
        else:
            key_avail = False
            print "Key missing"

        update_site.set_key(key, key_avail)

if __name__ == "__main__":
    setup()
    read_loop()

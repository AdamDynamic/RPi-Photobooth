#!/usr/bin/python

'''
Contains all functions that use external data sounces or api calls
'''


from subprocess import call
import RPi.GPIO as GPIO
import time
import os.path

import Reference as r

def led_take_photo(pin_number):
    ''' Makes the LED flash ahead of a photo being taken by the photobooth
        Flashes faster just before the photo is taken

    :param pin_number: The Raspberry Pi GPIO number that controls the relevant LED
    :return: True/False depending on whether the process was successful
    '''

    # Light up the LED to start
    GPIO.output(pin_number, True)
    time.sleep(1)

    for i in range(4): # This is the LED flashing to alert the user that a photo is about to be taken
        GPIO.output(pin_number, False)
        time.sleep(0.4)
        GPIO.output(pin_number, True)
        time.sleep(0.4)

    for i in range(5):
        GPIO.output(pin_number, False)
        time.sleep(0.1)
        GPIO.output(pin_number, True)
        time.sleep(0.1)

    GPIO.output(pin_number, True) # Leave the LED turned on

    return True

def turn_off_all_leds(list_of_pin_numbers):
    ''' Turns off all LEDs, for use when the photos have been taken and the photobooth resets

    :param list_of_pin_numbers: A python list containing all pin numbers to turn off
    :return: True/False on whether the process was successful
    '''

    if list_of_pin_numbers:
        for pin_number in list_of_pin_numbers:
            GPIO.output(pin_number, False)

    return True

def script_event_indicator():
    ''' Sequence used by the script to signal to users a non-typical event (e.g. error, or start-up of script)
    :return: Nothing
    '''

    # Flashes all LEDs 5 times
    for _ in range(0,5):
        GPIO.output(r.PIN_LED_PHOTO_1,True)
        GPIO.output(r.PIN_LED_PHOTO_2, True)
        GPIO.output(r.PIN_LED_PHOTO_3, True)
        GPIO.output(r.PIN_LED_PHOTO_4, True)
        time.sleep(0.3)
        GPIO.output(r.PIN_LED_PHOTO_1,False)
        GPIO.output(r.PIN_LED_PHOTO_2, False)
        GPIO.output(r.PIN_LED_PHOTO_3, False)
        GPIO.output(r.PIN_LED_PHOTO_4, False)
        time.sleep(0.3)



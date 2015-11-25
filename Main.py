#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import RPi.GPIO as GPIO
from PIL import Image
import subprocess
from time import gmtime, strftime, sleep
import logging
import RPi.GPIO as GPIO

from ImageManipulation import convert_photo_to_monochrome, crop_image_to_centre, create_image_montage, rotate_image

import InOut
import Reference as r

def actuate_camera_shutter():
    '''
    Actuates the camera and downloads the image onto the Raspberry Pi
    :return: the filepath of the photo taken
    '''

    image_name = "photobooth_" + strftime("%Y-%m-%d_%H%M%S", gmtime()) + ".jpg"
    image_filepath = r.FOLDER_PHOTOS_ORIGINAL + image_name
    gpout = ""

    try:
        gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename " + image_filepath, stderr=subprocess.STDOUT, shell=True)

        # CalledProcessError is raised when the camera is turned off (or battery dies?)

        if "ERROR" in gpout:
            print gpout
            logging.error(gpout)
            raise IOError("Not able to take photo as the command failed for photo " + image_filepath)

    except subprocess.CalledProcessError as e:
        logging.error("Unable to take photo, likely due to camera not responding - check batteries")
        logging.error(e)
        raise

    except Exception as e:
        logging.error("Unable to take photo as the command failed for photo " + image_filepath)
        logging.error(e)
        raise
    else:
        return image_filepath


def convert_image(original_image_filepath):
    ''' Transforms an image into the format of the image to be included in the montage and saves it to the folder
    :param: The filepath of the image to be converted
    :return: The filepath of the converted image
    '''

    original_image = Image.open(original_image_filepath, 'r')
    rotated_image = rotate_image(original_image)
    cropped_image = crop_image_to_centre(rotated_image)
    monochrome_image = convert_photo_to_monochrome(cropped_image)

    image_name = "photobooth_" + strftime("%Y-%m-%d_%H%M%S", gmtime()) + ".jpg"
    converted_image_filepath = r.FOLDER_PHOTOS_CONVERTED + image_name

    monochrome_image.save(converted_image_filepath, 'JPEG')

    # Append the filepath to the textfile directory to allow the slideshow to capture it
    text_file = open(r.SLIDESHOW_IMAGE_DIRECTORY, "a")
    text_file.write(converted_image_filepath + "\n")
    text_file.close()

    return converted_image_filepath


def take_photo(gpio_pin_number):
    '''
    :param gpio_pin_number: The Pi's GPIO pin number to signal to the user that the photo is being taken
    :return: The filepath of the new image
    '''

    photo_location = ""

    InOut.led_take_photo(gpio_pin_number)

    try:
        photo_location = actuate_camera_shutter()

    except subprocess.CalledProcessError:
        InOut.script_event_indicator()
        print "Unable to take photo as camera is not turned on or battery is dead"
        logging.error("Unable to take photo as camera is not turned on or battery is dead")
        raise Exception("Camera is not responding, battery is dead or camera is not turned on")

    else:
        return photo_location


def photobooth_main():
    '''
    Takes 4 photos in a series, tweets each one and then saves the individual files plus a vertical montage onto the pi
    :return: True/False on whether the process was successful
    '''

    process_success = False
    photo_file_locations_original = []
    photo_file_locations_converted = []

    # Take photo 1
    photo_location = take_photo(r.PIN_LED_PHOTO_1)
    photo_file_locations_original.append(photo_location)

    # Take photo 2
    photo_location = take_photo(r.PIN_LED_PHOTO_2)
    photo_file_locations_original.append(photo_location)

    # Take photo 3
    photo_location = take_photo(r.PIN_LED_PHOTO_3)
    photo_file_locations_original.append(photo_location)

    # Take photo 4
    photo_location = take_photo(r.PIN_LED_PHOTO_4)
    photo_file_locations_original.append(photo_location)

    print photo_file_locations_original

    try:

        # Turn on the "waiting" LED
        InOut.turn_off_all_leds([r.PIN_LED_PHOTO_1, r.PIN_LED_PHOTO_2, r.PIN_LED_PHOTO_3, r.PIN_LED_PHOTO_4])
        GPIO.output(r.PIN_LED_PHOTO_WAIT, True)

        # Convert each of the captured photos into a standardised format
        for photo in photo_file_locations_original:
            mono_photo_filepath = convert_image(photo)
            photo_file_locations_converted.append(mono_photo_filepath)

        #Turn off the "waiting" light
        GPIO.output(r.PIN_LED_PHOTO_WAIT,False)
        
        # Create a montage of the captured photos and save them down
        montage_image_name = "photobooth_" + strftime("%Y-%m-%d_%H%M%S", gmtime()) + ".jpg"
        montage_filepath = r.FOLDER_PHOTOS_MONTAGE + montage_image_name

        montage = create_image_montage(photo_file_locations_converted)
        montage.save(montage_filepath, 'JPEG')

        process_success = True

    except Exception, e:
        raise Exception(e)

    finally:

        # Turn off all photo LEDs and reset the 'wait' LED
        InOut.turn_off_all_leds([r.PIN_LED_PHOTO_1, r.PIN_LED_PHOTO_2, r.PIN_LED_PHOTO_3, r.PIN_LED_PHOTO_4])

        # Upload the montage into a public space where people can view the photos
        return process_success


# MAIN ENTRY POINT OF PROGRAM
# Switch logic taken from http://razzpisampler.oreilly.com/ch07.html

# Set up logging for the process
logging.basicConfig(filename="Photobooth_Log.txt",
                    level=logging.DEBUG,
                    format = '%(levelname)s: %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')

logging.info("Photobooth main.py started")

# Set up the various GPIO pins on the Raspberry Pi
# Broad numbering convention for naming the pins
GPIO.setmode(GPIO.BOARD)

# Output LEDs used for the photos taken
GPIO.setup(r.PIN_LED_PHOTO_1, GPIO.OUT)
GPIO.setup(r.PIN_LED_PHOTO_2, GPIO.OUT)
GPIO.setup(r.PIN_LED_PHOTO_3, GPIO.OUT)
GPIO.setup(r.PIN_LED_PHOTO_4, GPIO.OUT)

# LEDs used to indicate status to the user
GPIO.setup(r.PIN_LED_PHOTO_READY, GPIO.OUT)
GPIO.setup(r.PIN_LED_PHOTO_WAIT, GPIO.OUT)

# Indicate to the user that the script has started sucessfully by flashing all LEDs
InOut.script_event_indicator()


# Setup the input pin
# Sets the default of the pin as 'high'
# Pressing the switch drops the pin to 0v
GPIO.setup(r.PIN_SWITCH_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try: # Wrap in try loop in order to include KeyboardInterupt exception catch

    while True:    # Constantly cycles throuch script, waiting for the trigger event

        # Activate the "ready" LED
        GPIO.output(r.PIN_LED_PHOTO_READY,True)

        input_state = GPIO.input(r.PIN_SWITCH_IN)

        if input_state == False:

            # Deactivate the "ready" LED
            GPIO.output(r.PIN_LED_PHOTO_READY, False)

            try:
                photobooth_main()

            except Exception, e:
                logging.error("photobooth_main.py failed to run correctly")
                logging.error(e)
                # TODO: Include status information at the point the script failed
                InOut.script_event_indicator()
                # Send error report somehow

            else:
                logging.debug("Photo montage created successfully")

            finally:
                sleep(0.2) #Used to prevent 'switch bounce'


except KeyboardInterrupt:
    print "User ended process with KeyboardInterupt"
    InOut.turn_off_all_leds([r.PIN_LED_PHOTO_1, r.PIN_LED_PHOTO_2, r.PIN_LED_PHOTO_3, r.PIN_LED_PHOTO_4, r.PIN_LED_PHOTO_READY, r.PIN_LED_PHOTO_WAIT])
    logging.debug("Process interupted by keyboard interupt")
    GPIO.cleanup()


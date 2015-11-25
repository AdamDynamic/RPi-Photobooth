#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Contains reference and master data used elsewhere in the program
'''

# LED GPIO pin mappings
# Used to provide user information on when the photos are being taken
# and for the user to trigger the script by pressing the button controller
# Need to use BOARD numbering convention (not BCM)
PIN_LED_PHOTO_1 = int(15)
PIN_LED_PHOTO_2 = int(19)
PIN_LED_PHOTO_3 = int(21)
PIN_LED_PHOTO_4 = int(23)
PIN_LED_PHOTO_READY = int(13)
PIN_LED_PHOTO_WAIT = int(11)
PIN_SWITCH_IN = int(7)

# Folders on the Pi where the files are saved down
FOLDER_PHOTOS_ORIGINAL = "/home/pi/Desktop/PhotoBooth/Original/"
FOLDER_PHOTOS_CONVERTED = "/home/pi/Desktop/PhotoBooth/Converted/"
FOLDER_PHOTOS_MONTAGE = "/home/pi/Desktop/PhotoBooth/Montages/"

# Configuration of each image
# UK passport is 35mm width x 45mm height
PASSPORT_IMAGE_WIDTH = 35
PASSPORT_IMAGE_HEIGHT = 45

# Amount to rotate each image taken
# Handles different orientations of the camera
IMAGE_ROTATE_AMOUNT = 90

# Configuration of the photo montages
MONTAGE_NUMBER_OF_PHOTOS = 4
MONTAGE_PHOTO_WIDTH = PASSPORT_IMAGE_WIDTH * 20
MONTAGE_PHOTO_HEIGHT = PASSPORT_IMAGE_HEIGHT * 20
MONTAGE_MARGINS = [25,25,25,25] # [w, t, r, b]
MONTAGE_PADDING = 25

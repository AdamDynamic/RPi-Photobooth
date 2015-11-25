#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np
#import matplotlib.cm as cm

import Reference as r

def convert_photo_to_monochrome(image):
    ''' Converts a given image object to monocrhome and saves down the converted version
    Uses this guide (last method on list) to convert images:
    http://www.howtogeek.com/162781/how-to-convert-your-color-photos-to-stunning-black-and-white-prints/

    :param image: The image object of the file to be converted
    :return: The image object of the monochrome version of the supplied image
    '''

    im = image.convert('L')#Image.open(image).convert('L')

    return im



def create_image_montage(image_filepaths):
    """\

    From: http://code.activestate.com/recipes/578267-use-pil-to-make-a-contact-sheet-montage-of-images/
    Adapted to make a vertical 1xn array of photos

    Make a contact sheet from a group of filenames:

    image_filepaths       A list of filepaths of the image files
    returns a PIL image object.
    """

    # Calculate the size of the output image, based on the
    #  photo thumb sizes, MONTAGE_MARGINS, and MONTAGE_PADDING
    margin_width = r.MONTAGE_MARGINS[0] + r.MONTAGE_MARGINS[2]
    margin_height = r.MONTAGE_MARGINS[1] + r.MONTAGE_MARGINS[3]

    number_cols = 1             # Fixed as the images will always be in a vertical strip
    number_rows = len(image_filepaths)   # Attempt to add each file in the file list

    padw = (number_cols-1) * r.MONTAGE_PADDING
    padh = (number_rows-1) * r.MONTAGE_PADDING
    isize = (number_cols * r.MONTAGE_PHOTO_WIDTH + margin_width + padw, number_rows * r.MONTAGE_PHOTO_HEIGHT + margin_height + padh)

    # Create the new image. The background doesn't have to be white
    white = (255,255,255)
    image_montage = Image.new('RGB',isize,white)

    count = 0
    # Insert each thumb:
    for irow in range(number_rows):
        for icol in range(number_cols):

            left = r.MONTAGE_MARGINS[0] + icol*(r.MONTAGE_PHOTO_WIDTH + r.MONTAGE_PADDING)
            right = left + r.MONTAGE_PHOTO_WIDTH
            upper = r.MONTAGE_MARGINS[1] + irow*(r.MONTAGE_PHOTO_HEIGHT + r.MONTAGE_PADDING)
            lower = upper + r.MONTAGE_PHOTO_HEIGHT
            bbox = (left,upper,right,lower)

            try:
                # Read in an image and resize appropriately
                img = Image.open(image_filepaths[count]).resize((r.MONTAGE_PHOTO_WIDTH,r.MONTAGE_PHOTO_HEIGHT))
            except:
                break

            image_montage.paste(img,bbox)
            count += 1

    return image_montage



def crop_image_to_centre(image):
    ''' Crops an image from the centre of an image to a required width and height determined by the ratio of
    PASSPORT_IMAGE_HEIGHT and PASSPORT_IMAGE_WIDTH (designed to maintain as much of the image as possible)

    :param image: The original, pre-cropped image
    :param image_width: The required width of the cropped image
    :param image_height: The required height of the cropped image
    :return: The image object cropped to the required dimensions
    '''

    original_width, original_height = image.size

    top_crop = 0
    bottom_crop = 0
    right_crop = 0
    left_crop = 0

    if original_height >= original_width:

        # Determine the new height based on the ratio of the given passport photo dimensions
        new_height = int(original_width * (r.PASSPORT_IMAGE_HEIGHT/(r.PASSPORT_IMAGE_WIDTH*1.0)))
        amount_to_crop = max(original_height-new_height,0)
        top_crop = amount_to_crop / 2   # Round down to the nearest pixel
        bottom_crop = amount_to_crop / 2

    else:
        new_width = int(original_height * (r.PASSPORT_IMAGE_WIDTH/(r.PASSPORT_IMAGE_HEIGHT*1.0)))
        amount_to_crop = max(original_width-new_width,0)
        right_crop = amount_to_crop/2
        left_crop = amount_to_crop/2

    cropped_image = image.crop((left_crop,
                               top_crop,
                               original_width - right_crop,
                               original_height - bottom_crop))

    return cropped_image


def rotate_image(image):
    ''' Rotates the image to accommodate the camera not being mounted in portrait mode

    :param image: The original, pre-rotated image object
    :return: The rotated image object
    '''

    rotated_image = image.rotate(r.IMAGE_ROTATE_AMOUNT)

    return rotated_image



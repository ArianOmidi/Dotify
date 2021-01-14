# Importing all necessary libraries
import os
from dotify.Utils.Dotify import Dotify

def main():
    curdir = os.path.dirname(__file__)

    # Select image (relative), and save name
    in_path = os.path.join(curdir, '../../../resources/images/')
    image = 'girl_with_the_pearl_earring'
    img_extension = '.jpg'
    folder_name = 'dotified'
    out_path = in_path + folder_name + '/'
    img_out_extension = '_brush.png'

    # Adjust values to change output of img
    num_dots = 110.0
    rotation_angle = 10
    mutator = 4
    circle_size_constant = 3
    brightness_factor = 2.8
    resize = True
    save = True
    show = True
    grayscale = False

    dot = Dotify(in_path, image, img_extension, num_dots, rotation_angle, circle_size_constant, brightness_factor,
               resize, save, show, grayscale, mutator)
    dot.filename_output = out_path + image + "_dot" + img_out_extension
    dot.create_folder(in_path, folder_name)
    dot.output_name(out_path, image)
    # brighten image
    dot.image = dot.adjust_brightness(dot.image, 1)
    dot.run()

if __name__ == '__main__':
    main()

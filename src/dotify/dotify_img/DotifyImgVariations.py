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
    img_out_extension = '.png'

    # Adjust values to change output of imgs
    start_num_dots = 60.0
    start_rotation_angle = 5
    circle_size_constant = 3
    brightness_factor = 2.8
    mutator = 3

    dots_add = 20
    angle_add = 5

    end_dots = 140
    end_ang = 20

    change_ang = False

    resize = True
    save = False
    show = True
    grayscale = False

    if change_ang == True:
        loop_count = int((end_ang - start_rotation_angle) / angle_add)
    else:
        loop_count = 1


    for i in range (0, int((end_dots - start_num_dots) / dots_add) + 1):
        print((end_dots - start_num_dots) / dots_add)

        for j in range (0, loop_count):
            dot = Dotify(in_path, image, img_extension, start_num_dots, start_rotation_angle, circle_size_constant,
                       brightness_factor, resize, save, show, grayscale, mutator)
            dot.filename_output = out_path + image + "_dot(" + str(start_num_dots) + ", " + str(start_rotation_angle) + ", " + str(mutator) + ")" + img_out_extension
            dot.create_folder(in_path, folder_name)
            dot.output_name(out_path, image)
            # brighten image
            dot.image = dot.adjust_brightness(dot.image, 1)
            dot.run()

            if change_ang == True:
                start_rotation_angle += angle_add

        start_num_dots += dots_add


if __name__ == '__main__':
    main()

# Importing all necessary libraries
import os
from src.dotify.Utils.Dotify import Dotify


def main():
    curdir = os.path.dirname(__file__)

    # Select image (relative), and save name
    in_path = os.path.join(curdir, "../../../resources/images/")
    img_extension = ".jpg"
    folder_name = "dotified"
    out_path = in_path + folder_name + "/"

    # Adjust values to change output of imgs
    num_dots = 130.0
    rotation_angle = 5
    circle_size_constant = 3
    brightness_factor = 2.8
    resize = True
    save = True
    show = False
    grayscale = False
    mutator = 3

    images = [img for img in os.listdir(in_path) if img.endswith(img_extension)]
    images.sort()
    print(images)

    for image in images:
        image = image[: (len(image) - len(img_extension))]
        dot = Dotify(
            in_path,
            image,
            img_extension,
            num_dots,
            rotation_angle,
            circle_size_constant,
            brightness_factor,
            resize,
            save,
            show,
            grayscale,
            mutator,
        )

        dot.create_folder(in_path, folder_name)
        dot.filename_output = out_path + image + "_dot.png"
        dot.output_name(out_path, image)
        dot.image = dot.adjust_brightness(dot.image, 1.5)
        dot.r_g_b_image()


if __name__ == "__main__":
    main()

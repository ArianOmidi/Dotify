# Importing all necessary libraries
import os

from src.dotify.Utils.Dotify import Dotify
from src.dotify.Utils.Img2Vid import Img2Vid
from src.dotify.Utils.Vid2Img import Vid2Img


def main():
    curdir = os.path.dirname(__file__)

    # Select image (relative), and save name
    in_path = os.path.join(curdir, "../../../resources/videos/")
    img_extension = ".jpg"
    dot_extension = ".png"
    in_video_name = "fire"
    in_video_extension = ".mp4"
    folder_name = "dotified"
    out_path = in_path + folder_name + "/"
    out_name = "fire_dotify"
    fps = 20

    # Adjust values to change output of video
    num_dots = 100.0
    rotation_angle = 5
    circle_size_constant = 3
    brightness_factor = 2.8
    mutator = 3
    resize = True
    save = True
    show = False
    grayscale = False

    dot_vid = DotVideo(
        in_path,
        in_video_name,
        in_video_extension,
        "Frames",
        "Dots",
        img_extension,
        dot_extension,
        out_path,
        out_name,
        fps,
    )
    dot_vid.run(
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


class DotVideo:
    def __init__(
        self,
        in_path,
        in_video_name,
        in_video_extension,
        frame_folder_name,
        dots_folder_name,
        img_extension,
        dot_extension,
        out_path,
        out_name,
        out_fps,
    ):
        self.in_path = in_path
        self.in_video_name = in_video_name
        self.in_video_extension = in_video_extension
        self.frame_folder_name = frame_folder_name
        self.dots_folder_name = dots_folder_name
        self.img_extension = img_extension
        self.dots_img_extension = dot_extension
        self.out_path = out_path
        self.out_name = out_name
        self.out_extension = in_video_extension
        self.out_fps = out_fps

        self.frame_path = in_path + frame_folder_name + "/"
        self.dots_path = in_path + dots_folder_name + "/"

    def vid_to_img(self):
        v2i = Vid2Img(
            self.in_path,
            self.in_video_name,
            self.in_video_extension,
            self.frame_folder_name,
            self.img_extension,
        )
        v2i.run()
        v2i.create_folder(self.in_path, self.dots_folder_name)

    def dotify(
        self,
        num_dots,
        rotation_angle,
        circle_size_constant,
        brightness_factor,
        resize,
        save,
        show,
        grayscale,
        mutator,
    ):
        images = [
            img
            for img in os.listdir(self.frame_path)
            if img.endswith(self.img_extension)
        ]
        images.sort()
        print(images)

        for image in images:
            dot_im = Dotify(
                self.frame_path,
                image,
                "",
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
            dot_im.filename_output = (
                self.dots_path + image[:9] + "_dot" + self.dots_img_extension
            )
            dot_im.r_g_b_image()

    def imgs_to_vid(self):
        i2v = Img2Vid(
            self.dots_path,
            self.dots_img_extension,
            self.out_fps,
            self.out_path,
            self.out_name,
            self.out_extension,
        )
        i2v.run()

    def run(
        self,
        num_dots,
        rotation_angle,
        circle_size_constant,
        brightness_factor,
        resize,
        save,
        show,
        grayscale,
        mutator,
    ):
        self.vid_to_img()
        self.dotify(
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
        self.imgs_to_vid()


if __name__ == "__main__":
    main()

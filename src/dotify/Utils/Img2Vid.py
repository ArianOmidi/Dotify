import cv2
import os

class Img2Vid:
    def __init__(self, in_path, img_extension, fps, out_path, video_name, video_extension):
        self.in_path = in_path
        self.img_extension = img_extension
        self.fps = fps
        self.out_path = out_path
        self.video_name = video_name
        self.video_extension = video_extension

    def run(self):
        os.chdir(self.in_path)

        images = [img for img in os.listdir(self.in_path) if img.endswith(self.img_extension)]
        images.sort()
        print(images)
        frame = cv2.imread(os.path.join(images[0]))
        height, width, layers = frame.shape

        os.chdir(self.out_path)

        video = cv2.VideoWriter(self.video_name + self.video_extension, cv2.VideoWriter_fourcc(*'DIVX'), self.fps, (width, height))

        for image in images:
            video.write(cv2.imread(os.path.join(self.in_path, image)))

        cv2.destroyAllWindows()
        video.release()

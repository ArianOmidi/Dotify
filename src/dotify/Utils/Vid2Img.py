# Importing all necessary libraries
import cv2
import os

class Vid2Img:
    def __init__(self, path, filename, video_extension, frame_folder, img_extension):
        self.path = path
        self.filename = filename
        self.video_extension = video_extension
        self.frame_folder = frame_folder
        self.img_extension = img_extension

        self.cam = cv2.VideoCapture(path + filename + video_extension)

    def create_folder(self, path, folder_name):
        try:
            os.chdir(path)
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            # if not created then raise error
        except OSError:
            print('Error: Creating directory of data')

    def run(self):
        self.create_folder(self.path, self.frame_folder)
        # frame
        currentframe = 0

        while (True):
            leading_zeros = ['000', '00', '0', '']

            # reading from frame
            ret, frame = self.cam.read()

            if ret:
                frame_num = leading_zeros[len(str(currentframe)) - 1] + str(currentframe)
                # if video is still left continue creating images
                name = ('%s%s/frame%s%s' % (self.path,self.frame_folder, frame_num, self.img_extension))
                print('Creating.../%s/frame%s%s' % (self.frame_folder, frame_num, self.img_extension))

                # writing the extracted images
                cv2.imwrite(name, frame)

                # increasing counter so that it will
                # show how many frames are created
                currentframe += 1
            else:
                break

        # Release all space and windows once done
        self.cam.release()
        cv2.destroyAllWindows()


#-------------------------------------------------------------------------------
# Name:        Dots
# Purpose:
#
# Author:      Arian
#
# Created:     24/10/2018
# Copyright:   (c) user 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy
import os
from math import pi, cos, sin
from PIL import Image, ImageDraw, ImageEnhance

class Dotify:
    def __init__(self, path, filename, extension, num_dots, rotation_angle, circle_size_constant, brightness_factor, resize, save, show, grayscale, mutator):
        self.path = path
        self.filename = filename
        self.extension = extension
        self.img_num_ext = 1
        self.img_out_extension = '.png'
        self.img_out_path = self.path
        self.filename_output = path + filename + "_dot" + self.img_out_extension

        self.rotation_angle = rotation_angle
        self.num_dots = num_dots
        self.circle_size_constant = circle_size_constant
        self.brightness_factor = brightness_factor
        self.resize = resize
        self.save = save
        self.show = show
        self.grayscale = grayscale
        self.mutator = mutator

        self.image = Image.open(self.path + self.filename + self.extension)
        #self.final_image

        self.original_size = [self.image.width, self.image.height]
        print("Original Size: ", self.original_size)
        self.WtoH_ratio = self.original_size[0] / self.original_size[1]

        self.arr2 = []



    def run(self):
        self.r_g_b_image()

    def r_g_b_image(self):
        rgb_images = []
        data = self.image.getdata()

        # Suppress specific bands (e.g. (255, 120, 65) -> (0, 120, 0) for g)
        r = [(d[0], 0, 0) for d in data]
        g = [(0, d[1], 0) for d in data]
        b = [(0, 0, d[2]) for d in data]

        self.image.putdata(r)
        rgb_images.append(self.image.rotate(self.rotation_angle, expand=1).convert("RGB"))

        self.image.putdata(g)
        rgb_images.append(self.image.rotate(self.rotation_angle, expand=1).convert("RGB"))

        self.image.putdata(b)
        rgb_images.append(self.image.rotate(self.rotation_angle, expand=1).convert("RGB"))

        self.img_to_array(rgb_images)

    def img_to_array(self, imgs):
        cnt = 0
        for color_indx in range(3):
            arr = numpy.array(imgs[color_indx])
            size = arr.shape

            if size[1] > size[0]:
                ratio = int(size[1] / self.num_dots)
            else:
                ratio = int(size[0] / self.num_dots)

            if cnt == 0:
                self.arr2 = numpy.zeros((int(size[0] / ratio), int(size[1] / ratio), 3))
                arr2shape = self.arr2.shape

            for x in range(int(size[0] / ratio)):
                for y in range(int(size[1] / ratio)):
                    slicearr = arr[x * ratio:(x + 1) * ratio, y * ratio:(y + 1) * ratio]
                    avg = numpy.average(slicearr)

                    self.arr2[x, y, color_indx] = int(avg)

            cnt += 1


        self.drawAndSave(arr2shape[0], arr2shape[1], 40, self.arr2, self.filename_output)

    def drawAndSave(self, pX, pY, pCellSize, pArr, pFilenameOutput):
        # compress image
        pCellSize = int(pCellSize / self.mutator)

        # size of image
        canvas = (pX * pCellSize, pY * pCellSize)

        # init canvas
        im = Image.new('RGBA', canvas, (0, 0, 0, 255))
        draw = ImageDraw.Draw(im)

        for x1 in range(pX):
            for y1 in range(pY):
                self.draw_circle(pCellSize, pArr, x1, y1, draw)

        # save image
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        image_width = im.width
        image_height = im.height

        # im.rotate(90 - rotation_angle, expand=1).crop(resize_rotated_image(rotation_angle, image_width, image_height)).save(pFilenameOutput)
        im = im.rotate(90 - self.rotation_angle, expand=1).crop(
            self.resize_rotated_image(self.rotation_angle, image_width, image_height))
        if self.resize == True:
            im.thumbnail(self.original_size)
        im = self.adjust_brightness(im, self.brightness_factor)

        if self.grayscale == True:
            im = im.convert('L')
        if self.show == True:
            show_title = ("Dots: %s, Angle: %s, Mutator: %s" % (str(self.num_dots), str(self.rotation_angle), str(self.mutator)))
            print(show_title)
            im.show(title = show_title)
        if self.save == True:
            im.save(self.filename_output)

        print("Image Size: ", im.size)
        print("Output File: ", self.filename_output)

        self.final_image = im

    def draw_circle(self, pCellSize, pArr, x, y, draw):
        red = pArr[x, y, 0]
        green = pArr[x, y, 1]
        blue = pArr[x, y, 2]

        largest_radius = max(red, green, blue)

        color = (int(red), int(green), int(blue), 255)
        radius = int(largest_radius / 255.0 * pCellSize * self.circle_size_constant)

        # dot fill size
        if radius > pCellSize:
            radius = pCellSize

        radius1 = int(radius / 2)
        radius2 = radius - radius1

        draw.ellipse(
            (x * pCellSize - radius1, y * pCellSize - radius1, x * pCellSize + radius2, y * pCellSize + radius2),
            fill=color, outline=color)
        '''
        else:
            radius = 40
            draw.rectangle([x1 * pCellSize, y1 * pCellSize, x1 * pCellSize + radius, y1 * pCellSize + radius],
                           fill= color, outline= color)
        '''

    def resize_rotated_image(self, angle, width, height):
        angle *= pi / 180

        original_img_height = width / (cos(angle) + self.WtoH_ratio * sin(angle))
        original_img_width = self.WtoH_ratio * original_img_height


        cropped_width = original_img_height * cos(angle) * sin(angle)
        cropped_height = (width - original_img_height * cos(angle)) * cos(angle)

        return_vals = (cropped_width + 8, cropped_height, original_img_width + cropped_width - 21,
                       original_img_height + cropped_height - 25)
        return return_vals

    def adjust_brightness(self, image, factor):
        enhancer_object = ImageEnhance.Brightness(image)
        new_image = enhancer_object.enhance(factor)

        return new_image

    def create_folder(self, path, folder_name):
        try:
            os.chdir(path)
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            # if not created then raise error
        except OSError:
            print('Error: Creating directory of data')

    def output_name(self, out_path, image_name):
        os.chdir(out_path)
        while (os.path.exists(self.filename_output)):
            self.filename_output = out_path + image_name + "_dot" + str(self.img_num_ext) + self.img_out_extension
            self.img_num_ext += 1





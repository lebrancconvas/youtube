from os import path, getlogin, listdir
import tkinter as tk
from PIL import Image, ImageTk
from argparse import ArgumentParser


class showImageSlide:
    def __init__(self, window, imageDir):
        self.window = window
        self.imageDirectory = imageDir
        self.images = self.getPath()
        self.imageIndex = 0
        self.image_label = tk.Label(window)
        self.image_label.pack()
        self.imageShow()
        self.window.after(3000, self.nextImage())
        


    def getPath(self):
        allImages = []
        imageFormat = ('png', 'jpg', 'jpeg')
        for imageName in(listdir(self.imageDirectory)):
            if imageName.endswith(imageFormat):
                imagePath = path.join(self.imageDirectory, imageName)
                try:
                    allImages.append(ImageTk.PhotoImage(Image.open(imagePath)))
                except IOError:
                    print(f'Error in {imageName} --->>> {IOError}')
        return allImages

    def nextImage(self):
        self.imageIndex = (self.imageIndex + 1 ) % len(self.images)
        self.imageShow()
        self.window.after(3000, self.nextImage)


    def imageShow(self):
        image = self.images[self.imageIndex]
        self.image_label.config(image=image)


if __name__ == "__main__":
    parser = ArgumentParser('Parser')
    parser.add_argument('-d', '--dir', default=f'/home/{getlogin()}/Pictures/wallpaper/', help='Image Slideshow')
    args = parser.parse_args()
    imageDir = args.dir
    window = tk.Tk()
    window.title("Slideshow")
    app = showImageSlide(window, imageDir)
    try:
        window.mainloop()
    except KeyboardInterrupt:
        print("\nProgram Closed\n")






import tkinter as tk 
from tkinter import Label, Frame, Canvas, Button, Frame, OptionMenu, StringVar, filedialog
from PIL import Image, ImageTk

from colour import ColourGeneration



class Palette():
    def __init__(self, window):
        self.window = window

        #displays the image in this box
        self.canvas = Canvas(self.window, width=320, height=180) #it's a 16:9 ratio
        self.canvas.pack(padx=10)

        #button
        self.button = Button(self.window, text="Select", command=self.getPath)
        self.button.pack(padx=10, pady=10)
        
        #options for colours
        self.option = StringVar(value="1")
        self.select = OptionMenu(self.window, self.option, "1", "2", "3", "4", "5")
        self.select.pack(padx=10, pady=10)
    
        #frame which will hold the colours
        self.frame = Frame(self.window)
        self.frame.pack(padx=10)


    def getPath(self):
        fileType = [(".jpg", ".png")]
        path = filedialog.askopenfilename(filetypes=fileType)
        if path:
            self.displayImage(path)


    def displayImage(self, path):
        image = Image.open(path).resize((320, 180))
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo
        self.getColours(image) #just use the resized image not the photoimage       

    def getColours(self, photo):
        rangeVal = int(self.option.get())
        colours = ColourGeneration().generateColours(photo, rangeVal)
        palette = []
        for colour in colours:
            colour = palette.append(f"#{colour[0]:02x}{colour[1]:02x}{colour[2]:02x}")
            self.generatePalette(palette)
    
    def generatePalette(self, colour):
        for index, colour in enumerate(colour):
            label = Label(self.frame, bg=colour, width=10, height=10)
            label.grid(row=0, column=index, padx=10, pady=10)


        
if __name__ == "__main__":
    window = tk.Tk()
    window.title = "AI colour palette"
    app = Palette(window)
    try:
        window.mainloop()
    except Exception as e:
        print(e)






from tkinter import filedialog
from PIL import Image, ImageTk

def load_image(image_path, size=(400, 400)):
    image = Image.open(image_path)
    image.thumbnail(size)
    return ImageTk.PhotoImage(image)

def open_file_dialog():
    return filedialog.askopenfilename()

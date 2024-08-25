import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL.Image import Resampling
import numpy as np
from face_swap import swap_faces

class FaceSwapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Swap Application")
        self.root.geometry("1000x700")

        self.src_image_path = ""
        self.dst_image_path = ""
        self.result_image = None

        # Создаем Canvas и Frame для прокрутки
        self.canvas = Canvas(root)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(root, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Создаем Frame для размещения всех виджетов
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.on_frame_configure)

        # Загрузка исходного изображения
        self.src_label = Label(self.frame, text="Source Image", font=("Arial", 14))
        self.src_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.src_button = Button(self.frame, text="Choose Source Image", command=self.load_src_image)
        self.src_button.grid(row=0, column=1, padx=10, pady=10)

        self.src_canvas = Canvas(self.frame, width=300, height=300, bg="lightgray")
        self.src_canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Загрузка целевого изображения
        self.dst_label = Label(self.frame, text="Destination Image", font=("Arial", 14))
        self.dst_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        self.dst_button = Button(self.frame, text="Choose Destination Image", command=self.load_dst_image)
        self.dst_button.grid(row=2, column=1, padx=10, pady=10)

        self.dst_canvas = Canvas(self.frame, width=300, height=300, bg="lightgray")
        self.dst_canvas.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Цветокоррекция
        self.color_correction_var = BooleanVar(value=True)
        self.color_correction_checkbox = Checkbutton(self.frame, text="Apply Color Correction", variable=self.color_correction_var, font=("Arial", 12))
        self.color_correction_checkbox.grid(row=4, column=0, columnspan=2, pady=10)

        # Масштабирование размера лица
        self.face_size_var = DoubleVar(value=1.0)
        self.face_size_scale = Scale(self.frame, from_=0.5, to_=2.0, resolution=0.1, orient=HORIZONTAL, variable=self.face_size_var, label="Face Size Scale", font=("Arial", 12))
        self.face_size_scale.grid(row=5, column=0, columnspan=2, pady=10)

        # Кнопка для замены лиц
        self.swap_button = Button(self.frame, text="Swap Faces", command=self.swap_faces, font=("Arial", 12), bg="lightblue")
        self.swap_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Канва для отображения результата
        self.result_canvas = Canvas(self.frame, width=400, height=400, bg="lightgray")
        self.result_canvas.grid(row=7, column=0, columnspan=2, pady=10)

        # Кнопка для сохранения результата
        self.save_button = Button(self.frame, text="Save Result", command=self.save_result, font=("Arial", 12), bg="lightgreen")
        self.save_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Строка состояния
        self.status_label = Label(self.frame, text="Status: Ready", font=("Arial", 12), fg="blue")
        self.status_label.grid(row=9, column=0, columnspan=2, pady=10)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_src_image(self):
        """Загрузка исходного изображения."""
        self.src_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.src_image_path:
            self.display_image(self.src_image_path, self.src_canvas)
            self.status_label.config(text="Status: Source image loaded")

    def load_dst_image(self):
        """Загрузка целевого изображения."""
        self.dst_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.dst_image_path:
            self.display_image(self.dst_image_path, self.dst_canvas)
            self.status_label.config(text="Status: Destination image loaded")

    def display_image(self, path, canvas):
        """Отображение изображения в Canvas, масштабирование по размеру Canvas."""
        image = Image.open(path)
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Масштабирование изображения
        image = image.resize((canvas_width, canvas_height), Resampling.LANCZOS)
        image = ImageTk.PhotoImage(image)

        canvas.delete("all")
        canvas.create_image(canvas_width / 2, canvas_height / 2, anchor=CENTER, image=image)
        canvas.image = image

    def swap_faces(self):
        """Замена лиц на изображениях с опциональной цветокоррекцией."""
        if self.src_image_path and self.dst_image_path:
            self.status_label.config(text="Status: Swapping faces...")
            self.root.update_idletasks()  # Обновляем интерфейс

            src_img = cv2.imread(self.src_image_path)
            dst_img = cv2.imread(self.dst_image_path)
            color_correction = self.color_correction_var.get()
            face_size_scale = self.face_size_var.get()

            # Применяем изменение размера лица к изображениям
            result_img = swap_faces(src_img, dst_img, color_correction=color_correction, face_size_scale=face_size_scale)

            # Преобразование результата для отображения в Tkinter
            result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            result_img_pil = Image.fromarray(result_img_rgb)

            # Преобразуем результат для отображения в Canvas
            result_img_pil = result_img_pil.resize((self.result_canvas.winfo_width(), self.result_canvas.winfo_height()), Resampling.LANCZOS)
            result_img = ImageTk.PhotoImage(result_img_pil)
            self.result_image = result_img

            self.result_canvas.delete("all")
            self.result_canvas.create_image(self.result_canvas.winfo_width() / 2, self.result_canvas.winfo_height() / 2, anchor=CENTER, image=result_img)
            self.result_canvas.image = result_img

            self.status_label.config(text="Status: Face swap completed")
        else:
            self.status_label.config(text="Status: Please load both images")

    def save_result(self):
        """Сохранение результата в файл."""
        if self.result_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"),
                                                                ("All files", "*.*")])
            if file_path:
                # Преобразуем ImageTk обратно в формат PIL.Image
                pil_image = ImageTk.getimage(self.result_image)

                # Сохраняем изображение в выбранный файл с высоким качеством
                pil_image.save(file_path, quality=95)
                self.status_label.config(text=f"Result saved to {file_path}")
        else:
            self.status_label.config(text="Status: No result image to save.")

if __name__ == "__main__":
    root = Tk()
    app = FaceSwapApp(root)
    root.mainloop()

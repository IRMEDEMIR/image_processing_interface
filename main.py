import cv2 
from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import numpy as np

# İlk sayfa fonksiyonları
def open_file_page1():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if filename:
        file_label_page1.config(text="Seçilen dosya: " + filename)
        display_mirrored_image(filename)

def display_image_page1(filename):
    image = Image.open(filename)
    photo = ImageTk.PhotoImage(image)
    image_label_page1.config(image=photo)
    image_label_page1.image = photo

def display_mirrored_image(filename):
    # Aynalanan resmi görüntüle
    resim = cv2.imread(filename)
    aynalanan_resim = cv2.copyMakeBorder(resim, 75, 75, 125, 125, cv2.BORDER_REFLECT)

    # OpenCV resmini PIL formatına dönüştür
    aynalanan_resim_pil = cv2.cvtColor(aynalanan_resim, cv2.COLOR_BGR2RGB)
    aynalanan_resim_pil = Image.fromarray(aynalanan_resim_pil)

    # PIL formatındaki resmi Tkinter için uygun formata dönüştür
    photo_aynalanan = ImageTk.PhotoImage(aynalanan_resim_pil)

    # Resmi göster
    image_label_page1_aynalanan.config(image=photo_aynalanan)
    image_label_page1_aynalanan.image = photo_aynalanan

def apply_image_processing_page1(func):
    global image_page1, photo_page1
    if image_page1:
        image_page1 = func(image_page1)
        photo_page1 = ImageTk.PhotoImage(image_page1)
        image_label_page1.config(image=photo_page1)
        image_label_page1.image = photo_page1

# İkinci sayfa fonksiyonları
def open_file_page2():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if filename:
        file_label_page2.config(text="Seçilen dosya: " + filename)
        display_image_page2(filename)

def display_image_page2(filename):
    global image_page2, original_image_page2
    image_page2 = Image.open(filename)
    original_image_page2 = image_page2.copy()  # Orijinal resmi sakla
    photo = ImageTk.PhotoImage(image_page2)
    image_label_page2.config(image=photo)
    image_label_page2.image = photo

def apply_image_processing_page2(func):
    global image_page2, photo_page2
    if image_page2:
        image_page2 = func(image_page2)
        photo_page2 = ImageTk.PhotoImage(image_page2)
        image_label_page2.config(image=photo_page2)
        image_label_page2.image = photo_page2

# Noktasal işlem fonksiyonları
def increase_brightness():
    def apply_brightness(img):
        array = np.array(img)
        array = array + 50  # Parlaklığı artırmak için piksel değerlerini artırın
        array = np.clip(array, 0, 255)  # 0-255 arasında sınırlayın
        return Image.fromarray(array.astype('uint8'))
    apply_image_processing_page2(apply_brightness)

def decrease_brightness():
    def apply_brightness(img):
        array = np.array(img)
        array = array - 50  # Parlaklığı azaltmak için piksel değerlerini azaltın
        array = np.clip(array, 0, 255)  # 0-255 arasında sınırlayın
        return Image.fromarray(array.astype('uint8'))
    apply_image_processing_page2(apply_brightness)

def increase_contrast():
    def apply_contrast(img):
        array = np.array(img)
        array = (array - 127.5) * 1.2 + 127.5  # Kontrastı artırmak için bir formül kullanın
        array = np.clip(array, 0, 255)  # 0-255 arasında sınırlayın
        return Image.fromarray(array.astype('uint8'))
    apply_image_processing_page2(apply_contrast)

def decrease_contrast():
    def apply_contrast(img):
        array = np.array(img)
        array = (array - 127.5) * 0.8 + 127.5  # Kontrastı azaltmak için bir formül kullanın
        array = np.clip(array, 0, 255)  # 0-255 arasında sınırlayın
        return Image.fromarray(array.astype('uint8'))
    apply_image_processing_page2(apply_contrast)

def negative_image():
    def apply_negative(img):
        array = np.array(img)
        array = 255 - array  # Negatif görüntü almak için her piksel değerini tersine çevirin
        return Image.fromarray(array.astype('uint8'))
    apply_image_processing_page2(apply_negative)

def reset_changes():
    global original_image_page2
    if original_image_page2:  # Eğer orijinal resim varsa
        image_page2 = original_image_page2.copy()  # Orijinal resmi geri yükle
        photo_page2 = ImageTk.PhotoImage(image_page2)
        image_label_page2.config(image=photo_page2)
        image_label_page2.image = photo_page2

window = Tk()
window.title('Görüntü İşleme Arabirimi')
window.geometry('800x800+700+25')
window.attributes('-topmost', 1)  # hep üstte kalsın

notebook = ttk.Notebook(window)

page1 = Frame(notebook, bg="#D2F5E3")
page2 = Frame(notebook, bg="#D2F5E3")

notebook.add(page1, text='Aynalama')
notebook.add(page2, text='Noktasal İşlemler')

notebook.pack(expand=True, fill='both')

# İlk Sayfa İçeriği
frame_page1 = Frame(page1, bg="#D2F5E3")
frame_page1.pack(fill="both", expand=True)

file_button_page1 = Button(frame_page1, text="Dosya Seç", command=open_file_page1, bg="#27AE60", fg="white")
file_button_page1.pack(pady=10)

file_label_page1 = Label(frame_page1, text="Seçilen dosya: ", bg="#D2F5E3")
file_label_page1.pack()

image_label_page1 = Label(frame_page1, bg="#D2F5E3")
image_label_page1.pack()

image_label_page1_aynalanan = Label(frame_page1, bg="#D2F5E3")
image_label_page1_aynalanan.pack()

# İkinci Sayfa İçeriği
frame_page2 = Frame(page2, bg="#D2F5E3")
frame_page2.pack(fill="both", expand=True)

# Resim Bileşeni
image_frame = Frame(frame_page2, bg="#B7D7D8")
image_frame.pack(side="left", fill="both", expand=True)

file_button_page2 = Button(image_frame, text="Dosya Seç", command=open_file_page2, bg="#204E5F", fg="white")
file_button_page2.pack(pady=10)

file_label_page2 = Label(image_frame, text="Seçilen dosya: ", bg="#B7D7D8")
file_label_page2.pack()

image_label_page2 = Label(image_frame, bg="#B7D7D8")
image_label_page2.pack(side="top")

# Buton Bileşenleri
button_frame = Frame(frame_page2, bg="#D2F5E3")
button_frame.pack(side="right", fill="both", expand=True)

brightness_up_button = Button(button_frame, text="Parlaklık Artır", command=increase_brightness, bg="#27AE60", fg="white")
brightness_up_button.pack(pady=30)

brightness_down_button = Button(button_frame, text="Parlaklık Azalt", command=decrease_brightness, bg="#27AE60", fg="white")
brightness_down_button.pack(pady=30)

contrast_up_button = Button(button_frame, text="Kontrast Artır", command=increase_contrast, bg="#27AE60", fg="white")
contrast_up_button.pack(pady=30)

contrast_down_button = Button(button_frame, text="Kontrast Azalt", command=decrease_contrast, bg="#27AE60", fg="white")
contrast_down_button.pack(pady=30)

negative_button = Button(button_frame, text="Negatif Alma", command=negative_image, bg="#27AE60", fg="white")
negative_button.pack(pady=30)

reset_button = Button(image_frame, text="Değişiklikleri sıfırla", command=reset_changes, bg="#FF8984", fg="white")
reset_button.pack(pady=30)

window.mainloop()

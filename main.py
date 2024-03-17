import math
import cv2 
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt

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

#küçültme büyütme fonksiyonları
def open_file_page3():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if filename:
        file_label_page3.config(text="Seçilen dosya: " + filename)
        display_image_page3(filename)
        # Küçültülmüş ve büyütülmüş hallerini göster
        display_resized_images(filename, 0.5, "Küçültülmüş")  # Örneğin, %50 küçültme
        display_resized_images(filename, 2.0, "Büyütülmüş")  # Örneğin, 2 kat büyütme


def display_image_page3(filename):
    global image_page3, original_image_page3
    image_page3 = Image.open(filename)
    original_image_page3 = image_page3.copy()  # Orijinal resmi sakla
    photo = ImageTk.PhotoImage(image_page3)
    image_label_page3.config(image=photo)
    image_label_page3.image = photo

def display_resized_images(filename, scale_factor, title):
    global image_page3, original_image_page3
    image_page3 = Image.open(filename)
    original_image_page3 = image_page3.copy()  # Orijinal resmi sakla
    resized_image = resize_image(image_page3, scale_factor)
    photo = ImageTk.PhotoImage(resized_image)
    
    # Başlık etiketi oluştur
    title_label = Label(frame_page3, text=title, bg="#D2F5E3")
    title_label.pack()  # .pack() yöntemiyle yerleştir
    
    # Resim etiketi oluştur
    image_label = Label(frame_page3, image=photo, bg="#D2F5E3")
    image_label.image = photo
    image_label.pack(pady=10)  # .pack() yöntemiyle yerleştir

def apply_image_processing_page3(func):
    global image_page3, photo_page3
    if image_page3:
        image_page3 = func(image_page3)
        photo_page3 = ImageTk.PhotoImage(image_page3)
        image_label_page3.config(image=photo_page3)
        image_label_page3.image = photo_page3

def resize_image(image, scale_factor):
    width, height = image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    resized_image = Image.new("RGB", (new_width, new_height))
    
    for y in range(new_height):
        for x in range(new_width):
            # Yeni konumun orijinal görüntüdeki karşılığı
            src_x = x / scale_factor
            src_y = y / scale_factor
            
            # Yakınsama işlemi için dört köşe pikselin koordinatları
            x0 = int(src_x)
            x1 = min(x0 + 1, width - 1)
            y0 = int(src_y)
            y1 = min(y0 + 1, height - 1)
            
            # Interpolasyon için ağırlıkların hesaplanması
            dx = src_x - x0
            dy = src_y - y0
            
            # Köşe piksellerin renk değerlerinin alınması
            p00 = image.getpixel((x0, y0))
            p01 = image.getpixel((x0, y1))
            p10 = image.getpixel((x1, y0))
            p11 = image.getpixel((x1, y1))
            
            # Bilinear interpolasyonun hesaplanması
            new_pixel = (
                int((1 - dx) * (1 - dy) * p00[0] + dx * (1 - dy) * p10[0] + (1 - dx) * dy * p01[0] + dx * dy * p11[0]),
                int((1 - dx) * (1 - dy) * p00[1] + dx * (1 - dy) * p10[1] + (1 - dx) * dy * p01[1] + dx * dy * p11[1]),
                int((1 - dx) * (1 - dy) * p00[2] + dx * (1 - dy) * p10[2] + (1 - dx) * dy * p01[2] + dx * dy * p11[2])
            )
            
            # Yeni pikselin konumuna ekleme
            resized_image.putpixel((x, y), new_pixel)
    
    return resized_image

#Zoom fonksiyonları
def open_file_page4():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if filename:
        file_label_page4.config(text="Seçilen dosya: " + filename)
        display_image_page4(filename)

def display_image_page4(filename):
    global image_page4, original_image_page4
    image_page4 = Image.open(filename)
    photo = ImageTk.PhotoImage(image_page4)
    image_label_page4.config(image=photo)
    image_label_page4.image = photo

def apply_image_processing_page4(func):
    global image_page4, photo_page4
    if image_page4:
        image_page4 = func(image_page4)
        photo_page4 = ImageTk.PhotoImage(image_page4)
        image_label_page4.config(image=photo_page4)
        image_label_page4.image = photo_page4

def apply_processing():
    # Butona basıldığında bu işlev çalışır
    # Yukarıdaki işlemleri burada çağırabilirsiniz
    if image_page4:
        # up_sampling işlemini gerçekleştirin
        up_sampled_image = up_sampling(image_page4, 2)
        # down_sampling işlemini gerçekleştirin
        down_sampled_image = down_sampling(image_page4, 2)
        
        # İşlenmiş görüntüleri gösterin
        display_processed_images(image_page4, up_sampled_image, down_sampled_image)

def display_processed_images(image, up_sampled_image, down_sampled_image):
    # Sonuçları görselleştirme
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.imshow(image)
    plt.title('Orijinal Görüntü')
    plt.subplot(1, 3, 2)
    plt.imshow(up_sampled_image)
    plt.title('Yakınlaştırılmış Görüntü')
    plt.subplot(1, 3, 3)
    plt.imshow(down_sampled_image)
    plt.title('Uzaklaştırılmış Görüntü')
    plt.show()

def up_sampling(image, factor):
    width, height = image.size
    new_width = width * factor
    new_height = height * factor
    new_image_up = Image.new("RGB", (new_width, new_height))
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            for dy in range(factor):
                for dx in range(factor):
                    new_image_up.putpixel((x * factor + dx, y * factor + dy), pixel)
    return new_image_up

def down_sampling(image, factor):
    width, height = image.size
    new_width = width // factor
    new_height = height // factor
    new_image_down = Image.new("RGB", (new_width, new_height))
    for y in range(new_height):
        for x in range(new_width):
            pixels = [image.getpixel((x * factor + dx, y * factor + dy)) for dy in range(factor) for dx in range(factor)]
            average_pixel = tuple(int(sum(channel) / len(channel)) for channel in zip(*pixels))
            new_image_down.putpixel((x, y), average_pixel)
    return new_image_down

# Döndürme fonksiyonları
def open_file_page5():
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if filename:
        file_label_page5.config(text="Seçilen dosya: " + filename)
        display_image_page5(filename)

def display_image_page5(filename):
    global image_page5, original_image_page5
    image_page5 = Image.open(filename)
    photo = ImageTk.PhotoImage(image_page5)
    image_label_page5.config(image=photo)
    image_label_page5.image = photo

def apply_image_processing_page4(func):
    global image_page5, photo_page5
    if image_page5:
        image_page5 = func(image_page5)
        photo_page5 = ImageTk.PhotoImage(image_page5)
        image_label_page5.config(image=photo_page5)
        image_label_page5.image = photo_page5

def apply_processing_p5():
    if image_page5:
        try:
            angle = float(angle_entry.get())
            rotated_image = rotate_image(image_page5, angle)
            photo_page5 = ImageTk.PhotoImage(rotated_image)
            image_label_page5.config(image=photo_page5)
            image_label_page5.image = photo_page5
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz açı değeri. Lütfen sayısal bir değer girin.")

def display_processed_images(image, up_sampled_image):
    # Sonuçları görselleştirme
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title('Orijinal Görüntü')
    plt.subplot(1, 2, 2)
    plt.imshow(up_sampled_image)
    plt.title('Döndürülmüş Görüntü')
    plt.show()

def bilinear_interpolation(image, x, y):
    # Piksel koordinatlarını alın
    x0 = int(x)
    y0 = int(y)
    x1 = x0 + 1
    y1 = y0 + 1

    # Köşe piksellerin değerlerini alın
    top_left = image.getpixel((x0, y0))
    top_right = image.getpixel((x1, y0))
    bottom_left = image.getpixel((x0, y1))
    bottom_right = image.getpixel((x1, y1))

    # Piksel aralıklarını hesaplayın
    x_weight = x - x0
    y_weight = y - y0

    # Her bir renk bileşeni için interpolasyon yapın
    red = (1 - x_weight) * (1 - y_weight) * top_left[0] + x_weight * (1 - y_weight) * top_right[0] + \
          (1 - x_weight) * y_weight * bottom_left[0] + x_weight * y_weight * bottom_right[0]

    green = (1 - x_weight) * (1 - y_weight) * top_left[1] + x_weight * (1 - y_weight) * top_right[1] + \
            (1 - x_weight) * y_weight * bottom_left[1] + x_weight * y_weight * bottom_right[1]

    blue = (1 - x_weight) * (1 - y_weight) * top_left[2] + x_weight * (1 - y_weight) * top_right[2] + \
           (1 - x_weight) * y_weight * bottom_left[2] + x_weight * y_weight * bottom_right[2]

    return int(red), int(green), int(blue)

def rotate_image(image, angle):
    # Görüntünün genişliği ve yüksekliği
    width, height = image.size
    
    # Dereceyi radyana dönüştür
    angle_rad = math.radians(angle)
    
    # Döndürülmüş görüntünün boyutlarını hesapla
    new_width = int(abs(width * math.cos(angle_rad)) + abs(height * math.sin(angle_rad)))
    new_height = int(abs(width * math.sin(angle_rad)) + abs(height * math.cos(angle_rad)))
    
    # Yeni bir görüntü oluştur
    rotated_image = Image.new("RGB", (new_width, new_height), color="white")
    
    # Yeni görüntünün merkezini hesapla
    center_x = new_width / 2
    center_y = new_height / 2
    
    # Görüntüyü döndür
    for x in range(new_width):
        for y in range(new_height):
            # Yeni pikselin orijinal görüntüdeki karşılığını bul
            orig_x = (x - center_x) * math.cos(angle_rad) + (y - center_y) * math.sin(angle_rad) + width / 2
            orig_y = -(x - center_x) * math.sin(angle_rad) + (y - center_y) * math.cos(angle_rad) + height / 2
            
            # Eğer orijinal piksel görüntü içindeyse, interpolasyon yaparak yeni görüntüye kopyala
            if 0 <= orig_x < width - 1 and 0 <= orig_y < height - 1:
                red, green, blue = bilinear_interpolation(image, orig_x, orig_y)
                rotated_image.putpixel((x, y), (red, green, blue))
    
    return rotated_image


window = Tk()
window.title('Görüntü İşleme Arabirimi')
window.geometry('800x800+700+25')
window.attributes('-topmost', 1)  # hep üstte kalsın

notebook = ttk.Notebook(window)

page1 = Frame(notebook, bg="#D2F5E3")
page2 = Frame(notebook, bg="#D2F5E3")
page3 = Frame(notebook, bg="#D2F5E3")
page4 = Frame(notebook, bg="#D2F5E3")
page5 = Frame(notebook, bg="#D2F5E3")

notebook.add(page1, text='Aynalama')
notebook.add(page2, text='Noktasal İşlemler')
notebook.add(page3, text='Küçültme Büyütme')
notebook.add(page4, text='Zoom İşlemleri')
notebook.add(page5, text='Döndürme')

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

# küçültme büyütme sayfa içeriği
frame_page3 = Frame(page3, bg="#D2F5E3")
frame_page3.pack(fill="both", expand=True)

file_button_page3 = Button(frame_page3, text="Dosya Seç", command=open_file_page3, bg="#27AE60", fg="white")
file_button_page3.pack(pady=10)

file_label_page3 = Label(frame_page3, text="Seçilen dosya: ", bg="#D2F5E3")
file_label_page3.pack()

image_label_page3 = Label(frame_page3, bg="#B7D7D8")
image_label_page3.pack(side="top")

#Zoom sayfa içeriği
frame_page4 = Frame(page4, bg="#D2F5E3")
frame_page4.pack(fill="both", expand=True)

file_button_page4 = Button(frame_page4, text="Dosya Seç", command=open_file_page4, bg="#27AE60", fg="white")
file_button_page4.pack(pady=10)

file_label_page4 = Label(frame_page4, text="Seçilen dosya: ", bg="#D2F5E3")
file_label_page4.pack()

image_label_page4 = Label(frame_page4, bg="#B7D7D8")
image_label_page4.pack(side="top")

process_button_page4 = Button(frame_page4, text="İşlemi Uygula", command=apply_processing, bg="#FF8984", fg="white")
process_button_page4.pack(pady=10)

#Döndürme sayfa içeriği
frame_page5 = Frame(page5, bg="#D2F5E3")
frame_page5.pack(fill="both", expand=True)

file_button_page5 = Button(frame_page5, text="Dosya Seç", command=open_file_page5, bg="#27AE60", fg="white")
file_button_page5.pack(pady=10)

file_label_page5 = Label(frame_page5, text="Seçilen dosya: ", bg="#D2F5E3")
file_label_page5.pack()

image_label_page5 = Label(frame_page5, bg="#B7D7D8")
image_label_page5.pack(side="top")

angle_entry = Entry(frame_page5)
angle_entry.pack()

rotate_button_page5 = Button(frame_page5, text="Döndür", command=apply_processing_p5, bg="#27AE60", fg="white")
rotate_button_page5.pack(pady=10)



window.mainloop()

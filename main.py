import cv2, os
import numpy as np
from PIL import Image

# Каскады Хаара
cascadePath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)

# Бинарные шаблоны
# Параметры незначительно влияют на нахождение лиц
recognizer = cv2.face.LBPHFaceRecognizer_create(1,8,8,8,123)

def get_images(path):
    # Ищем все фотографии в папке и записываем их в image_paths
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    print(image_paths)
    images = []

    count = 0
    for image_path in image_paths:
        # Открываем фотографию, чтобы сохранить лицо в цвете
        image = Image.open(image_path)
        # Переводим изображение в черно-белый формат и приводим его к формату массива
        gray = Image.open(image_path).convert('L')
        imarray = np.array(gray, 'uint8')
        Image.Image.close(gray)

        # Определяем области где есть лица
        faces = faceCascade.detectMultiScale(imarray, scaleFactor=1.1, minNeighbors=10, minSize=(25, 25))
        # Если лицо нашлось добавляем его в список images
        for (x, y, w, h) in faces:
            # Обрезаем цветную фотографию и сохраняем в папку
            cropped = Image.Image.crop(image, (x,y,x + w, y + h))
            cropped.save(r'../media/faces/feature' + f'{count}' + '.jpg')
            images.append(imarray[y: y + h, x: x + w])
            # В окне показываем изображение
            cv2.imshow('', imarray[y: y + h, x: x + w])
            cv2.waitKey(50)
            # cv2.imwrite(r'../media/faces/'+f'{count}'+'.jpg', image)
            count += 1
        Image.Image.close(image)
    return images

# Путь к фотографиям
path = 'test/'

# Получаем лица и соответствующие им номера
images = get_images(path)
cv2.destroyAllWindows()

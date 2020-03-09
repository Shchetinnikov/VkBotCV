import cv2
import vk_api
import os
import numpy as np
from PIL import Image

# Для детектирования лиц используем каскады Хаара
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
print(faceCascade)
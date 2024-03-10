import os
from PIL import Image
import numpy as np

def image_to_matrix(image_path):
    image = Image.open(image_path)
    matrix = np.array(image)
    return matrix

def test_creator():
    base_dir = os.path.dirname(__file__)  
    image_path = os.path.join(base_dir, 'image.jpg') 
    return image_to_matrix(image_path)

def test_creator_grayscale():
    base_dir = os.path.dirname(__file__)  
    image_path = os.path.join(base_dir, 'imageGRAY.jpg')  
    return image_to_matrix(image_path)

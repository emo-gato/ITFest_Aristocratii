from PIL import Image
import numpy as np

def image_to_matrix(image_path):
    image = Image.open(image_path)
    matrix = np.array(image)
    return matrix

def image_to_grayscale_matrix(image_path):
    image = Image.open(image_path).convert("L")  # Convert to grayscale
    matrix = np.array(image)
    return matrix

def test_creator():
    image_path = 'images/image.jpg'
    return image_to_matrix(image_path)


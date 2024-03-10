from imageToMatrix import image_to_matrix
import random

def generate_matrix(image_path=None):
    if image_path is None:
        rows = 1024
        cols = 768
        matrix = [[(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(cols)] for _ in range(rows)]
    else:
        matrix = image_to_matrix(image_path)

    return matrix

resulting_matrix = generate_matrix('images/image.jpg')

print("Sample RGB value at position (0, 0):", resulting_matrix[0][0])

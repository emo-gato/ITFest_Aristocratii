from binary_image import BinaryImage
import numpy as np
from PIL import Image

class HLDB:
    def __init__(self):
        self.centerLight = []
        self.brightnessStatus = None
        self.colorScheme = 0

    # \brief Runs the headlight detection algorithm
    # \param [in]: image - Current frame in grayscale or RGB.
    # \param [in]: width - Width of the image.
    # \param [in]: height - Height of the image.
    # \retrun: -1 for error, 0 for no light, 1 for light detected
    def run(self, image: Image, width: int, height: int):
        if self.colorScheme == 0:
            return -1
        elif self.colorScheme == 1:
            image_matrix = np.array(image)
        else:
            grayscale_image = image.convert("L")
            image_matrix = np.array(grayscale_image)

        if width == 0 | height == 0:
            return -1
        
        average_brightness = image_matrix.sum() / (width * height)
        
        self.brightnessStatus = average_brightness;
        
        image_matrix[image_matrix <= 200] = 0
        image_matrix[image_matrix > 200] = 1
        
        BinImg = BinaryImage(image_matrix, width, height)
        boxes = BinImg.get_boxes()

        biggestBox1 = boxes[0]
        biggestBox2 = boxes[0]

        for i in boxes:
            if i.get_size() > biggestBox1.get_size():
                biggestBox2 = biggestBox1
                biggestBox1 = i

        if len(boxes) == 0:
            return 0
        elif len(boxes) == 1:
            self.centerLight.append(biggestBox1.get_center())
        else:
            self.centerLight.append(biggestBox1.get_center())
            self.centerLight.append(biggestBox2.get_center())
        return 1

    # \brief Returns a list of points with the largest two spots of light
    # \return : centerLight
    def getCenterLight(self):
        return self.centerLight

    # \brief Returns a value representing the average brightness of the image
    # \return : brightnessStatus
    def getBrightnessStatus(self):
        return self.brightnessStatus
    
    # \brief Sets the color scheme of the video
    # \param [in]: imgColor - Image color. 1 for graysacle, 2 for RGB, 0 for uninit
    def setImageColor(self, imgColor):
        self.colorScheme = imgColor
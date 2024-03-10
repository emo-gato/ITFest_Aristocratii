from binary_image import BinaryImage
import numpy as np
from PIL import Image, ImageDraw
import cv2
from vector2 import Vector2
class BoundingBox:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right



class HLDB:
    def __init__(self, video_player):
        self.detected_headlights = []
        self.frame_number = 0
        self.video_player = video_player 

    def run(self, image: Image, width: int, height: int):
        image_array = np.array(image)

        hsv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)

        lower_white = np.array([0, 0, 200], dtype=np.uint8)
        upper_white = np.array([255, 30, 255], dtype=np.uint8)

        mask = cv2.inRange(hsv_image, lower_white, upper_white)


        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            moments = cv2.moments(largest_contour)
            center_x = int(moments["m10"] / moments["m00"])
            center_y = int(moments["m01"] / moments["m00"])

            self.detected_headlights.append((center_x, center_y))

            cv2.circle(image_array, (center_x, center_y), 5, (0, 0, 255), -1)

            frame_with_red_dots_path = f"frame_with_red_dots_{self.frame_number}.png"
            cv2.imwrite(frame_with_red_dots_path, cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR))

            print(f"Frame with red dots saved at: {frame_with_red_dots_path}")

            self.frame_number += 1

            output_image = Image.fromarray(image_array)
            return output_image
    def get_detected_headlights(self):
        return self.detected_headlights


    # \brief Returns a list of points with the largest two spots of light
    # \return : centerLights  # Corrected variable name
    def getCenterLights(self):
        return self.centerLights  # Corrected variable name

    # \brief Returns a value representing the average brightness of the image
    # \return : brightnessStatus
    def getBrightnessStatus(self):
        return self.brightnessStatus

    # \brief Sets the color scheme of the video
    # \param [in]: imgColor - Image color. 1 for grayscale, 2 for RGB, 0 for uninitialized
    def setImageColor(self, imgColor):
        self.colorScheme = imgColor
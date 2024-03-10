import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
class HistogramGenerator:
    def __init__(self):
        pass

    def generate_histogram(self, matrix, color=True, save_path=None):
        if color:
            flattened_matrix = np.array(matrix).reshape(-1, 3)
            r_hist = np.histogram(flattened_matrix[:, 0], bins=256, range=(0, 256))
            g_hist = np.histogram(flattened_matrix[:, 1], bins=256, range=(0, 256))
            b_hist = np.histogram(flattened_matrix[:, 2], bins=256, range=(0, 256))

            plt.figure(figsize=(10, 6))
            plt.title('RGB Histogram')
            plt.xlabel('Pixel Value')
            plt.ylabel('Frequency')

            plt.plot(r_hist[1][:-1], r_hist[0], color='red', label='Red', alpha=0.7)
            plt.plot(g_hist[1][:-1], g_hist[0], color='green', label='Green', alpha=0.7)
            plt.plot(b_hist[1][:-1], b_hist[0], color='blue', label='Blue', alpha=0.7)
        else:
            flattened_matrix = np.array(matrix).reshape(-1)
            gray_hist = np.histogram(flattened_matrix, bins=256, range=(0, 256))

            plt.figure(figsize=(10, 6))
            plt.title('Grayscale Histogram')
            plt.xlabel('Pixel Value')
            plt.ylabel('Frequency')

            plt.plot(gray_hist[1][:-1], gray_hist[0], color='black', label='Grayscale', alpha=0.7)

        plt.legend()

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

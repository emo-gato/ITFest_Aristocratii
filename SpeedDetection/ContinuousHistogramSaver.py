import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

class ContinuousHistogramSaver:
    def __init__(self, histogram_generator):
        self.histogram_generator = histogram_generator
        self.save_continuous_histogram = False
        self.save_path = 'histogram_plot.png'

    def start_saving(self, save_path=None):
        self.save_continuous_histogram = True
        if save_path:
            self.save_path = save_path

    def stop_saving(self):
        self.save_continuous_histogram = False

    def save_histogram(self, frame):
        if self.save_continuous_histogram:
            self.histogram_generator.generate_histogram(frame, color=True, save_path=self.save_path)

    def save_histogram_without_display(self, frame, save_path):
        self.histogram_generator.generate_histogram(frame, color=True, save_path=save_path)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class HistogramGenerator:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.color = None
        self.frame = None
        self.memory = []
        self.headlight = False
        self.animation_running = False

    def generate_histogram(self, matrix=None, color=True, save_path=None):
        if matrix is not None:
            self.frame = matrix
            self.color = color
        else:
            pass

        if not self.animation_running:
            return 

    def generate_histogram_headlight(self):
        self.memory.append(self.headlight)

        if not self.animation_running:
            return


    def update_histogram(self, frame):
        self.generate_histogram()

    def update_histogram_headlight(self, frame):
        self.generate_histogram_headlight()

    def animation(self):
        self.animation_running = True
        animation = FuncAnimation(self.fig, self.update_histogram, frames=1, interval=50, repeat=False)
        plt.pause(2)

    def animation_headlight(self):
        self.animation_running = True
        animation = FuncAnimation(self.fig, self.update_histogram_headlight, frames=1, interval=50, repeat=False)
        plt.pause(2)

    def animation_maker(self, new_frame, new_color):
        self.frame = new_frame
        self.color = new_color
        self.animation()

    def animation_maker_headlight(self, new_headlight):
        self.headlight = new_headlight
        self.animation_headlight()
    # Returns the last generated histogram data
    def get_last_histogram_data(self):
        if self.color:
            flattened_matrix = np.array(self.frame).reshape(-1, 3)
            r_hist = np.histogram(flattened_matrix[:, 0], bins=256, range=(0, 256))
            g_hist = np.histogram(flattened_matrix[:, 1], bins=256, range=(0, 256))
            b_hist = np.histogram(flattened_matrix[:, 2], bins=256, range=(0, 256))

            return {
                'title': 'RGB Histogram',
                'labels': ['Pixel Value', 'Frequency'],
                'data': {
                    'Red': {'values': r_hist[0], 'color': 'red'},
                    'Green': {'values': g_hist[0], 'color': 'green'},
                    'Blue': {'values': b_hist[0], 'color': 'blue'}
                }
            }

        else:
            flattened_matrix = np.array(self.frame).reshape(-1)
            gray_hist = np.histogram(flattened_matrix, bins=256, range=(0, 256))

            return {
                'title': 'Grayscale Histogram',
                'labels': ['Pixel Value', 'Frequency'],
                'data': {
                    'Grayscale': {'values': gray_hist[0], 'color': 'black'}
                }
            }

import matplotlib
# Explicitly set the backend to a suitable one
matplotlib.use('TkAgg')

from HistogramCreator import HistogramGenerator
import input_test as test
import imageToMatrix as test2

if __name__ == "__main__":
    histogram_generator = HistogramGenerator()

    # Uncomment the relevant line based on your input source
    # input_matrix = test.generate_matrix()
    input_matrix = test2.test_creator()

    # Set color parameter as needed
    histogram_generator.generate_histogram(input_matrix, color=True, save_path='histogram_plot.png')
    # or histogram_generator.generate_histogram(input_matrix, color=False, save_path='histogram_plot.png') for grayscale

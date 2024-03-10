from pathlib import Path
import os
import inspect
import git
from itertools import combinations
import tkinter as tk
from tkinter import Canvas, Button, Label, PhotoImage, filedialog
import cv2
import time
import schedule
import csv
from itertools import combinations
from datetime import datetime
from PIL import Image, ImageTk
from HistogramCreator import HistogramGenerator
from VideoPlayer import VideoPlayer
from getFrame import getFrame
import matplotlib.pyplot as plt
import imageToMatrix as test2
import numpy as np
from sklearn.cluster import DBSCAN
import inspect
import random
import threading
import sys
from ContinuousHistogramSaver import ContinuousHistogramSaver

from binary_image import BinaryImage
from bounding_box import BoundingBox
from headlight_detection_backend import HLDB
from vector2 import Vector2


histogram_generator = HistogramGenerator()
continuous_histogram_saver = ContinuousHistogramSaver(histogram_generator)

current_dir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
assetsPath = os.path.join(current_dir, 'assets/frame0')
download_button = None
purple_line_start = None
purple_line_end = None
video_loaded = False


frame_capturer = getFrame()

is_paused = [False]
video_capture = None
is_video_playing = False
video_player = None

binary_image = None
bounding_box = None
hldb = None
vector2 = None
canvas_width=800
canvas_height=400

def relativeToAssets(path: str) -> Path:
    return assetsPath / Path(path)
    

def showVideo(video_player, root, video_display):
    global is_paused, continuous_histogram_saver

    if not is_paused[0]:
        frame = video_player.getFrame()
        if frame is not None:
            frame = cv2.resize(frame, (488, 287))

            image = Image.fromarray(frame)
            image = ImageTk.PhotoImage(image=image)
            video_display.create_image(0, 0, anchor=tk.NW, image=image)
            video_display.image = image

            continuous_histogram_saver.start_saving()

            root.after(10, lambda: showVideo(video_player, root, video_display))
        else:
            print("Video finished")
            video_player.video.release()

def openVideo(video_display, root):
    global is_paused

    is_paused[0] = False
    file_path = filedialog.askopenfilename(filetypes=[("Video files", ".mp4;.avi;*.mkv")])

    global video_player
    video_player = None 

    if file_path:
        videoSource = cv2.VideoCapture(file_path)
        video_player = VideoPlayer(videoSource)
        liveStream.config(bg="#FF0000")
        showVideo(video_player, root, video_display)




def openCam(video_display, root):
    global is_paused

    is_paused[0] = False

    global video_player

    videoSource = getFrame()
    video_player = VideoPlayer(videoSource.video)
    liveStream.config(bg="#FF0000")
    showVideo(video_player, root, video_display)
        

def playVideo(video_capture, root, video_display):
    global is_video_playing, video_player, is_paused

    if video_player is not None and is_paused[0]:
        is_paused[0] = False
        video_player.playButton()
        is_video_playing = True
        updateLiveStreamButtonColor()
        showVideo(video_player, root, video_display)



def pauseVideo():
    global is_video_playing, video_player
    is_paused[0] = True
    is_video_playing = False
    updateLiveStreamButtonColor()
    video_player.pauseButton()


def rewindVideo():
    global video_player, is_paused
    if video_player is not None:
        if is_paused[0]:
            video_player.rewindButton()
        else:
            is_paused[0] = True
            video_player.rewindButton()
            showVideo(video_player, window, video_display)



def live_stats_clicked():
    global video_player, video_canvas, liveStatistics, dumpData, download_button

    frame = video_player.getFrame()

    if frame is not None:
        histogram_generator.generate_histogram(frame, color=True, save_path='histogram_plot.png')

        histogram_image = Image.open('histogram_plot.png')
        histogram_image = ImageTk.PhotoImage(histogram_image)

        liveStatistics.place_forget()
        dumpData.place_forget()

        global histogram_label
        histogram_label = Label(window, image=histogram_image)
        histogram_label.image = histogram_image
        histogram_label.place(x=0, y=0, relwidth=1, relheight=1)
        histogram_label.bind("<Button-1>", lambda event: goBack(video_canvas, [liveStatistics, dumpData]))

        download_button = Button(window, text="Download", command=lambda: downloadHistogram(), relief="flat")
        download_button.place(x=window.winfo_width() - 80, y=10)


def checkLineContinuity(line, threshold):
    x1, y1, x2, y2 = line
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance > threshold

def calculateSpeed(purple_line_start, purple_line_end):
    if purple_line_start is not None and purple_line_end is not None:
        # Calculate the length of the purple line
        length_of_purple_line = calculate_length(purple_line_start[0], purple_line_start[1],
                                                 purple_line_end[0], purple_line_end[1])

        # Convert speed to km/h
        speed_kmh = length_of_purple_line / (10000 * 1.5)

        if speed_kmh > 61.50:
            print("Illegal driving! Switching the Traffic Light Colors")

            save_to_csv(datetime.now(), 4, speed_kmh)

        return f"{speed_kmh:.2f} km/h"
    else:
        return "Unable to calculate speed"


def save_to_csv(timestamp, intersection_id, speed):
    csv_file_path = "IllegalDrivers.csv"
    is_new_file = not os.path.isfile(csv_file_path)
    with open(csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['Timestamp', 'Intersection_ID', 'Speed (km/h)']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if is_new_file:
            writer.writeheader()

        writer.writerow({
            'Timestamp': timestamp,
            'Intersection_ID': intersection_id,
            'Speed (km/h)': "{:.2f}".format(round(speed, 2))
        })

    print(f"Frame information saved to {csv_file_path}")
        
def is_connected(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    threshold = 10 
    if np.sqrt((x2 - x3)**2 + (y2 - y3)**2) < threshold or np.sqrt((x1 - x4)**2 + (y1 - y4)**2) < threshold:
        return True

    return False

def min_distance_to_line(point, line):
    x1, y1, x2, y2 = line
    x0, y0 = point

    numerator = np.abs((y2 - y1)*x0 - (x2 - x1)*y0 + x2*y1 - y2*x1)
    denominator = np.sqrt((y2 - y1)**2 + (x2 - x1)**2)

    return numerator / denominator if denominator != 0 else np.sqrt((x2 - x0)**2 + (y2 - y0)**2)

def distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))


def calculate_length(x1, y1, x2, y2):
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def midpoint(point1, point2):
    return ((point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2)

def find_two_closest_headlights(headlight_points):
    if len(headlight_points) < 2:
        return None

    headlight_points.sort(key=lambda point: point[0])  # Sort horizontally
    return headlight_points[:2]

def identifyLanes(image_path, min_distance_factor=0.25):
    frame = cv2.imread(image_path)

    if frame is not None:
        width = frame.shape[1]
        height = frame.shape[0]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        cv2.imwrite('detected_edges.png', edges)

        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=20, maxLineGap=70)

        if lines is not None:
            filtered_lines = filter_lines(lines, width, height, min_distance_factor)

            if len(filtered_lines) >= 2:
                # Sort lines by length
                filtered_lines = sorted(filtered_lines, key=line_length, reverse=True)

                # Select the two longest non-parallel lines
                longest_lines = select_two_longest_non_parallel(filtered_lines)

                for l in longest_lines:
                    draw_line(frame, l)

                # Draw the green symmetry line between the two identified lines
                draw_symmetry_line(frame, longest_lines, canvas_width, canvas_height)

                cv2.imwrite('final_image.png', frame)
            else:
                print("No valid lines found.")
        else:
            print("Failed to read the image.")

    return frame


def midpoint(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def extend_lines(lines, canvas_width, canvas_height):
    extended_lines = []

    for line in lines:
        x1, y1, x2, y2 = line
        slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')

        extended_lines.append([0, int(-x1 * slope + y1), canvas_width, int((canvas_width - x1) * slope + y1)])

    return extended_lines

def draw_symmetry_line(frame, lines, canvas_width, canvas_height):
    global purple_line_start, purple_line_end
    if len(lines) < 2:
        print("Not enough lines to draw symmetry line.")
        return None, None  # Return None if not enough lines

    extended_lines = extend_lines(lines, canvas_width, canvas_height)

    mid1 = midpoint((extended_lines[0][0], extended_lines[0][1]), (extended_lines[0][2], extended_lines[0][3]))
    mid2 = midpoint((extended_lines[1][0], extended_lines[1][1]), (extended_lines[1][2], extended_lines[1][3]))

    dir_vector_leftmost = np.array([extended_lines[0][2] - extended_lines[0][0], extended_lines[0][3] - extended_lines[0][1]], dtype=np.float64)

    dir_vector_leftmost /= np.linalg.norm(dir_vector_leftmost)
    red_mid1 = midpoint((lines[0][0], lines[0][1]), (lines[0][2], lines[0][3]))
    red_mid2 = midpoint((lines[1][0], lines[1][1]), (lines[1][2], lines[1][3]))

    dir_vector_red_lines = np.array([red_mid2[0] - red_mid1[0], red_mid2[1] - red_mid1[1]], dtype=np.float64)

    dir_vector_red_lines /= np.linalg.norm(dir_vector_red_lines)

    deviation_angle = 5.0 
    rotation_matrix = cv2.getRotationMatrix2D((red_mid1[0], red_mid1[1]), deviation_angle, 1.0)
    dir_vector_red_lines = cv2.transform(np.array([[dir_vector_red_lines]]), rotation_matrix)[0][0]


    red_mid_on_extended1 = find_intersection(red_mid1, dir_vector_red_lines, canvas_width, canvas_height)
    red_mid_on_extended2 = find_intersection(red_mid2, dir_vector_red_lines, canvas_width, canvas_height)

    cv2.line(frame, (extended_lines[0][0], extended_lines[0][1]), (extended_lines[0][2], extended_lines[0][3]), (0, 0, 255), 2)
    cv2.line(frame, (extended_lines[1][0], extended_lines[1][1]), (extended_lines[1][2], extended_lines[1][3]), (0, 0, 255), 2)

    cv2.line(frame, (int(red_mid_on_extended1[0]), int(red_mid_on_extended1[1])), (int(red_mid_on_extended2[0]), int(red_mid_on_extended2[1])), (0, 255, 0), 2)

    green_line_end = midpoint(red_mid_on_extended1, red_mid_on_extended2)

    green_midpoint = midpoint(red_mid_on_extended1, red_mid_on_extended2)

    purple_line_start = find_intersection(green_midpoint, -dir_vector_red_lines, canvas_width, canvas_height)
    purple_line_end = find_intersection((green_midpoint[0] - 2 * dir_vector_red_lines[0] * canvas_width, green_midpoint[1] - 2 * dir_vector_red_lines[1] * canvas_width), -dir_vector_red_lines, canvas_width, canvas_height)
    purple_line_start_far = (purple_line_start[0] + 10 * dir_vector_red_lines[0] * canvas_width, purple_line_start[1] + 10 * dir_vector_red_lines[1] * canvas_width)
    purple_line_end_far = (purple_line_end[0] - 10 * dir_vector_red_lines[0] * canvas_width, purple_line_end[1] - 10 * dir_vector_red_lines[1] * canvas_width)

    cv2.line(frame, (int(purple_line_start_far[0]), int(purple_line_start_far[1])), (int(purple_line_end_far[0]), int(purple_line_end_far[1])), (128, 0, 128), 2)


    mirrored_purple_line_start = mirror_point(purple_line_start_far, (extended_lines[1][0], extended_lines[1][1]), dir_vector_red_lines)
    mirrored_purple_line_end = mirror_point(purple_line_end_far, (extended_lines[1][0], extended_lines[1][1]), dir_vector_red_lines)

    length_of_purple_line = calculate_length(mirrored_purple_line_start[0], mirrored_purple_line_start[1],
                                             mirrored_purple_line_end[0], mirrored_purple_line_end[1])

    cv2.line(frame, (int(mirrored_purple_line_start[0]), int(mirrored_purple_line_start[1])), (int(mirrored_purple_line_end[0]), int(mirrored_purple_line_end[1])), (128, 0, 128), 2)

    purple_line_start, purple_line_end = mirrored_purple_line_start, mirrored_purple_line_end

def mirror_point(point, line_point, line_direction):
    vector_to_point = np.array([point[0] - line_point[0], point[1] - line_point[1]])

    mirrored_vector = np.array([-vector_to_point[0], vector_to_point[1]])

    mirrored_point = line_point + mirrored_vector

    return mirrored_point

def mirror_line_horizontally(line_start, line_end, mirror_point):
    mirrored_line_start = mirror_point(line_start, mirror_point)
    mirrored_line_end = mirror_point(line_end, mirror_point)

    return mirrored_line_start, mirrored_line_end


def find_intersection(point, direction, canvas_width, canvas_height):
    # Find intersection with canvas edges
    t_x_min = (0 - point[0]) / direction[0] if direction[0] != 0 else float('inf')
    t_x_max = (canvas_width - point[0]) / direction[0] if direction[0] != 0 else float('inf')
    t_y_min = (0 - point[1]) / direction[1] if direction[1] != 0 else float('inf')
    t_y_max = (canvas_height - point[1]) / direction[1] if direction[1] != 0 else float('inf')

    t_min = max(min(t_x_min, t_x_max, t_y_min, t_y_max), 0)  # Take the maximum of 0 and the minimum t-value
    intersection = [point[0] + t_min * direction[0], point[1] + t_min * direction[1]]

    return intersection

def filter_lines(lines, width, height, min_distance_factor):
    filtered_lines = []
    for line in lines[:, 0]:
        x1, y1, x2, y2 = line
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        length = np.sqrt((y2 - y1)**2 + (x2 - x1)**2)

        if 30 <= abs(angle) <= 60 and length > 50:
            filtered_lines.append(line)

    min_distance = width * min_distance_factor
    filtered_lines = filter_overlapping_lines(filtered_lines, min_distance, width, height)

    return filtered_lines

def filter_overlapping_lines(lines, min_distance, width, height):
    filtered_lines = []
    for line in lines:
        # Check if the line is far enough from existing lines
        if all(line_distance(line, other_line) > min_distance for other_line in filtered_lines):
            filtered_lines.append(line)
    return filtered_lines

def line_distance(line1, line2):
    # Calculate the distance between the midpoints of two lines
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    mid_x1, mid_y1 = (x1 + x2) / 2, (y1 + y2) / 2
    mid_x2, mid_y2 = (x3 + x4) / 2, (y3 + y4) / 2
    return np.sqrt((mid_x2 - mid_x1)**2 + (mid_y2 - mid_y1)**2)

def select_two_longest_non_parallel(lines):
    # Select the two longest non-parallel lines
    longest_lines = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            if not are_lines_parallel(lines[i], lines[j]):
                longest_lines.extend([lines[i], lines[j]])
                return longest_lines

    return longest_lines

def are_lines_parallel(line1, line2, threshold_angle=5):
    # Check if two lines are parallel within a given threshold angle
    angle1 = np.arctan2(line1[3] - line1[1], line1[2] - line1[0]) * 180 / np.pi
    angle2 = np.arctan2(line2[3] - line2[1], line2[2] - line2[0]) * 180 / np.pi
    return abs(angle1 - angle2) < threshold_angle

def line_length(line):
    if len(line) >= 4:
        x1, y1, x2, y2 = line[:4]
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    else:
        return 0

def draw_line(frame, line):
    x1, y1, x2, y2 = line
    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

def filter_parallel_lines(lines, angle_threshold=10):
    filtered_lines = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            angle_i = np.arctan2(lines[i][0][3] - lines[i][0][1], lines[i][0][2] - lines[i][0][0]) * 180 / np.pi
            angle_j = np.arctan2(lines[j][0][3] - lines[j][0][1], lines[j][0][2] - lines[j][0][0]) * 180 / np.pi

            if abs(angle_i - angle_j) < angle_threshold:
                filtered_lines.append(lines[i])
                filtered_lines.append(lines[j])

    return filtered_lines

def findTwoRectangles(lines, image_width, image_height):
    if lines is not None and len(lines) >= 4:
        line_combinations = list(combinations(lines, 2))

        valid_combinations = []
        for combo in line_combinations:
            line1, line2 = combo

            if not isHorizontal(line1) and not isHorizontal(line2):
                valid_combinations.append(combo)

        if not valid_combinations:
            return None, None

        valid_combinations.sort(key=lambda pair: distance(pair[0][:2], pair[1][:2]), reverse=True)

        left_rectangle, right_rectangle = valid_combinations[:2]
        return np.array(left_rectangle), np.array(right_rectangle)

    return None, None


def formsRectangle(pair):
    # Check if the two lines in the pair form a rectangle
    x1, y1, x2, y2 = pair[0]
    x3, y3, x4, y4 = pair[1]

    side1 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    side2 = np.sqrt((x4 - x3)**2 + (y4 - y3)**2)

    # Check if the sides are approximately equal
    return abs(side1 - side2) < 20


def findTwoLongestPairs(lines, image_width, image_height):
    if lines is not None and len(lines) > 0:
        # Convert the lines to a more convenient format for processing
        lines = [line[0] for line in lines]

        # Filter out horizontal or close-to-horizontal lines
        lines = [line for line in lines if abs(np.arctan2(line[3] - line[1], line[2] - line[0])) < 1.2]

        # Sort lines by their length
        lines = sorted(lines, key=lambda x: np.arctan2(x[0][3] - x[0][1], x[0][2] - x[0][0]))

        # Separate the lines into two groups based on their slope
        left_lane_lines = []
        right_lane_lines = []

        for line in lines:
            x1, y1, x2, y2 = line
            slope = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')

            if slope < 0 and x1 < image_width / 2 and x2 < image_width / 2:
                left_lane_lines.append(line)
            elif slope > 0 and x1 > image_width / 2 and x2 > image_width / 2:
                right_lane_lines.append(line)

        return left_lane_lines[:2], right_lane_lines[:2]  # Return the two longest lines for each lane

    return None, None

def isHorizontal(line):
    try:
        if len(line) != 1:
            x1, y1, x2, y2 = line
        else:
            x1, y1, x2, y2 = line[0]
    except (TypeError, ValueError):
        return False

    if isinstance(x1, np.ndarray):
        x1, y1, x2, y2 = x1[0]

    angle = np.arctan2(y2 - y1, x2 - x1)
    angle = np.degrees(angle)
    return abs(angle) < 45 or abs(angle) > 135


def isLineInProximity(line, point):
    x1, y1, x2, y2 = line
    distance_to_point = min_distance_to_line(point, line)

    return distance_to_point < 50



def is_dark_white(color):
    return color[2] < 200

def findContinuousParallelLines(frame, lines, image_height, image_width):
    if lines is not None and len(lines) > 0:
        lines = [line[0] for line in lines]
        lines.sort(key=lambda l: np.arctan2(l[3] - l[1], l[2] - l[0]))
        lines = [line for line in lines if abs(np.arctan2(line[3] - line[1], line[2] - line[0])) < 1.2]

        valid_lines = [line for line in lines if abs(line[3] - line[1]) > image_height / 2]

        return valid_lines

    return None



def isRectangular(line, frame):
    x1, y1, x2, y2 = line
    line_length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # Set aspect ratio thresholds based on your requirements
    aspect_ratio_min = 0.2
    aspect_ratio_max = 5.0

    # Calculate aspect ratio
    aspect_ratio = line_length / max(frame.shape[1], frame.shape[0])

    # Check if the aspect ratio falls within the desired range
    if aspect_ratio_min < aspect_ratio < aspect_ratio_max:
        # Extract the region enclosed by the bounding box of the line
        roi = frame[int(min(y1, y2)):int(max(y1, y2)), int(min(x1, x2)):int(max(x1, x2))]

        # Convert the region to grayscale
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Apply a threshold to identify white regions
        _, thresh = cv2.threshold(roi_gray, 200, 255, cv2.THRESH_BINARY)

        # Calculate the percentage of white pixels
        white_pixel_percentage = np.count_nonzero(thresh == 255) / (roi.shape[0] * roi.shape[1])

        # Set the threshold for considering it a white lane based on your requirements
        white_threshold = 0.7

        # Check if the percentage of white pixels exceeds the threshold
        return white_pixel_percentage > white_threshold

    return False


def findRoadMiddle(lines, image_width):
    if len(lines) >= 2:
        x_coords = [lines[0][0], lines[0][2], lines[-1][0], lines[-1][2]]

        middle_point_x = sum(x_coords) // len(x_coords)

        return middle_point_x

    return None


def process_frame(frame):
    # Perform your image processing to identify lanes and obtain the 'lines' variable
    lines = identifyLanes(frame, 0.30)

    # Draw the symmetry line and get its coordinates
    draw_symmetry_line(frame, lines, canvas_width, canvas_height)

    # Perform your processing to calculate speed
    calculated_speed = calculateSpeed(purple_line_start, purple_line_end)

    # Update the speed label text
    speed_label.config(text=f"Speed: {calculated_speed}")


def dumpDataClicked():
    global video_player, purple_line_start, purple_line_end, hldb, video_loaded

    if video_player is not None:
        frame = video_player.getFrame()

        if frame is not None:
            script_directory = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
            frame_file_path = os.path.join(script_directory, "headlight_location.png")
            cv2.imwrite(frame_file_path, frame)

            # Process the frame and identify lanes
            lines = identifyLanes(frame_file_path, 0.30)

            # Update the speed label text
            speed_label.config(text=f"Speed: {calculateSpeed(purple_line_start, purple_line_end)}")

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_white = np.array([0, 0, 200], dtype=np.uint8)
            upper_white = np.array([255, 30, 255], dtype=np.uint8)
            white_mask = cv2.inRange(hsv_frame, lower_white, upper_white)
            result_frame = cv2.bitwise_and(frame, frame, mask=white_mask)
            grayscale_frame = cv2.cvtColor(result_frame, cv2.COLOR_BGR2GRAY)
            _, binary_image = cv2.threshold(grayscale_frame, 200, 255, cv2.THRESH_BINARY)
            binary_image = cv2.medianBlur(binary_image, 5)
            contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            detected_headlights = []

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                contour_area = cv2.contourArea(contour)
                if 500 < contour_area < 5000:
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    bounding_box = BoundingBox(top_left, bottom_right)
                    detected_headlights.append(bounding_box)

                    center_x = x + w // 2
                    center_y = y + h // 2
                    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            script_directory = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))

            frame_with_red_dots_path = os.path.join(script_directory, "headlight_location.png")
            cv2.imwrite(frame_with_red_dots_path, frame)

            print(f"Frame with red dots saved at: {frame_with_red_dots_path}")

            if detected_headlights:
                print(f"Headlights detected at: {detected_headlights}")
            else:
                print("No headlights detected.")

            image_with_lanes = identifyLanes(frame_with_red_dots_path, 0.30)

def loadVideoClicked():
    global video_loaded
    global is_video_playing, is_paused
    if is_video_playing and not is_paused[0]:
        video_loaded = True
        schedule.every(1).seconds.do(dumpDataClicked)


def updateLiveStreamButtonColor():
    global is_video_playing, is_paused
    button_color = "#FF0000" if is_video_playing and not is_paused[0] else "#FFFFFF"
    liveStream.config(bg=button_color)

def convertToGrayscale(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale Frame', gray_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return gray_frame
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

   
window = tk.Tk()
window.title("Headlight Detection Software")
window.geometry("928x612")
window.configure(bg="#FFFFFF")


video_canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=612,
    width=928,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
video_canvas.place(x=0, y=0)

video_display = Canvas(
    window,
    bg="#FFFFFF",
    height=287,
    width=488,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
video_display.place(x=354, y=141)


video_canvas.create_rectangle(0.0, 0.0, 220.0, 612.0, fill="#9400D3", outline="")
video_canvas.create_rectangle(220.0, 0.0, 928.0, 612.0, fill="#FFFFFF", outline="")

speed_label = Label(window, text="Speed: N/A", font=("Helvetica", 14), bg="#FFFFFF")
speed_label.place(x=416.9278869628906, y=400)

buttonImageVideoPlayerStart = PhotoImage(file=relativeToAssets("button_1.png"))
videoPlayerStart = Button(image=buttonImageVideoPlayerStart, borderwidth=0, highlightthickness=0, command=lambda: playVideo(video_capture, window, video_display), relief="flat")
videoPlayerStart.place(x=416.9278869628906, y=465.0, width=88.26480102539062, height=79.10787200927734)

buttonImageVideoPlayerPause = PhotoImage(file=relativeToAssets("button_2.png"))
videoPlayerPause = Button(image=buttonImageVideoPlayerPause, borderwidth=0, highlightthickness=0, command=lambda: pauseVideo(), relief="flat")
videoPlayerPause.place(x=553.5960083007812, y=465.0, width=88.26480102539062, height=79.10787200927734)

buttonImageVideoPlayerRewind = PhotoImage(file=relativeToAssets("button_3.png"))
videoPlayerRewind = Button(image=buttonImageVideoPlayerRewind, borderwidth=0, highlightthickness=0, command=rewindVideo, relief="flat")
videoPlayerRewind.place(x=690.2640991210938, y=465.0, width=88.26480102539062, height=79.10787200927734)


buttonImageDumpData = PhotoImage(file=relativeToAssets("button_4.png"))
dumpData = Button(image=buttonImageDumpData, borderwidth=0, highlightthickness=0, command=dumpDataClicked, relief="flat")
dumpData.place(x=19.1009521484375, y=325.5, width=187.29383850097656, height=51.49781799316406)


buttonImageLiveStream = PhotoImage(file=relativeToAssets("button_6.png"))
liveStream = Button(image=buttonImageLiveStream, borderwidth=0, highlightthickness=0, command=lambda: openCam( video_display, window), relief="flat")
liveStream.place(x=846.8172607421875, y=17.0, width=48.081729888916016, height=46.75)

buttonImageLoadVideo = PhotoImage(file=relativeToAssets("button_7.png"))
loadVideo = Button(image=buttonImageLoadVideo, borderwidth=0, highlightthickness=0, command=lambda: openVideo( video_display, window), relief="flat")
loadVideo.place(x=19.0, y=208.0, width=187.29383850097656, height=51.49781799316406)


window.resizable(False, False)


window.mainloop()
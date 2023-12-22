import math
import numpy as np
from PIL import Image, ImageFilter, ImageOps
import matplotlib.pyplot as plt
from PIL.ImageDraw import ImageDraw
from skimage import io, color, filters


# Stage 1: Eliminate the printed text
def remove_printed_text(image_path):
    image = Image.open(image_path)
    gray_image = color.rgb2gray(image)

    # thresholding to remove printed text
    threshold = 200
    thresholded_image = gray_image.point(lambda p: p > threshold and 255)

    # applying morphological operations to remove noise
    cleaned_image = thresholded_image.filter(ImageFilter.MedianFilter(size=3))

    cleaned_image.save('OOP_MT_170317_L077_p1_bin.png')


# Stage 2: Evaluate page features
def evaluate_page_features(cleaned_image_path):
    cleaned_image = Image.open(cleaned_image_path)

    edges = cleaned_image.filter(ImageFilter.FIND_EDGES)
    gray_edges = color.rgb2gray(edges)
    contours, _ = gray_edges.findContours(mode=Image.RETR_EXTERNAL, method=Image.CHAIN_APPROX_SIMPLE)
    draw = ImageDraw.Draw(cleaned_image)

    # iterating through the contours and drawing bounding boxes
    for contour in contours:
        x, y, w, h = contour.bounds
        draw.rectangle([x, y, x + w, y + h], outline=(255, 0, 0))

    cleaned_image.save('evaluated_page_features.png')


# Stage 3: Straight lines in handwriting samples
def detect_straight_lines(cleaned_image_path):
    cleaned_image = Image.open(cleaned_image_path)
    lines = cleaned_image.convert('L').transform((cleaned_image.width,
                                                  cleaned_image.height),
                                                 Image.HOUGH_TRANSFORM_HORIZONTAL)

    lines_binary = lines.point(lambda p: p > 128 and 255)
    contours, _ = lines_binary.findContours(mode=Image.RETR_EXTERNAL, method=Image.CHAIN_APPROX_SIMPLE)
    draw = ImageDraw.Draw(cleaned_image)

    # iterating through the contours and drawing bounding boxes
    for contour in contours:
        x, y, w, h = contour.bounds
        line_length_threshold = 50
        angle_threshold = 10

        if w > line_length_threshold:
            angle = math.degrees(math.atan2(h, w))

            if abs(angle) < angle_threshold:
                draw.rectangle([x, y, x + w, y + h], outline=(0, 0, 255))

    cleaned_image.save('interpreted_lines.png')


# Stage 4: Binary regions in handwriting samples
def binary_regions(cleaned_image_path):
    cleaned_image = Image.open(cleaned_image_path)
    gray_image = color.rgb2gray(cleaned_image)
    threshold = 200
    binary_image = gray_image.point(lambda p: p > threshold and 255)
    kernel_size = 3
    dilated_image = binary_image.filter(ImageFilter.MaxFilter(size=kernel_size))
    eroded_image = dilated_image.filter(ImageFilter.MinFilter(size=kernel_size))

    # finding contours in the eroded image
    contours, _ = eroded_image.findContours(mode=Image.RETR_EXTERNAL, method=Image.CHAIN_APPROX_SIMPLE)

    draw = ImageDraw.Draw(cleaned_image)

    # iterating through the contours and drawing bounding boxes
    for contour in contours:
        x, y, w, h = contour.bounds
        draw.rectangle([x, y, x + w, y + h], outline=(0, 255, 0))

    cleaned_image.save('binary_regions.png')


# Stage 5: Labeled features of specific characters
def label_characters(binary_image_path, original_image_path):
    binary_image = Image.open(binary_image_path)
    original_image = Image.open(original_image_path)
    # finding contours in the binary image
    contours, _ = binary_image.findContours(mode=Image.RETR_EXTERNAL, method=Image.CHAIN_APPROX_SIMPLE)
    draw = ImageDraw.Draw(original_image)
    # iterating through the contours
    for contour in contours:
        x, y, w, h = contour.bounds
        aspect_ratio = w / h
        if 0.8 < aspect_ratio < 1.2:
            label = 'i'
            draw.text((x, y), label, fill=(255, 0, 0), font=None)

    original_image.save('labeled_image.png')


remove_printed_text('OOP_MT_170317_L077_p1.jpg')
evaluate_page_features('OOP_MT_170317_L077_p1_bin.png')
detect_straight_lines('OOP_MT_170317_L077_p1_bin.png')
binary_regions('OOP_MT_170317_L077_p1_bin.png')
label_characters('OOP_MT_170317_L077_p1_bin.png', 'OOP_MT_170317_L077_p1.jpg')


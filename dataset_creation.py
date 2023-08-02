"""
dataset_creation module handles the processing of the dataset
Dataset may include the following:
- images (jpg, png, jpeg)
- videos (mp4)
- pdfs (pdf)

Developed By : Huzaifa Jawad
"""

import numpy as np
import pandas as pd
import os
import cv2
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from pdf2image import convert_from_path

def get_extension(file_path):
    """
    Returns the extension of a file
    """
    return file_path.split(".")[-1]

def get_file_name(file_path):
    """
    Returns the name of a file
    """
    return file_path.split("/")[-1]

def flip_image_horizontally(image):
    """
    Flips an image horizontally
    """
    return cv2.flip(image, 1)

def flip_image_vertically(image):
    """
    Flips an image vertically
    """
    return cv2.flip(image, 0)

def Padding_and_resizing(image, size=224):
    """
    Pads and resizes an image to a specified size
    """
    h, w = image.shape[:2]
    if h > w:
        pad = (h - w) // 2
        image = cv2.copyMakeBorder(image, 0, 0, pad, pad, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    elif w > h:
        pad = (w - h) // 2
        image = cv2.copyMakeBorder(image, pad, pad, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    image = cv2.resize(image, (size, size))
    return image

def compare_ssim(cv2_image1, cv2_image2):
    # Convert images to grayscale if they are color
    if len(cv2_image1.shape) == 3 and cv2_image1.shape[2] == 3:
        cv2_image1 = cv2.cvtColor(cv2_image1, cv2.COLOR_BGR2GRAY)
        cv2_image2 = cv2.cvtColor(cv2_image2, cv2.COLOR_BGR2GRAY)

    # Calculate SSIM
    ssim_score, _ = ssim(cv2_image1, cv2_image2, full=True)

    return ssim_score

def extract_frames_from_video(video_path, size=224, augment = [False, False]):
    """
    Extracts frames from a video and returns a list of frames after every 5 frames
    """
    frames = []
    cap = cv2.VideoCapture(video_path)
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if count % 5 == 0:
                # padding and resizing the frame
                frame = Padding_and_resizing(frame, size)

                # is the previous frame similar to the current frame
                if len(frames) > 0:
                    if augment[0] and augment[1]:
                        if compare_ssim(frames[-3], frame) > 0.80:
                            continue
                    elif (augment[0] and not augment[1]) or (augment[1] and not augment[0]):
                        if compare_ssim(frames[-2], frame) > 0.80:
                            continue
                    else:
                        if compare_ssim(frames[-1], frame) > 0.80:
                            continue
                frames.append(frame)
                if augment[0]:
                    frames.append(flip_image_horizontally(frame))
                if augment[1]:
                    frames.append(flip_image_vertically(frame))
            count += 1
        else:
            break
    cap.release()
    return frames
    

def pdf_to_image(pdf_path, size=224):
    """
    Converts a pdf file to an image and returns the image
    """
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image = np.array(image)
        image = Padding_and_resizing(image, size)
        images[i] = image
    return images


def save_frames(frames, save_path):
    """
    Saves the frames to a specified path
    """
    for i, frame in enumerate(frames):
        cv2.imwrite(os.path.join(save_path, str(i)+".jpg"), frame)

def save_image(image, save_path):
    """
    Saves the image to a specified path
    """
    cv2.imwrite(save_path, image)

def convert_to_dataset(list_of_file_paths, name_of_dataset, augment = [False, False], size=224):
    """
    Converts a list of files to a dataset
    """
    count = 0
    for file_path in list_of_file_paths:
        extension = get_extension(file_path)
        if extension == "pdf":
            images = pdf_to_image(file_path, size)
            for i, image in enumerate(images):
                save_image(image, f"{name_of_dataset}/" + str(count) + str(i)+".jpg")
        elif extension == "jpg" or extension == "jpeg" or extension == "png":
            save_image(Padding_and_resizing(cv2.imread(file_path), size), f"{name_of_dataset}/" + str(count)+ '0' + ".jpg")
        elif extension in ["mp4", "avi", "mov", "webm"]:
            frames = extract_frames_from_video(file_path, size, augment)
            for i, frame in enumerate(frames):
                save_image(frame, f"{name_of_dataset}/" + str(count) + str(i)+".jpg")

        count += 1
            


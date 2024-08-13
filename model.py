import cv2
import numpy as np
import urllib.request
import imutils

def url_to_image(url):
    # Download the image from the URL and convert it to a NumPy array
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def process_image(image):
    # Resize image for easier processing (optional)
    image = imutils.resize(image, width=500)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use edge detection (Canny) to find the person outline
    edges = cv2.Canny(gray, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Assume the largest contour is the person
    largest_contour = max(contours, key=cv2.contourArea)

    # Get the bounding rectangle of the person
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Estimate height, chest, waist, and hips based on bounding box dimensions and ratios
    estimated_height = h  # Height in pixels
    estimated_chest = w * 0.8  # Estimate chest width using a ratio
    estimated_waist = w * 0.7  # Estimate waist width using a ratio
    estimated_hips = w * 0.9  # Estimate hip width using a ratio

    # Convert from pixels to centimeters (requires calibration)
    pixels_to_cm = 0.5  # Example scale factor, adjust based on actual calibration

    estimated_height_cm = estimated_height * pixels_to_cm
    estimated_chest_cm = estimated_chest * pixels_to_cm
    estimated_waist_cm = estimated_waist * pixels_to_cm
    estimated_hips_cm = estimated_hips * pixels_to_cm
    
    return {
        "height": estimated_height_cm,
        "chest": estimated_chest_cm,
        "waist": estimated_waist_cm,
        "hips": estimated_hips_cm
    }


def cal_size(image_url):
    # Convert URL to image
    image = url_to_image(image_url)

    # Process the image
    measurements = process_image(image)
    return measurements

# URL of the image
# image_url = 'https://res.cloudinary.com/dvmk4d0kb/image/upload/v1713056140/6_fpzubi.jpg'

# print(cal_size(image_url))

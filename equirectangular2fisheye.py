import os

import cv2
import numpy as np
from tqdm import tqdm


# Function to convert equirectangular to fisheye with tqdm
def panoramic_to_fisheye(panoramic_image, file_name):
    # Extract the height and width of the panoramic image
    panoramic_height, panoramic_width = panoramic_image.shape[:2]

    # Calculate the dimensions of the fisheye image
    fisheye_height = min(panoramic_height, panoramic_width)  # Set height to be minimum of width and height
    fisheye_width = fisheye_height * 2  # Set width to be twice the height to maintain 2:1 aspect ratio

    # Initialize an empty array to store the fisheye image
    fisheye_image = np.zeros((fisheye_height, fisheye_width, 3), dtype=np.uint8)

    # Calculate fisheye parameters
    center_x = fisheye_width // 2  # Calculate the x-coordinate of the center
    center_y = fisheye_height // 2  # Calculate the y-coordinate of the center
    radius = min(center_x, center_y)  # Calculate the radius of the circular fisheye region

    # Create a binary mask to identify the circular region of interest in the fisheye image
    mask = np.zeros((fisheye_height, fisheye_width), dtype=np.uint8)
    cv2.circle(mask, (center_x, center_y), radius, 255, -1)  # Draw a filled circle on the mask

    # Convert panoramic image to fisheye
    for y in tqdm(range(fisheye_height), desc=f"Converting {file_name}"):
        for x in range(fisheye_width):
            if mask[y, x] == 255:  # Check if the pixel falls within the circular region of interest
                # Calculate polar coordinates
                theta = np.arctan2(y - center_y, x - center_x)  # Angle relative to the center
                rho = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)  # Distance from the center

                # Map polar coordinates to equirectangular coordinates of the panoramic image
                panoramic_x = int((theta / np.pi + 1) * (panoramic_width / 2))  # Map angle to width
                panoramic_y = int((rho / radius) * panoramic_height)  # Map distance to height

                # Handle edge cases where the mapped coordinates may exceed the bounds of the panoramic image
                if panoramic_x >= panoramic_width:
                    panoramic_x = panoramic_width - 1
                if panoramic_y >= panoramic_height:
                    panoramic_y = panoramic_height - 1

                # Copy pixel value from panoramic image to fisheye image
                fisheye_image[y, x] = panoramic_image[panoramic_y, panoramic_x]

    return fisheye_image


# Function to convert equirectangular to fisheye and save fisheye images
def process_equirectangular_images(data_dir):
    # Traverse through directories containing equirectangular images
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith("_equirectangular.jpg"):  # Check if it's an equirectangular image
                # Construct paths
                input_path = os.path.join(root, file)
                output_dir = os.path.join(root, "fisheye_image")
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, file.replace("_equirectangular.jpg", "_fisheye.jpg"))

                # Open equirectangular image
                equirectangular_img = cv2.imread(input_path)

                # Convert equirectangular to fisheye
                fisheye_img = panoramic_to_fisheye(equirectangular_img, file)

                # Save fisheye image
                cv2.imwrite(output_path, fisheye_img)

                # Calculate time statistics
                print(f"\nProcessing {file}")
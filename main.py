import math
import os
import time

from PIL import Image
from tqdm import tqdm

import cubemap2equirectangular as equirectangular
import equirectangular2fisheye as fisheye
import tiles2cubemap as cubemap
from helpers import crop90 as crop

# Global variable to track the number of parent files processed
parent_file_count = 0

# Global variable to track the starting time
start_time = None

# Global variable to track the total number of parent files
total_parent_files = 0


# Function to convert cubemap to equirectangular
def cubemap_to_equirectangular(cube_map, progress_bar):
    output_height = math.floor(cube_map.size[0] / 3)
    output_width = 2 * output_height
    n = math.floor(cube_map.size[1] / 3)

    output_img = Image.new('RGB', (output_width, output_height))

    total_iterations = output_width * output_height  # Calculate total iterations
    progress_bar.total = total_iterations  # Set total iterations for the progress bar

    for ycoord in range(0, output_height):
        for xcoord in range(0, output_width):
            corrx, corry, face = equirectangular.cubemap_to_equirectangular(xcoord,
                                                                            ycoord,
                                                                            output_width,
                                                                            output_height,
                                                                            n)
            output_img.putpixel((xcoord, ycoord), cube_map.getpixel((corrx, corry)))
            progress_bar.update(1)  # Update tqdm progress bar
    return output_img


# Function to process stitched images and save equirectangular images
def process_stitched_images(data_dir):
    global parent_file_count  # Access the global counter variable
    global start_time  # Access the global start time variable
    global total_parent_files  # Access the global total parent files variable

    # Initialize the start time
    start_time = time.time()

    # Traverse through directories containing stitched images
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith("_cubemap_image.jpg"):  # Check if it's a stitched image
                # Count the total number of parent files
                total_parent_files += 1

    # Reset the parent file count
    parent_file_count = 0

    # Traverse through directories containing stitched images
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith("_cubemap_image.jpg"):  # Check if it's a stitched image
                # Print the parent file count to the console
                print(f"\nProcessing parent file {parent_file_count + 1}/{total_parent_files}")

                # Construct paths
                input_path = os.path.join(root, file)
                output_dir = os.path.join(root, "equirectangular_image")
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, file.replace("_cubemap_image.jpg", "_equirectangular.jpg"))

                # Open stitched image
                cube_map = Image.open(input_path)

                # Convert cubemap to equirectangular
                with tqdm(desc=f"Converting {file}", total=0, leave=False) as pbar:
                    output_img = cubemap_to_equirectangular(cube_map, pbar)

                # Save equirectangular image
                output_img.save(output_path)

                output_path_90 = os.path.join(output_dir, file.replace("_cubemap_image.jpg", "_equirectangular_90.jpg"))

                crop.crop_image_upper_half(output_path, output_path_90, quality=100)

                # Increment the parent file count
                parent_file_count += 1

                # Calculate the average time taken per file
                time_elapsed = time.time() - start_time
                avg_time_per_file = time_elapsed / parent_file_count

                # Calculate the remaining time
                remaining_files = total_parent_files - parent_file_count
                remaining_time = avg_time_per_file * remaining_files

                # Print the estimated remaining time to the console
                print(f"Estimated remaining time: {remaining_time} seconds")

    # Calculate total time elapsed
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time elapsed for converting cubemaps into equirectangular images: {total_time} seconds")


# Example usage:
data_dir = "data"  # data directory

cubemap.stitch_images_corrected(data_dir)

process_stitched_images(data_dir)

fisheye.process_equirectangular_images(data_dir)

print("All processes are done.")

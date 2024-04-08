import os
from PIL import Image


def stitch_images_corrected(data_dir):
    # Iterate over all files in the data directory
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith("_raw_B.jpg"):  # Check if the file is a B image
                file_prefix = file.split("_raw_B.jpg")[0]  # Extract the prefix
                image_paths = {
                    'left': os.path.join(root, file_prefix + "_raw_L.jpg"),
                    'top': os.path.join(root, file_prefix + "_raw_U.jpg"),
                    'front': os.path.join(root, file_prefix + "_raw_F.jpg"),
                    'right': os.path.join(root, file_prefix + "_raw_R.jpg"),
                    'back': os.path.join(root, file_prefix + "_raw_B.jpg"),
                    'bottom': os.path.join(root, file_prefix + "_raw_D.jpg")
                }

                # Create the output directory if it doesn't exist
                output_dir = os.path.join(root, "cubemap_image")
                os.makedirs(output_dir, exist_ok=True)

                # Create the save path
                save_path = os.path.join(output_dir, file_prefix + "_cubemap_image.jpg")

                # Call the stitching function
                stitch_images(image_paths, save_path)


def stitch_images(image_paths, save_path):
    # Load the images
    images = {name: Image.open(path) for name, path in image_paths.items()}

    # Assuming all images are the same size
    tile_width, tile_height = images['front'].size

    # Create a new blank image with a size that can hold all six square tiles
    width, height = tile_width * 4, tile_height * 3
    cube_map = Image.new('RGB', (width, height))

    # Paste the images into the cubemap
    cube_map.paste(images['left'], (0, tile_height))
    cube_map.paste(images['top'], (tile_width, 0))
    cube_map.paste(images['front'], (tile_width, tile_height))
    cube_map.paste(images['right'], (tile_width * 2, tile_height))
    cube_map.paste(images['back'], (tile_width * 3, tile_height))
    cube_map.paste(images['bottom'], (tile_width, tile_height * 2))

    # Save the new image
    cube_map.save(save_path)

    return cube_map




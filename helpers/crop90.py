from PIL import Image


def crop_image_upper_half(img_path, output_path, quality=100):
    """
    Crop the upper half of the image and save it with specified quality.

    Args:
        img_path (str): Path to the input image.
        output_path (str): Path to save the cropped image.
        quality (int): Quality of the saved image (0-100), defaults to 100.
    """
    # Load the image
    img = Image.open(img_path)

    # Calculate the dimensions for the cropped image
    width, height = img.size
    new_height = height // 2

    # Crop the image (left, upper, right, lower)
    cropped_img = img.crop((0, 0, width, new_height))

    # # Convert PIL Image to NumPy array
    # cropped_array = np.array(cropped_img)
    #
    # transparent_fisheye_img = remove.remove_black_make_transparent(cropped_array)
    #
    # # Convert NumPy array back to PIL Image
    # transparent_fisheye_img = Image.fromarray(transparent_fisheye_img)

    # Save the cropped image with specified quality
    cropped_img.save(output_path, quality=quality)

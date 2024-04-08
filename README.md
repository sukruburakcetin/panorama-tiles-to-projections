# Panorama Tiles To Projections


The project involves a series of image processing tasks, primarily aimed at handling panoramic images:

### Panorama Tiles Stitching to Create Cubemap Images:
Initially, individual tiles of a panoramic image are stitched together to form cubemap images. These cubemap images typically consist of six faces representing different perspectives of a 360-degree view: top, bottom, front, back, left, and right.

### Processing Cubemap Images to Create Equirectangular Images:
The cubemap images are then processed to generate equirectangular images. Equirectangular projection maps the spherical surface of a scene onto a rectangular image, providing a more standardized format for panoramic images that is commonly used in various applications.

### Bulk Processing with Process Tracking:
The project offers the capability to process multiple cubemap images and equirectangular images in bulk. This bulk processing is implemented with progress tracking, allowing users to monitor the conversion progress as the images are being processed.

### Optional Processing to Fisheye Images:
Additionally, the project includes functionality to further process equirectangular images into fisheye images. Fisheye projection distorts the image to achieve a wide-angle view, often used in virtual reality environments or for artistic effects.

Overall, the project streamlines the conversion and processing of panoramic images through multiple stages, catering to users who work with panoramic imagery in various domains such as virtual reality content creation, immersive media experiences, and panoramic photography. The inclusion of bulk processing and process tracking enhances usability and efficiency, especially when handling large batches of images.






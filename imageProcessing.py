import glob
import os
import shutil

from PIL import Image


def count_white_black_pixels(image_path: str, white_level: int = 225) -> (int, int):
    """
    Counts the number of white and black pixels in an image

    :param image_path: path to the image to evaluate
    :param white_level: level above which we call a pixel 'white' (default 200)
    :return: (number of white pixels, number of black pixels)
    """
    img = Image.open(image_path)
    greyed = img.convert("L")
    white = 0
    width, height = greyed.size
    pixels = width * height

    # Get number of white pixels
    for x in range(width):
        for y in range(height):
            v = greyed.getpixel((x, y))
            if v > white_level:
                white += 1

    black = pixels - white

    return white, black


def filter_image_on_whitespace(image_path: str, threshold: float = 0.95, white_level: int = 200) -> bool:
    """
    Evaluates whether the image has sufficiently low whitespace to include in training.

    :param image_path: path to the image to evaluate
    :param threshold: proportion of white pixels allowed (default 0.95)
    :param white_level: level above which we call a pixel 'white' (default 200)
    :return: True if image accepted, False if rejected
    """
    white, black = count_white_black_pixels(image_path, white_level)
    pixels = white + black
    p = white / float(pixels)

    if p > threshold:
        print("Rejected " + image_path + " white proportion " + str(p))
        return False
    else:
        return True


def filter_folder_on_whitespace(src: str, dst: str, threshold: float = 0.95, white_level: int = 200,
                                regex: str = "*") -> None:
    """
    Copies images in src to dst if they contain enough information

    :param src: source folder containing images
    :param dst: destination folder
    :param threshold: proportion of white pixels allowed (default 0.95)
    :param white_level: level above which we call a pixel 'white' (default 200)
    :param regex: Regular expression to find images in the folder (default * will use all images)
    """
    if os.path.exists(dst):
        print("ERROR in filter_folder_on_whitespace: dst folder already exists")
        return

    os.mkdir(dst)
    files = glob.glob(src + "/" + regex + ".png")
    for i, image_path in enumerate(files):
        if filter_image_on_whitespace(image_path, threshold, white_level):
            shutil.copy(image_path, dst)

    print("Accepted Images copied to " + dst)

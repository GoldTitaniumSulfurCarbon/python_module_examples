from pathlib import Path
def resize(image, x=None, y=None):
    """
    :param image: Image to be resized
    :param x: Width of the image; defaults to base image's width
    :param y: Height of the image; defaults to base image's height
    :return: Image object resized by the given length and width.
    """

    if x is None:
        x = image.width
    if y is None:
        y = image.height
    new_img = image.resize((x, y))

    if hasattr(image, 'filename'):
        #If the image being resized has a filename, give the resized one a new one,
        # identical to the old one, except it says it's resized by the dimensions passed in the arguments.
        old_img = Path(image.filename)
        new_img.filename = f"{old_img.stem}_resized_{x}x{y}{old_img.suffix}"
    return new_img



def image_info(image):
    """
    Gets the image's size, filename, format, and format description
    :param image: PIL.Image object
    :return str: Contains the filesize, filename, file format, and file format's description
    """
    return (f"Filesize: {image.size}"
            f"\nFilename: {image.filename}"
            f"\nFile format: {image.format}"
            f"\nFormat description: {image.format_description}")

def convert_file(image, desired_format, output_directory=Path(__file__).resolve().parent):
    """
    Converts the image into a desired file format, being saved to a given directory.
    :param image: PIL.Image object
    :param desired_format: Desired format of the image, case insensitive. Only accepts formats from PIL.Image.registered_extensions()
    :param output_directory: Desired directory for the output image to go to. Default is the folder where the script is located.
    :return:
    """
    file_name = Path(image.filename).stem #Gets the file name alone from the image.
    image.save(output_directory / f"{file_name}.{desired_format.lower()}", format=desired_format.upper())


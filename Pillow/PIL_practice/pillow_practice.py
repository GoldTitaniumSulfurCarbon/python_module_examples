from PIL import Image
from pathlib import Path
import PIL_helper_methods as PHL
""" Hiearchy of paths:
BASE_DIR: Path containing the project's folder
RESOURCE_DIR: Path that contains input objects, within the project's folder
OUTPUT_DIR: Path that contains output images, within the script's folder
"""
# Mainly just creating practice methods and testing them out here. Want to make them into universal methods later.
def directory_creation(troubleshoot=True):
    global BASE_DIR, RESOURCE_DIR, OUTPUT_DIR
    BASE_DIR = Path(__file__).resolve().parent.parent # Directory where this file is
    #__file__ keyword to get the path of the file, absolute
    #partent method to get the parent of the file.
    if troubleshoot:
        print(BASE_DIR)
        print(BASE_DIR.exists())

    RESOURCE_DIR = BASE_DIR / "resources" # Directory where input files will be.
    if troubleshoot:
        print(RESOURCE_DIR)
        print(RESOURCE_DIR.exists())

    OUTPUT_DIR = BASE_DIR / "Practice" / "outputs" #Directory for where edited images will go to.
    if troubleshoot:
        print(OUTPUT_DIR)
        print(OUTPUT_DIR.exists())
directory_creation(False)
#image1 = Image.open(RESOURCE_DIR / "good_boy.webp")





#Mass conversion of files in the resource directory.
#print(PHL.__file__) #Checking if helper method directory works.
for file in RESOURCE_DIR.iterdir():
    if file.is_file() and (file.suffix.lower() in Image.registered_extensions()): #Checks if the path is a file, and if it's a valid filetype for PIL to operate.
        img = Image.open(file)
        resized = PHL.resize(img, 640, 480)
        PHL.convert_file(resized,"png", OUTPUT_DIR)
        PHL.convert_file(img, "png", OUTPUT_DIR)
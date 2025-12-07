from moviepy import *
from pathlib import Path
import datetime

def time_stamp(seconds, minutes=0, hours=0,
               miliseconds=0):  # Takes in time units and outputs a time in seconds for ease of use.
    return (seconds) + (minutes * 60) + (hours * 3600) + (miliseconds / 1000)

#Declares paths for directories used for input and output, and creates them if they do not exist in this directory where the script is.
input_dir = Path(__file__).resolve().parent / "resources"
output_dir = Path(__file__).resolve().parent / "output"
if not input_dir.exists():
    input_dir.mkdir()
if not output_dir.exists():
    output_dir.mkdir()

#Input and output names for the files.
input_file_name = "{FILE_NAME}.mp4"
output_file_name = f"{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}_{input_file_name}"

input_file = input_dir / input_file_name
output_file = output_dir / output_file_name

# Gets the video to be clipped, and with the timeframe too.
if input_file.exists() and not output_file.exists():
    clip = VideoFileClip(input_file)

    #The main logic here. First paramater is start crop, 2nd is end time of crop.
    clip = clip.subclipped(time_stamp(minutes=35, seconds=50), time_stamp(minutes=37,seconds = 45))
    clip.write_videofile(output_file)
from moviepy import *
from pathlib import Path
import math
import datetime

#Mutation of the clips. At the end of each method, create self to be equal to the clipl then return.

def time_stamp(seconds, minutes=0, hours=0,
               miliseconds=0):
    # Takes in time units and outputs a time in seconds for ease of use.
    return (seconds) + (minutes * 60) + (hours * 3600) + (miliseconds / 1000)


class MoviePyTest:
    def __init__(self, base_clip_filename):
      #Initializes the directories, then creates them if they dont already exist.
        self.base_dir = Path(__file__).resolve().parent #Directory where the script is located
        self.resource_dir = self.base_dir / "resources" #Directory where resources (ie: input videos, watermark fonts), go.
        self.image_dir = self.resource_dir / "images"
        self.font_dir = self.resource_dir / "fonts" #Directory where fonts for watermarks go
        self.input_dir = self.resource_dir / "inputs" #Directory where videos to be edited go
        self.output_dir = self.base_dir / "outputs" #Directory where the edited videos go to.



        for d in self.resource_dir, self.image_dir, self.input_dir, self.font_dir, self.output_dir: #Makes directories
            d.mkdir(exist_ok=True)

        #Declaring input path
        self.base_clip_path = self.input_dir / base_clip_filename
        if not self.base_clip_path.exists():
            raise FileNotFoundError(self.base_clip_path)
        self.clip = VideoFileClip(str(self.base_clip_path)) #Path works, but some weird bugs can occur on Windows with path vs string.

        #Declaring output path
        self.output_clip_filename =  f"{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}_{base_clip_filename}"
        self.output_clip = self.output_dir / self.output_clip_filename

    def preview(self):
        """
        Calls the preview() method of MoviePy clips.
        :return: Preview of the clip.
        """
        self.clip.preview()

    def save(self):
        self.clip.write_videofile(self.output_clip_filename)

    def crop(self, begin_time, end_time): #Crops the given clip from begin time to end time
        """

        :param begin_time: Time(in seconds) where the cropping begins
        :param end_time: Time(in seconds) where the cropping ends
        :return: Base clip with the desired crop
        """
        self.clip = self.clip.subclipped(begin_time, end_time)
        return self


    def create_text_watermark(self,
                              watermark_text,
                              color = "white",
                              text_size=64,
                              font=None,
                              opacity=1,
                              rotation_speed=0,
                              rotation_phase=0
                              ):
        """

        :param watermark_text: The text that the watermark will display.
        :param text_color:  The color of the text; either takes in color keywords, tuple of RGB ints, or hex values. Defaults to white
        :param text_size:  The size of the text; defaults to 64
        :param font: The font of the text, font filetypes such as .otf; defaults to Moviepy's defaults (None)
        :param opacity: Opacity of the text; defaults to 1
        :param rotation_speed: Rotation speed of the text, [ω] = (deg)/(sec). Defaults to 0.
        :param rotation_phase: Phase of the text, [φ] = deg. Defaults to 0.
        :return: Base clip with the desired watermark
        """
        #Using Pythagorean Theorem to create an area for the text to rotate without clipping, used in the clip_size argument for the watermark constructor.
        length, width = self.clip.size
        diagonal = int(math.hypot(length, width))
        clip_size = (diagonal, diagonal)
        #Setting the font type. If the font is None, TextClip constructor will ignore it.
        if font is not None:
            font_path = self.font_dir / font
        else:
            font_path = None

        watermark = (
            TextClip(
                text = watermark_text,
                font_size=text_size,
                font = font_path,
                color = color,
                size = clip_size
            )
            .with_position(("center", "center"))
            .with_duration(self.clip.duration)
            .with_opacity(opacity)
            .rotated(lambda t: (rotation_speed*t) + rotation_phase) #Degrees
        )

        self.clip = CompositeVideoClip(
            [self.clip, watermark],
            size = self.clip.size
        )
        return self

    def create_image_watermark(self, image_name, position=("center", "center")):
        """
        :param image_name: Filename of the image used for the watermark; only takes in the name; so long as it's in the resources/images directory, it will accept.
        :param position: The position of the watermark, in a tuple, (x,y). Defaults to ("center", "center")
        :return: The base clip with the desired watermark
        """

        #Gets the path of the image.
        image_path = self.image_dir / image_name
        image_watermark = (
            ImageClip(image_path)
            .with_duration(self.clip.duration)
            .with_position(position)
        )

        self.clip = CompositeVideoClip(
            [self.clip, image_watermark],
            size = self.clip.size
        )
        return self





to_clip = MoviePyTest("dumbest_australian_shepherd.mp4")

(to_clip.crop(0,12)
 .create_image_watermark("cobson2.png", ("right", "top"))
 .create_image_watermark("good_boy.png",("left", "bottom"))
 .create_text_watermark("TESTING", opacity=.55, rotation_speed=15, rotation_phase=45, color="#8c02d1")
 .save()

 )

#from .images2gif import writeGif
#import images2gif as i2g
import imageio

from PIL import Image, ImageDraw
from trains import settings
pics = settings.BASE_DIR + "\\pics\\"

def something():
    files = []
    image = Image.new("RGBA", (320, 320), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((10, 10, 300, 300), fill="red", outline="red")
    del draw
    image.save(pics + "test0.png", "PNG")
    files.append(pics + "test0.png")

    image = Image.new("RGBA", (320, 320), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((110, 110, 200, 200), fill="green", outline="blue")
    del draw
    image.save(pics + "test1.png", "PNG")
    files.append(pics + "test1.png")

    compose_video(files)

def compose_video(filenames):
    with imageio.get_writer(pics + "movie.gif", mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    #writeGif(pics + "images.gif", filenames, duration=0.3, dither=0)

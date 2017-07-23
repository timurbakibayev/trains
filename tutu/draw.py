#from .images2gif import writeGif
#import images2gif as i2g
import imageio
from django.http import HttpResponse
from tutu.models import Switch
from tutu.models import Track
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


def draw_track(track):
    width = 1000
    height = 50
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle(xy=(-1,height*2/6,width,height*4/6), fill="white", outline="black")
    # draw.ellipse((10, 10, 30, 30), fill="black", outline="green")
    switches = Switch.objects.filter(track_id = track.id)
    draw.rectangle(xy=(0,height/6,1,height*5/6),fill="black")
    for switch in switches:
        pos = switch.position / track.length() * width
        draw.rectangle(xy=(pos - 1, height/6, pos, height*5/6), fill="black")

    del draw
    response = HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response

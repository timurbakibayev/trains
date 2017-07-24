#from .images2gif import writeGif
#import images2gif as i2g
import imageio
import os
from django.http import HttpResponse
from tutu.models import Switch
from tutu.models import Track
from PIL import Image, ImageDraw, ImageFont
from trains import settings
pics = settings.PICS_DIR


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

    compose_video(files, "movie")


def compose_video(files,new_filename):
    with imageio.get_writer(pics + new_filename + ".gif", mode='I', fps=15) as writer:
        for filename in files:
            image = imageio.imread(filename)
            writer.append_data(image)
            os.remove(filename)


def draw_track(track):
    width = 1000
    height = 50
    image = Image.new("RGBA", (int(width*1.1), int(height*1.2)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # draw.ellipse((10, 10, 30, 30), fill="black", outline="green")
    switches = Switch.objects.filter(track_id = track.id)

    text_position_y = height*9/12
    font = ImageFont.truetype("arial.ttf", int(height/3))
    draw.text(xy=(2,text_position_y), text="1", fill="green", font=font)
    last_switch_position = 0
    for i,switch in enumerate(switches):
        x1 = last_switch_position / track.length() * width
        x2 = switch.position / track.length() * width
        if switch.number_of_tracks > 1:
            draw.rectangle(xy=(x1, height * 4 / 12, x2, height * 6 / 12), fill="white", outline="black")
            draw.rectangle(xy=(x1, height * 6 / 12, x2, height * 8 / 12), fill="white", outline="black")
        else:
            draw.rectangle(xy=(x1, height * 5 / 12, x2, height * 7 / 12), fill="white", outline="black")
        draw.rectangle(xy=(x1, height / 6, x1+1, height * 5 / 6), fill="black")
        draw.rectangle(xy=(x2 - 1, height / 6, x2, height * 5 / 6), fill="black")

        pos = switch.position / track.length() * width
        draw.text(xy=(pos+1, text_position_y), text=str(i+2), fill="green", font=font)
        last_switch_position = switch.position
    font = ImageFont.truetype("arial.ttf", int(height/3))
    text_position_y = 0
    last_switch_position = 0
    for i,switch in enumerate(switches):
        text = str(switch.position - last_switch_position) + " км."
        text_length = font.getsize(text=text)[0]
        if text_length > (switch.position - last_switch_position)/track.length() * width:
            text = str(switch.position - last_switch_position)
            text_length = font.getsize(text=text)[0]
        if text_length < (switch.position - last_switch_position) / track.length() * width:
            pos =  int((switch.position + last_switch_position)/2/track.length() * width - int(text_length / 2))
            draw.text(xy=(pos, text_position_y), text=text, fill="black", font=font)
        last_switch_position = switch.position
    del draw
    response = HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response


def all(track, prefix, step, trains, switches):
    width = 1000
    height = 50
    length = track.length()
    image_size = (int(width + 15), int(height * 1.2))
    image = Image.new("RGBA", image_size, (0, 0, 0, 0))
    filename = pics + prefix + str(step) + ".png"
    draw = ImageDraw.Draw(image)
    draw.rectangle(xy=(0,0, image_size[0], image_size[1]), fill="white", outline="white")

    text_position_y = height * 9 / 12
    font = ImageFont.truetype("arial.ttf", int(height / 3))
    draw.text(xy=(2, text_position_y), text="1", fill="green", font=font)
    last_switch_position = 0
    for i, switch in enumerate(switches):
        x1 = last_switch_position / track.length() * width
        x2 = switch.position / track.length() * width
        if switch.number_of_tracks > 1:
            draw.rectangle(xy=(x1, height * 4 / 12, x2, height * 6 / 12), fill="white", outline="black")
            draw.rectangle(xy=(x1, height * 6 / 12, x2, height * 8 / 12), fill="white", outline="black")
        else:
            draw.rectangle(xy=(x1, height * 5 / 12, x2, height * 7 / 12), fill="white", outline="black")
        draw.rectangle(xy=(x1, height / 6, x1 + 1, height * 5 / 6), fill="black")
        draw.rectangle(xy=(x2 - 1, height / 6, x2, height * 5 / 6), fill="black")

        pos = switch.position / track.length() * width
        draw.text(xy=(pos + 1, text_position_y), text=str(i + 2), fill="green", font=font)
        last_switch_position = switch.position
    font = ImageFont.truetype("arial.ttf", int(height / 3))
    text_position_y = 0
    last_switch_position = 0
    for i, switch in enumerate(switches):
        text = str(switch.position - last_switch_position) + " км."
        text_length = font.getsize(text=text)[0]
        if text_length > (switch.position - last_switch_position) / track.length() * width:
            text = str(switch.position - last_switch_position)
            text_length = font.getsize(text=text)[0]
        if text_length < (switch.position - last_switch_position) / track.length() * width:
            pos = int((switch.position + last_switch_position) / 2 / track.length() * width - int(text_length / 2))
            draw.text(xy=(pos, text_position_y), text=text, fill="black", font=font)
        last_switch_position = switch.position

    radius = height/12
    for train in trains:
        x = float(train.position/length*width)
        y = float(height/2)+radius*train.level
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=train.color)

    del draw
    image.save(filename, "PNG")

    return filename

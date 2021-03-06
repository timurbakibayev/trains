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

def compose_video(files,new_filename):
    with imageio.get_writer(os.path.join(settings.PICS_DIR,new_filename + ".gif"), mode='I', fps=15, subrectangles=True) as writer:
        for filename in files:
            image = imageio.imread(filename)
            writer.append_data(image)
            os.remove(filename)

font_file = os.path.join(settings.BASE_DIR, "arial.ttf")

#font_file = "/arial.ttf"


def draw_track(track):
    width = 1000
    height = 50
    image = Image.new("RGBA", (int(width*1.1), int(height*1.2)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # draw.ellipse((10, 10, 30, 30), fill="black", outline="green")
    switches = Switch.objects.filter(track_id = track.id)

    text_position_y = height*9/12
    print(font_file)
    font = ImageFont.truetype(font_file, int(height/3))
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
    font = ImageFont.truetype(font_file, int(height/3))
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
    image_size = (int(width + height/5), int(height * 2.5))
    image = Image.new("RGBA", image_size, (0, 0, 0, 0))
    filename = os.path.join(settings.PICS_DIR, prefix + str(step) + ".png")

    draw = ImageDraw.Draw(image)
    draw.rectangle(xy=(0,0, image_size[0], image_size[1]), fill="white", outline="white")

    text_position_y = height * 9 / 12
    font = ImageFont.truetype(font_file, int(height / 3))
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
    font = ImageFont.truetype(os.path.join(settings.BASE_DIR,"arial.ttf"), int(height / 3))
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
    finished_fw = 0
    finished_bk = 0
    on_way = 0
    for train in trains:
        if train.running:
            on_way += 1
            x = float(train.position/float(length)*width)
            y = float(height/2)+radius*train.level
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=train.color)
        if train.finished:
            if train.dx > 0:
                finished_fw += 1
            else:
                finished_bk += 1

    progress_hrs = str(step // 60)
    progress_min = str(step % 60)
    progress_text = "Время: " + progress_hrs.zfill(2) + ":" + progress_min.zfill(2)
    draw.text(xy=(10, height), text=progress_text, fill="black", font=font)
    progress_text = "Время: " + progress_hrs.zfill(2) + ":" + progress_min.zfill(2)
    draw.text(xy=(10, height + height/3), text="В пути: " + str(on_way) + " поездов", fill="black", font=font)
    draw.text(xy=(10, height + height/3 * 2), text="Доехало: " +
                                                   str(finished_fw) + "/" +
                                                   str(finished_bk),
              fill="black", font=font)

    del draw
    image.save(filename, "PNG")

    return filename

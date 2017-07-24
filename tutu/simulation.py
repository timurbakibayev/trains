from background_task import background
from datetime import datetime
from django.contrib.auth.models import User
from tutu.models import Track
from tutu.models import Switch
from tutu import draw
import random

@background(schedule=2)
def start_sim(track_id):
    print("Started simulation for " + str(track_id))
    # lookup user by id and send them a message
    prefix = ''.join(random.choice('abcd') for _ in range(5))
    track = Track.objects.get(pk=track_id)
    simulate(track, prefix)
    track.simulation_in_progress = False
    track.simulation_filename = prefix + ".gif"
    track.simulation_date_time = datetime.now()
    track.save()


class Train:
    global switches_global, trains

    def __init__(self, dx):
        self.dx = dx
        self.position = 0
        self.waiting = True
        self.station = None
        self.switch = None
        self.going_to_station = 0
        self.color = (125,125,0,255)
        self.level = 0


def simulate(track, prefix):
    one_train = Train(1)
    switches = Switch.objects.filter(track_id=track.id)
    global switches_global, trains
    length = track.length()
    trains = [one_train]
    files = []
    number_of_steps_to_simulate = 1000
    for step in range(number_of_steps_to_simulate):
        if step % 300 == 0:
            track.simulation_progress = int(step/number_of_steps_to_simulate*100/2)
            track.save()
        for one_train in trains:
            if 0 < one_train.position+one_train.dx < length:
                if one_train.switch is None or one_train.switch.number_of_tracks == 0:
                    one_train.level = 0
                else:
                    one_train.level = (-1,1)[one_train.dx>0]
        if step%4 == 0:
            files.append(draw.all(track, prefix, step, trains, switches))
    draw.compose_video(files, prefix)

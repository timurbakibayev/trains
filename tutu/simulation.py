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
    def __init__(self, dx):
        self.dx = dx
        self.position = 0
        self.switch_position_0_to_1 = 0
        self.running = False
        self.finished = False
        self.minutes_in_way = 0
        self.waiting = True
        self.station = None
        self.switch = None
        self.next_switch = None
        self.color = (random.randint(50,230),random.randint(50,230),random.randint(50,230),255)
        self.level = 0

    def reset_minutes_in_way(self):
        self.minutes_in_way = 0

    def inc_minutes_in_way(self):
        self.minutes_in_way += 1

    def set_switch_position_0_to_1(self, new_value):
        self.switch_position_0_to_1 = new_value

    def set_position(self, position):
        self.position = position

    def set_switch(self, switch):
        self.switch = switch

    def set_next_switch(self, switch):
        self.next_switch = switch

    def set_running(self, running):
        self.running = running

    def set_finished(self, finished):
        self.finished = finished

    def set_level(self, level):
        self.level = level


def simulate(track, prefix):
    switches = Switch.objects.filter(track_id=track.id)
    first_switch = None
    last_switch = None
    prev_sw = {}
    next_sw = {}
    start_position = {}
    prev_switch = None
    for switch in switches:
        if first_switch is None:
            start_position[switch.id] = 0
            first_switch = switch
            prev_sw[switch.id] = None
        else:
            start_position[switch.id] = prev_switch.position
            prev_sw[switch.id] = prev_switch
            next_sw[prev_switch.id] = switch
        last_switch = switch
        prev_switch = switch
    print("Start positions", start_position)
    next_sw[last_switch.id] = None
    trains = []
    length = track.length()
    for i in range(200):
        train = Train((1,-1)[i % 2])
        train.next_switch = (first_switch,last_switch)[i % 2]
        trains.append(train)
    files = []
    number_of_steps_to_simulate = 60*24 #60*24
    for step in range(number_of_steps_to_simulate):
        if step % 100 == 0:
            track.simulation_progress = int(step/number_of_steps_to_simulate*100/1.2)
            track.save()
        # ----------------------------------------- Simulation <

        # ----------- if train is waiting, check if next_switch is free <
        for train in trains:
            if train.switch is None and not train.finished:
                switch_is_busy = False
                for train1 in trains:
                    if train1.switch == train.next_switch and train.next_switch is not None:
                        if train.next_switch.number_of_tracks == 1 or (train.dx == train1.dx and train1.minutes_in_way < 8):
                            switch_is_busy = True
                if not switch_is_busy:
                    train.set_switch(train.next_switch)
                    train.set_switch_position_0_to_1((0,1)[train.dx < 0])
                    train.reset_minutes_in_way()
                    if train.switch is None:
                        train.set_finished(True)
                        train.set_running(False)
                    else:
                        train.set_running(True)
                    if train.switch is not None:
                        if train.dx > 0:
                            train.set_next_switch(next_sw[train.switch.id])
                        else:
                            train.set_next_switch(prev_sw[train.switch.id])
        # ----------- if train is waiting, check if next_switch is free />
        # ----------- if train is on switch and running, progress <
        for train in trains:
            if train.switch is not None:
                train.set_switch_position_0_to_1(train.switch_position_0_to_1 + train.dx /
                                                 ((train.switch.mins_main_fw,train.switch.mins_main_bk)[train.dx<0] +
                                                  train.switch.mins_acc +
                                                  train.switch.mins_brk))
                if train.switch_position_0_to_1 < 0 or train.switch_position_0_to_1 > 1:
                    train.set_switch(None)
                if train.switch is not None:
                    r = train.switch_position_0_to_1
                    start = float(start_position[train.switch.id])
                    train.set_position(start + r*(float(train.switch.position) - float(start)))
                    train.inc_minutes_in_way()
                    if train.switch.number_of_tracks > 1:
                        train.set_level((-1,1)[train.dx < 0])
                    else:
                        train.set_level(0)
        # ----------- if train is on switch and running, progress />
        # ----------------------------------------- Simulation />
        if step % 3 == 0:
            files.append(draw.all(track, prefix, step, trains, switches))
    for i in range(20):
        files.append(draw.all(track, prefix+"_p_"+str(i), number_of_steps_to_simulate, trains, switches))
    draw.compose_video(files, prefix)

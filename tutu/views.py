from django.shortcuts import render
from django.http import HttpResponseRedirect
from tutu.models import Track
from django.views.decorators.csrf import csrf_exempt
from tutu.models import Switch
from tutu import draw


def index(request):
    tracks = Track.objects.all()
    # draw.something()
    tracks_plus = []
    for track in tracks:
        t = {"id": track.id, "name": track.name, "start_name": track.start_name}
        t["length"] = track.length()
        tracks_plus.append(t)
    context = {"tracks": tracks_plus}
    return render(request, 'index.html', context)


def reset(request):
    tracks = Track.objects.all()
    for i in tracks:
        i.simulation_in_progress = False
        i.save()
    # draw.something()
    tracks_plus = []
    for track in tracks:
        t = {"id": track.id, "name": track.name, "start_name": track.start_name, "length": track.length()}
        tracks_plus.append(t)
    context = {"tracks": tracks_plus}
    return render(request, 'index.html', context)


def new_track(request):
    context = {}
    if request.method == "POST":
        track_name = request.POST["track_name"]
        if (track_name is None) or (track_name == ""):
            return render(request, "new_tarif.html", context)
        t = Track()
        t.name = track_name
        t.start_name = request.POST["track_start_name"]
        t.length = 0
        try:
            t.length = float(request.POST["track_length"])
        except:
            pass
        t.save()
        return HttpResponseRedirect("/")
    return render(request, 'new_track.html', context={})


def new_switch(request, track_id):
    try:
        track = Track.objects.get(pk=int(track_id))
    except:
        return render(request, "error.html")
    context = {"track": track}
    if request.method == "POST":
        switch_name = request.POST["switch_name"]
        if (switch_name is None) or (switch_name == ""):
            return render(request, "new_switch.html", context)
        s = Switch()
        s.track_id = track.id
        s.name = switch_name
        try:
            s.position = float(request.POST["switch_position"])
        except:
            s.position = 0
        try:
            s.mins_acc = float(request.POST["switch_acc"])
        except:
            s.mins_acc = 0
        try:
            s.mins_main_fw = float(request.POST["switch_main_fw"])
        except:
            s.mins_main_fw = 0
        try:
            s.mins_main_bk = float(request.POST["switch_main_bk"])
        except:
            s.mins_main_bk = 0
        try:
            s.mins_station = float(request.POST["switch_station"])
        except:
            s.mins_station = 0
        try:
            s.mins_brk = float(request.POST["switch_brk"])
        except:
            s.mins_brk = 0
        try:
            s.number_of_tracks = float(request.POST["switch_number_of_tracks"])
        except:
            pass
        try:
            s.trains_fit = float(request.POST["switch_trains_fit"])
        except:
            pass
        s.save()
        return HttpResponseRedirect("/track/" + track_id)
    return render(request, 'new_switch.html', context=context)


@csrf_exempt
def edit_track(request, track_id):
    try:
        t = Track.objects.get(pk=int(track_id))
    except:
        return render(request, "error.html")
    context = {"track": t}
    if request.method == "POST":
        track_name = request.POST["track_name"]
        if (track_name is None) or (track_name == ""):
            pass
        else:
            t.name = track_name
            t.start_name = request.POST["track_start_name"]
            t.length = 0
            try:
                t.length = float(request.POST["track_length"])
            except:
                pass

            try:
                t.number_of_passenger_trains = float(request.POST["number_of_passenger_trains"])
            except:
                pass

            try:
                t.number_of_cargo_trains = float(request.POST["number_of_cargo_trains"])
            except:
                pass

            try:
                t.density_netto = float(request.POST["density_netto"])
            except:
                pass

            t.save()
            return HttpResponseRedirect("/")
    return render(request, "edit_track.html", context)


@csrf_exempt
def delete_track(request, track_id):
    try:
        t = Track.objects.get(pk=int(track_id))
    except:
        return render(request, "error.html")
    context = {"track": t}
    if request.method == "POST":
        t.delete()
        return HttpResponseRedirect("/")
    return render(request, "delete_track.html", context)


@csrf_exempt
def delete_switch(request, track_id, switch_id):
    try:
        t = Track.objects.get(pk=int(track_id))
        s = Switch.objects.get(pk=int(switch_id))
    except:
        return render(request, "error.html")
    context = {"switch": s, "track": t}
    if request.method == "POST":
        s.delete()
        return HttpResponseRedirect("/track/" + track_id)
    return render(request, "delete_switch.html", context)


@csrf_exempt
def edit_switch(request, track_id, switch_id):
    try:
        t = Track.objects.get(pk=int(track_id))
        s = Switch.objects.get(pk=int(switch_id))
    except:
        return render(request, "error.html")
    context = {"switch": s, "track": t}
    if request.method == "POST":
        switch_name = request.POST["switch_name"]
        if (switch_name is None) or (switch_name == ""):
            pass
        else:
            s.name = switch_name
            try:
                s.position = float(request.POST["switch_position"])
            except:
                pass
            try:
                s.mins_acc = float(request.POST["switch_acc"])
            except:
                s.mins_acc = 0
            try:
                s.mins_main_fw = float(request.POST["switch_main_fw"])
            except:
                s.mins_main_fw = 0
            try:
                s.mins_main_bk = float(request.POST["switch_main_bk"])
            except:
                s.mins_main_bk = 0
            try:
                s.mins_brk = float(request.POST["switch_brk"])
            except:
                s.mins_brk = 0
            try:
                s.mins_station = float(request.POST["switch_station"])
            except:
                s.mins_station = 0
            try:
                s.number_of_tracks = float(request.POST["switch_number_of_tracks"])
            except:
                pass
            try:
                s.trains_fit = float(request.POST["switch_trains_fit"])
            except:
                pass
            s.save()
            return HttpResponseRedirect("/track/" + track_id)
    return render(request, "edit_switch.html", context)


def round(a):
    return "%.3f" % a


@csrf_exempt
def show_track(request, track_id):
    try:
        track = Track.objects.get(pk=int(track_id))
        switches_orig = Switch.objects.filter(track_id=track_id)
    except:
        return render(request, "error.html")
    switches = []

    prev_pos = 0
    worst = 1000
    for i, switch in enumerate(switches_orig):
        new_sw = {"switch": switch, "sum":
            switch.mins_acc + switch.mins_brk + switch.mins_main_fw +
            switch.mins_main_bk + switch.mins_station}
        single = int((60 * 23) * 0.96 / new_sw["sum"])
        double = single * int(new_sw["sum"] / 8)
        new_sw["capacity"] = (double, single)[switch.number_of_tracks < 2]
        new_sw["number"] = i + 2
        length = switch.position - prev_pos
        new_sw["length"] = length
        time = new_sw["sum"] / 60
        new_sw["speed"] = int(float(length) / time * 10) / 10
        new_sw["nalich"] = new_sw["capacity"] - \
                           (((track.number_of_cargo_trains + track.number_of_passenger_trains) / 0.85) -
                            (track.number_of_cargo_trains + track.number_of_passenger_trains)) - track.number_of_passenger_trains
        new_sw["potreb"] = (track.number_of_cargo_trains + track.number_of_passenger_trains) / 0.85
        new_sw["reserve_pairs"] = new_sw["nalich"] - new_sw["potreb"]
        new_sw["train_weight"] = (track.density_netto * 1000000) / track.number_of_cargo_trains / 365
        new_sw["reserve_cargo"] = new_sw["train_weight"] * new_sw["reserve_pairs"] * 365 / 1000000
        new_sw["reserve_cargo_f"] = new_sw["reserve_cargo"]
        if new_sw["reserve_cargo_f"] < worst:
            worst = new_sw["reserve_cargo_f"]
        new_sw["positive"] = new_sw["reserve_cargo"] > 0
        new_sw["nalich"] = round(new_sw["nalich"])
        new_sw["potreb"] = round(new_sw["potreb"])
        new_sw["reserve_pairs"] = round(new_sw["reserve_pairs"])
        new_sw["reserve_cargo"] = round(new_sw["reserve_cargo"])
        new_sw["train_weight"] = round(new_sw["train_weight"])
        switches.append(new_sw)
        prev_pos = switch.position

    switches_last_stage = []
    for i in switches:
        i["worst"] = (i["reserve_cargo_f"] == worst)
        switches_last_stage.append(i)


    context = {"track": track, "switches": switches_last_stage}

    return render(request, "show_track.html", context)


def thumbnail_track(request, track_id):
    try:
        track = Track.objects.get(pk=int(track_id))
    except:
        return render(request, "error.html")
    return draw.draw_track(track)

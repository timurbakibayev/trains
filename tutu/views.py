from django.shortcuts import render
from django.http import HttpResponseRedirect
from tutu.models import Track
from django.views.decorators.csrf import csrf_exempt
from tutu.models import Switch
from tutu import draw


def index(request):
    tracks = Track.objects.all()
    # draw.something()
    context = {"tracks": tracks}
    return render(request, 'index.html', context)


def new_track(request):
    context = {}
    if request.method == "POST":
        track_name = request.POST["track_name"]
        if (track_name is None) or (track_name == ""):
            return render(request, "new_tarif.html", context)
        t = Track()
        t.name = track_name
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
        return render(request, "newevent_result.html")
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
            s.mins_main = float(request.POST["switch_main"])
        except:
            s.mins_main = 0
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
        return render(request, "newevent_result.html")
    context = {"track": t}
    if request.method == "POST":
        track_name = request.POST["track_name"]
        if (track_name is None) or (track_name == ""):
            pass
        else:
            t.name = track_name
            t.length = 0
            try:
                t.length = float(request.POST["track_length"])
            except:
                pass
            t.save()
            return HttpResponseRedirect("/")
    return render(request, "edit_track.html", context)


@csrf_exempt
def edit_switch(request, switch_id):
    try:
        s = Switch.objects.get(pk=int(switch_id))
    except:
        return render(request, "newevent_result.html")
    context = {"switch": s}
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
                s.mins_main = float(request.POST["switch_main"])
            except:
                s.mins_main = 0
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
            return HttpResponseRedirect("/")
    return render(request, "edit_switch.html", context)


@csrf_exempt
def show_track(request, track_id):
    try:
        track = Track.objects.get(pk=int(track_id))
        switches_orig = Switch.objects.filter(track_id=track_id)
    except:
        return render(request, "newevent_result.html")
    switches = []

    for switch in switches_orig:
        new_switch = {}
        new_switch["switch"] = switch
        new_switch["sum"] = switch.mins_acc + switch.mins_brk + switch.mins_main
        new_switch["capacity"] = new_switch["sum"] + 1
        switches.append(new_switch)

    context = {"track": track, "switches": switches}

    return render(request, "show_track.html", context)

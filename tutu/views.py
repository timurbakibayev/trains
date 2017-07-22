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

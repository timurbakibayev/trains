from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from tutu.models import Track
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from tutu.models import Switch
from tutu import draw
from django.shortcuts import render
from django.db.models import Q
from django.utils.datetime_safe import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils.deprecation import MiddlewareMixin
from tutu import simulation as sim

from trains import settings
import os

class DisableCsrfCheck(MiddlewareMixin):
    def process_request(self, req):
        attr = '_dont_enforce_csrf_checks'
        if not getattr(req, attr, False):
            setattr(req, attr, True)


@api_view(['GET', 'POST'])
@permission_classes([])
@method_decorator(csrf_exempt, name='dispatch')
def simulation(request, track_id):
    if request.method == 'GET':
        return Response({"detail","no content"})

    elif request.method == 'POST':
        data = request.data
        if "track_id" in data:
            track = Track.objects.get(pk=track_id)
            if not track.simulation_in_progress:
                track.simulation_in_progress = True
                try:
                    os.remove(settings.PICS_DIR + track.simulation_filename)
                except:
                    pass
                track.simulation_filename = ""
                track.save()
                return Response({"detail","simulation started"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail", "Симуляция уже в процессе"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail","Track is not defined"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
@method_decorator(csrf_exempt, name='dispatch')
def simulation_start(request, track_id):
    if request.method == 'POST':
        data = request.data
        if "track_id" in data:
            sim.start_sim(track_id)
        return Response({"detail","Started"}, status=status.HTTP_201_CREATED)
    return Response({"detail", "Only POST allowed"}, status=status.HTTP_400_BAD_REQUEST)


def serve_upload_files(request, file_url):
    import os.path
    import mimetypes
    mimetypes.init()

    try:
        file_path = settings.BASE_DIR + "\\pics\\" + file_url
        fsock = open(file_path,"r")
        #file = fsock.read()
        #fsock = open(file_path,"r").read()
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        print("file size is: " + str(file_size))
        mime_type_guess = mimetypes.guess_type(file_name)
        if mime_type_guess is not None:
            response = HttpResponse(fsock, content_type='image/gif')
        response['Content-Disposition'] = 'attachment; filename=' + file_name
    except IOError:
        response = HttpResponseNotFound()
    return response

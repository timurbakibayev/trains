from background_task import background
from django.contrib.auth.models import User
from tutu.models import Track
from tutu.models import Switch


@background(schedule=2)
def start_sim(track_id):
    print("Started simulation for " + str(track_id))
    # lookup user by id and send them a message
    track = Track.objects.get(pk=track_id)
    track.simulation_in_progress = False
    track.save()

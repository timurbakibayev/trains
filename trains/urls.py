"""trains URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from tutu import views
from tutu import views_sim
from django.views.static import serve
from trains import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),
    url(r'^track/new/$', views.new_track, name='new_track'),
    url(r'^track/edit/(?P<track_id>[0-9]*)$', views.edit_track, name="edit_track"),
    url(r'^track/delete/(?P<track_id>[0-9]*)$', views.delete_track, name="delete_track"),
    url(r'^track/(?P<track_id>[0-9]*)/switch/edit/(?P<switch_id>[0-9]*)$', views.edit_switch, name="edit_switch"),
    url(r'^track/(?P<track_id>[0-9]*)/switch/delete/(?P<switch_id>[0-9]*)$', views.delete_switch, name="delete_switch"),
    url(r'^track/(?P<track_id>[0-9]*)$', views.show_track, name="show_track"),
    url(r'^track/(?P<track_id>[0-9]*)/thumbnail$', views.thumbnail_track, name="thumbnail_track"),
    url(r'^track/(?P<track_id>[0-9]*)/new_switch$', views.new_switch, name="new_switch"),
    url(r'^track/(?P<track_id>[0-9]*)/simulation/$', views_sim.simulation, name="simulation"),
    url(r'^reset$', views.reset, name="reset"),
    url(r'^serve/(?P<path>.*)$', serve, {'document_root': settings.PICS_DIR}),
    url(r'^files/(?P<file_url>.*)$', views_sim.serve_upload_files, name="file"),
    url(r'^track/(?P<track_id>[0-9]*)/simulation_start/$', views_sim.simulation_start, name="simulation_start"),
]

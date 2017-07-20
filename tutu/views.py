from django.shortcuts import render
from tutu import draw

def index(request):
    draw.something()
    context = {}
    return render(request, 'index.html', context)




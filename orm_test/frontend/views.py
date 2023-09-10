from django.shortcuts import render
from backend.src.auxiliary.websocket import ApiRequestConsumer
from django.http import HttpResponse

def main(request):
    return render(request, 'frontend/main.html')

def derivative_constellium(request):
    return render(request, 'frontend/derivative_constellium.html')

def refresh(request):
    ApiRequestConsumer.informCacheInvalid("/api/project/")
    return HttpResponse('<h1>refresh</h1>')
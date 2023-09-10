from django.shortcuts import render
from frontend.consumers import ApiRequestConsumer
from django.http import HttpResponse

def main(request):
    return render(request, 'frontend/main.html')

def refresh(request):
    ApiRequestConsumer.sendToAllConsumers("/api/project/")
    return HttpResponse('<h1>refresh</h1>')
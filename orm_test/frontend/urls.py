from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('derivative_constellium/', views.derivative_constellium, name='derivative_constellium'),
]
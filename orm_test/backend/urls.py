from django.urls import path
from . import views

urlpatterns = [
    path('project/', views.getProject_list),
    path('project/<int:project_group_id>', views.getProject_detail),
    path('derivative_constellium/', views.getDerivativeConstellium_list),
    path('derivative_constellium/<int:derivative_constellium_group_id>', views.getDerivativeConstellium_detail),
]

from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect, JsonResponse
from backend.src.auxiliary.info_handler import handleManagerRequestMethods_list, handleManagerRequestMethods_detail
from backend.src.info.project_info import serializeProject
from backend.src.manager import ProjectManager


@api_view(['GET', 'POST'])
def getProject_list(request):
    return handleManagerRequestMethods_list(
        request, 
        ProjectManager, 
        serializeProject
    )

@api_view(['GET', 'PUT', 'DELETE'])
def getProject_detail(request, project_group_id):
    return handleManagerRequestMethods_detail(
        request, 
        ProjectManager, 
        project_group_id, 
        serializeProject
    )

@api_view(['GET', 'POST'])
def getDerivativeConstellium_list(request):
    return handleManagerRequestMethods_list(
        request, 
        ProjectManager, 
        serializeProject
    )

@api_view(['GET', 'PUT', 'DELETE'])
def getDerivativeConstellium_detail(request, derivative_constellium_group_id):
    return handleManagerRequestMethods_detail(
        request,
        ProjectManager,
        derivative_constellium_group_id,
        serializeProject
    )
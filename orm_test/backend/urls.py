from backend.src.info import *

info_list = [
    ProjectInfo,
    DerivativeConstelliumInfo,
]

def createUrls():
    urlpatterns = []
    for info_class in info_list:
        urlpatterns += info_class.getUrlList()
    return urlpatterns

urlpatterns = createUrls()


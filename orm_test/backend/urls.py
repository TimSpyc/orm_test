from backend.src.info import *

urlpatterns = [
    *ProjectInfo._getUrl(),
    *DerivativeConstelliumInfo._getUrl(),
]
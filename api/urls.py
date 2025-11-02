from django.urls import include, path
from rest_framework import routers

from .views import RideUserViewset

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', RideUserViewset)

urlpatterns = [
    path('', include(router.urls))
]
from django.urls import include, path
from rest_framework import routers

from .views import RideUserViewset, RideViewset, RideEventViewset

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', RideUserViewset)
router.register('rides', RideViewset)
router.register('ride_events', RideEventViewset, basename='rideevent')

urlpatterns = [
    path('', include(router.urls)),
]
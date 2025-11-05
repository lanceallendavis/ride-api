from django.urls import include, path
from rest_framework import routers

from .views import RideUserViewset, RideViewset

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', RideUserViewset)
router.register('rides', RideViewset)

urlpatterns = [
    path('', include(router.urls)),
]
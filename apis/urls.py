from django.urls import path

from .views import getResponse

urlpatterns = [
    path("", getResponse),
]

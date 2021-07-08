from django.urls import path

from .views import generatePage, reportPage

urlpatterns = [
    path("reports/<slug:id>", reportPage),
    path("generate-report", generatePage),
]

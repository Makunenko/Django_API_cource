
from django.conf.urls import url

from .views import (
    UpdateModelDetailAPIview,
    UpdateModelListAPIview
)

urlpatterns = [
    url(r'^(?P<id>\d+)/$', UpdateModelDetailAPIview.as_view()),
    url(r'^$', UpdateModelListAPIview.as_view())
]

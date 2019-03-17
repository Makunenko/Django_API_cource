from django.conf.urls import url
from samples.views import SamplesListView, SystemListView, SampleDetailView
from .views import SampleModelDetailAPIView, SampleModelListAPIView

urlpatterns = [
    url(r'^$', SampleModelListAPIView.as_view()),
    url(r'^(?P<system_id>[\w-]+)/(?P<sample_treatment>[\w-]+)/$', SampleModelDetailAPIView.as_view())

]
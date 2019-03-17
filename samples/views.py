from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.core.serializers import serialize

from .models import Sample as SampleModel

class SamplesListView(View):
    '''
    View of all samples
    '''
    def get(self, request, *args, **kwargs):
        obj = SampleModel.samples.all()
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type='application/json')

class SystemListView(View):
    '''
    View of all samples in one system
    '''
    def get(self, request, system_id=None, *args, **kwargs):
        '''
        какого это хера пока не добавил systemid=None это говно не работало?
        это ведь КВАРГ его было видно print(kwargs).... так хуле???

        в примере по курсу такое говно не происходило
        а ну блять... ясен хуй. я там же это ИД задавал в коде, а не урл
        '''
        obj = SampleModel.samples.filter(system_id=system_id)
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type='application/json')


class SampleDetailView(View):
    '''
    View for single sample
    '''
    def get(self,request, system_id=None, sample_treatment=None, *args, **kwargs):
        '''
        ннада указать систему и обработку
        '''
        sample_treatment = sample_treatment.replace('-', ' ')
        obj = SampleModel.samples.get(system_id=system_id, sample_treatment__iexact=sample_treatment) # сделать бы независимым от lower/upper
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type='application/json')



import json # 2
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import View # 3
from django.core.serializers import serialize

from drestapi.mixins import JsonResponseMixin

from .models import Update

def json_example_view(request):
    data = {
        "count" : 10000,
        'content' : 'blablabla',
        'auaa' : 'qwerty'
    }
    json_data = json.dumps(data) # 2
    # return JsonResponse(data)
    return HttpResponse(json_data, content_type='application/json') # 2

class JsonCBV(View):
    def get(self, request, *args, **kwargs):
        data = {
            "count": 10000,
            'content': 'blablabla',
            'auaa': 'qwerty'
        }
        return JsonResponse(data)



class JsonCBV2(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs): #chto visivaet etot metod?
        data = {
            "count": 10000,
            'content': 'blablabla',
            'auaa': 'qwerty'
        }
        return self.render_to_json_response(data)

class SerializedDetailView(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs): #chto visivaet etot metod?
        obj = Update.objects.get(id=1) # ebanoe id
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type="application/json")


class SerializedListView(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs): #chto visivaet etot metod?
        qs = Update.objects.all()
        # data = serialize("json", qs, fields=("user", "content"))
        # # data = {
        # #     "user" : obj.user.username,
        # #     "content" : obj.content
        # # }
        # # return self.render_to_json_response(data)
        # json_data = data
        json_data = Update.objects.all().serialize()
        return HttpResponse(json_data, content_type="application/json")
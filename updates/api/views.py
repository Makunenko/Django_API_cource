import json

from updates.models import Update as UpdateModel
from django.views.generic import View
from django.http import HttpResponse

from drestapi.mixins import HttpResponseMixin
from updates.forms import UpdateModelForm
from .mixins import CSRFExemptMixin
from .utils import is_json

class UpdateModelDetailAPIview(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True

    def get_object(self,id=None):
        '''
        проверка существует ли этот объект
        разные методы
        :param id:
        :return: объект. если существует, иначе None
        '''
        # try:
        #     obj = UpdateModel.objects.get(id=id)
        # except UpdateModel.DoesNotExist:
        #     obj = None
        # return obj

        qs = UpdateModel.objects.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None



    def get(self, request, id, *arg, **kwargs):
        obj = self.get_object(id=id)
        if obj == None:
            error_data = json.dumps({'message': 'Update no found'})
            return self.render_to_response(error_data, status=404)

        json_data = obj.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *arg, **kwargs):
        json_data = json.dumps({'message' : 'Not allowad on this endpoint'})
        return self.render_to_response(json_data)

    def put(self, request, id, *arg, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent. Use JSOn'})
            return self.render_to_response(error_data, status=400)

        obj = self.get_object(id=id)
        if obj == None:
            error_data = json.dumps({'message': 'Update not found'})
            return self.render_to_response(error_data, status=404)

        data = json.loads(obj.serialize())
        passed_data = json.loads(request.body)
        for key, value in passed_data.items():
            data[key] = value

        form = UpdateModelForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)

        json_data = json.dumps({'message': 'something cool has happened'})
        return self.render_to_response(json_data)

    def delete(self, request, id, *arg, **kwargs):
        obj = self.get_object(id=id)
        if obj == None:
            error_data = json.dumps({'message': 'there in nothing to delete'})
            return self.render_to_response(error_data, status=404)
        deleted_ = obj.delete()
        if deleted_.count() == 1:
            json_data = json.dumps({'message': 'something was deleted'})
            return self.render_to_response(json_data, status=200)
        error_data = json.dumps({'message': 'something bad happened in the jungle'})
        return self.render_to_response(eror_data, status=200)


class UpdateModelListAPIview(HttpResponseMixin, CSRFExemptMixin, View):

    is_json = True
    queryset = None
    def get_queryset(self):
        qs = UpdateModel.objects.all()
        self.queryset = qs
        return qs

    def get_object(self,id=None):
        '''
        проверка существует ли этот объект
        разные методы
        :param id:
        :return: объект. если существует, иначе None
        '''
        if id is None:
            return None
        print(id)
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)
        passed_id = data.get('id', None)
        if passed_id is not None:
            obj = self.get_object(id=passed_id)
            if obj == None:
                error_data = json.dumps({'message': 'Update no found'})
                return self.render_to_response(error_data, status=404)
            json_data = obj.serialize()
            return self.render_to_response(json_data)
        qs = UpdateModel.objects.all()
        json_data = qs.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *arg, **kwargs):

        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent. Use JSOn'})
            return self.render_to_response(error_data, status=400)
        data = json.loads(request.body)
        form = UpdateModelForm(data)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)
        data = {'message' : 'Something bad happend'}
        return self.render_to_response(data, status=400)

    def put(self, request, *arg, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent. Use JSOn'})
            return self.render_to_response(error_data, status=400)
        passed_data = json.loads(request.body)
        passed_id = passed_data.get('id', None)

        if not passed_id:
            error_data = json.dumps({'message': 'Plese ukajite id of object'})
            return self.render_to_response(error_data, status=400)

        obj = self.get_object(id=passed_id)
        if obj == None:
            error_data = json.dumps({'message': 'Object not found'})
            return self.render_to_response(error_data, status=404)

        data = json.loads(obj.serialize())
        passed_data = json.loads(request.body)
        for key, value in passed_data.items():
            data[key] = value

        form = UpdateModelForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)

        json_data = json.dumps({'message': 'something cool has happened'})
        return self.render_to_response(json_data)


    def delete(self, request, *arg, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({'message': 'Invalid data sent. Use JSOn'})
            return self.render_to_response(error_data, status=400)
        passed_data = json.loads(request.body)
        passed_id = passed_data.get('id', None)

        obj = self.get_object(id=passed_id)
        if obj == None:
            error_data = json.dumps({'message': 'there in nothing to delete'})
            return self.render_to_response(error_data, status=404)
        deleted_, item_deleted = obj.delete()
        print(deleted_, 'DELETED')
        if deleted_ == 1:
            json_data = json.dumps({'message': 'something was deleted'})
            return self.render_to_response(json_data, status=200)
        error_data = json.dumps({'message': 'something bad happened in the jungle'})
        return self.render_to_response(error_data, status=200)
import json
from samples.models import Sample as SampleModel

from django.views import View
from drestapi.mixins import HttpResponseMixin
from .mixins import CSRFExemptMixin
from .utils import is_json
from samples.forms import SampleModelForm

class SampleModelDetailAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    '''
    CRUD
    Create      POST
    Retrieve    GET
    Update      PUT
    Delete      DELETE
    '''
    def get_sample(self, system_id=None, sample_treatment=None):
        try:
            obj = SampleModel.samples.get(system_id=system_id, sample_treatment=sample_treatment)
        except SampleModel.DoesNotExist:
            obj = None
        return obj

    def get(self, request, system_id, sample_treatment, *args, **kwargs):
        '''RETRIEVE'''
        sample_treatment = sample_treatment.replace('-', ' ') # kak by eto inache sdelat`???
        obj = self.get_sample(system_id=system_id, sample_treatment=sample_treatment)
        if obj == None:
            error_data = json.dumps({'message': 'sample does not exist'})
            return self.render_to_response(error_data, status=404)
        json_data = obj.serialize()
        return self.render_to_response(json_data)

    def put(self, request, *args, **kwargs):
        '''UPDATE
        find sample, replace old data with new, validata i bla bla
        '''
        sample_treatment = sample_treatment.replace('-', ' ')



    def post(self, request, *args, **kwargs): # create blyat
        '''CREATE
        system -> tretment -> data -> unique_check -> load -> save
        '''
        error_data = json.dumps({'message': 'you can not create sample data at this endpoint'})
        return self.render_to_response(error_data, status=400)


    def delete(self, request, system_id, sample_treatment, *args, **kwargs):
        '''DELETE
        1 check if sample exist
        2 delete that MF
        '''
        sample_treatment = sample_treatment.replace('-', ' ')
        obj = self.get_sample(system_id=system_id, sample_treatment=sample_treatment)

        if obj:
            del_obj = obj.delete()
            del_message = json.dumps({'message': 'sucsessfully deleted'})
            return self.render_to_response(del_message)
        if obj == None:
            error_data = json.dumps({'message': 'sample not fount'})
            return self.render_to_response(error_data, status=404)
        error_data = json.dumps({'message': 'could not delete this stuff'})
        return self.render_to_response(error_data, status=400)



class SampleModelListAPIView(HttpResponseMixin, CSRFExemptMixin, View):

    def get_data_from_db(self, system_id=None, sample_treatment=None, *args, **kwargs):
        if system_id:
            if sample_treatment:
                qs = SampleModel.samples.filter(system_id=system_id, sample_treatment=sample_treatment)
                if len(qs) == 0:
                    qs = None
                return qs
            qs = SampleModel.samples.filter(system_id=system_id)
            if len(qs) == 0:
                qs = None
            return qs
        qs = SampleModel.samples.all()
        return qs



    def get(self, request, *args, **kwargs):
        if not is_json(request.body):
            error_data = json.dumps({'message': 'invalid data format. please use JSON'})
            return self.render_to_response(error_data, status=404)
        input_data = json.loads(request.body)
        # ne nravitsya mne eto govno
        try:
            system_id = input_data['system_id']
        except:
            system_id = None
        try:
            sample_treatment = input_data['sample_treatment'].replace('-', ' ')
        except:
            sample_treatment = None
        obj = self.get_data_from_db(system_id=system_id, sample_treatment=sample_treatment)
        if obj == None: # check if EXIST
            error_data = json.dumps({'message': 'sample not fount'})
            return self.render_to_response(error_data, status=404)
        json_data = obj.serialize()
        return self.render_to_response(json_data)


    def put(self, request, *args, **kwargs):
        '''UPDATE'''
        if not is_json(request.body):
            error_data = json.dumps({'message': 'invalid data format. please use JSON'})
            return self.render_to_response(error_data, status=404)

        pas_data = json.loads(request.body)
        pas_system_id = pas_data['system_id']
        pas_sample_treatment = pas_data['sample_treatment']

        sample = self.get_data_from_db(system_id=pas_system_id, sample_treatment=pas_sample_treatment)# [0]
        if sample is None:
            error_data = json.dumps({'message': 'sample not found'})
            return self.render_to_response(error_data, status=404)

        for key, value in pas_data.items():
            sample[key] = value

        form = SampleModelForm(sample)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)
        data = {'message' : 'Something bad happend'}
        return self.render_to_response(data, status=400)




    def post(self, request, *args, **kwargs):
        if not is_json(request.body):
            error_data = json.dumps({'message': 'invalid data format. please use JSON'})
            return self.render_to_response(error_data, status=404)

        input_data = json.loads(request.body)
        form = SampleModelForm(input_data)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)
        data = {'message' : 'Something bad happend'}
        return self.render_to_response(data, status=400)



    def delete(self, request, *args, **kwargs):
        if not is_json(request.body):
            error_data = json.dumps({'message': 'invalid data format. please use JSON'})
            return self.render_to_response(error_data, status=404)
        input_data = json.loads(request.body)
        # ne nravitsya mne eto govno
        try:
            system_id = input_data['system_id']
        except:
            system_id = None
        try:
            sample_treatment = input_data['sample_treatment'].replace('-', ' ')
        except:
            sample_treatment = None
        if system_id is None or sample_treatment is None:
            error_data = json.dumps({'message': 'please specify sample'})
            return self.render_to_response(error_data, status=400)

        obj = self.get_data_from_db(system_id=system_id, sample_treatment=sample_treatment)
        if obj is None:
            error_data = json.dumps({'message': 'sample is not found'})
            return self.render_to_response(error_data, status=404)
        del_samples = []
        for sample in obj:
            del_samples.append((sample.system_id, sample.sample_treatment))
            sample.delete()
        del_message = json.dumps({'message': 'all specified objects were deleted', 'samples' : del_samples})
        return self.render_to_response(del_message)


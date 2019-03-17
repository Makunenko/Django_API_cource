import json
from django.db import models



def upload_sample_xrd(instance, filename):
    return "samples/xrd/{system}/{filename}".format(system=instance.system_id, filename=filename)

class SampleQuerySet(models.QuerySet):
    def serialize(self):
        list_of_samples = list(self.values('system_id', 'system_composition', 'sample_treatment', 'sample_xrd'))
        # print(list_values)
        return json.dumps(list_of_samples)

class SampleManager(models.Manager):
    def get_queryset(self):
        return SampleQuerySet(self.model, using=self._db)

class Sample(models.Model):
    system_id           = models.CharField(max_length=6)
    system_composition  = models.CharField(max_length=100,blank=True, null=True)
    sample_treatment    = models.CharField(max_length=100)
    sample_xrd          = models.FileField(upload_to=upload_sample_xrd, blank=True, null=True)

    samples = SampleManager()

    def __str__(self):
        return self.system_id or ""

    def serialize(self):
        try:
            sample_xrd = self.sample_xrd.url
        except:
            sample_xrd = ""
        data = {
            'system_id' : self.system_id,
            'system_composition' : self.system_composition,
            'sample_treatment' : self.sample_treatment,
            'sample_xrd' : sample_xrd
        }
        data = json.dumps(data)
        return data
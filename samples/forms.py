from django import forms

from .models import Sample as SampleModel

class SampleModelForm(forms.ModelForm):
    class Meta:         # class Meta???
        model = SampleModel
        fields = [
            'system_id',
            'system_composition',
            'sample_treatment',
            'sample_xrd'
        ]

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        system_id = data.get('system_id', None)
        system_composition = data.get('system_composition', None)
        sample_treatment = data.get('sample_treatment', None)

        if system_id is None or sample_treatment is None:
            raise forms.ValidationError('System id and sample treatment is required')
        return super().clean(*args, **kwargs)
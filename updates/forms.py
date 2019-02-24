from django import forms

from .models import Update as UpdateModel # почему .models, а не просто models?

class UpdateModelForm(forms.ModelForm):
    class Meta:         # class inside of class...
        model = UpdateModel
        fields = [
            'user',
            'content',
            'image'
        ]

    def clean(self, *args, **kwargs):
        data = self.cleaned_data # шо це таке?
        content = data.get('content', None)
        image = data.get('image', None)
        if not content:
            content = None
        if content is None and image is None:
            raise forms.ValidationError('content or image is required')
        return super().clean(*args, **kwargs) #а это что значит????

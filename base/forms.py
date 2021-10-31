from django.forms.models import ModelForm
from .models import Room


class roomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

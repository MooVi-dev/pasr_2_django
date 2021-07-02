from django import forms
from django.forms import ModelForm

from procedures.models import Procedure


class ProcedureForm(ModelForm):

    class Meta:
        model = Procedure
        fields = '__all__'


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

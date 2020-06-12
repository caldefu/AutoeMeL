from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Dataset


class CreateDatasetForm (ModelForm):
    def clean_archivo(self):
        file = self.cleaned_data['archivo']
        
        if not (file.name.endswith('.csv') |  file.name.endswith('.xls')):
            raise ValidationError('Archivo no válido')

        return file


    class Meta:
        model = Dataset
        fields = ('name','description', 'archivo')
        labels = { 'name': 'Nombre', 'description':'Descripción'}
        help_texts = { 'description': 'Puede utilizar código Html y/o Markdown' } 



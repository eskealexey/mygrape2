from django import forms
from django.forms import ModelForm, DateInput, Select, TextInput
from tinymce.widgets import TinyMCE

from .models import Location, Notes, GreenOper, Feeding, Processing
from mygrape2.settings import TINYMCE_SIMPLE_CONFIG, TINYMCE_DEFAULT_CONFIG


class LocationAddForm(ModelForm):
    class Meta:
        model = Location
        fields = ['name','sort_id', 'sort', 'date_posadki', 'mesto', 'mesto_graf', 'nameuser']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control',}),
            'date_posadki': DateInput(attrs={'type': 'date'}),
            'mesto': TextInput(attrs={'class': 'form-control',}),
        }


class LocationEditForm(ModelForm):
    class Meta:
        model = Location
        fields = ['name','sort_id', 'sort', 'date_posadki', 'mesto', 'mesto_graf', 'nameuser']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control',}),
            'date_posadki': TextInput(attrs={'class': 'form-control',}),
            'mesto': TextInput(attrs={'class': 'form-control',}),
        }

class LocationDeleteForm(ModelForm):
    class Meta:
        model = Location
        fields = ['date_delete', 'prichina']
        widgets = {
            'date_delete': DateInput(attrs={'type': 'date'}),
            'prichina': TextInput(attrs={'class': 'form-control',}),
        }


class NoteAddForm(ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))
    def __init__(self, *args, **kwargs):
        is_admin = kwargs.pop('is_admin', False)  # Определяем, используется ли форма в админке
        super().__init__(*args, **kwargs)

        if not is_admin:
            self.fields['description'].widget = TinyMCE(attrs={'config': 'TINYMCE_DEFAULT_CONFIG'})
        else:
            self.fields['description'].widget = TinyMCE(attrs={'config': 'TINYMCE_SIMPLE_CONFIG'})

    class Meta:
        model = Notes
        fields = ['title_note', 'description', 'date_add']
        widgets = {
            'date_add': DateInput(attrs={'type': 'date'}),
        }


class NoteEditForm(ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))
    class Meta:
        model = Notes
        fields = ['title_note', 'description', 'date_add']


class GreenOperAddForm(ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))
    class Meta:
        model = GreenOper
        fields = ['date_add','description']
        widgets = {
            'date_add': DateInput(attrs={'type': 'date'}),
        }


class GreenOperEditForm(ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))
    class Meta:
        model = GreenOper
        fields = ['date_add','description']


class FeedingAddForm(ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))

    class Meta:
        model = Feeding
        fields = ['date_add','dung_id', 'dung', 'description']
        widgets = {
            'date_add': DateInput(attrs={'type': 'date'}),
        }

class FeedingEditForm(ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))
    class Meta:
        model = Feeding
        fields = ['date_add','dung_id','dung', 'description']


class ProcessingAddForm(ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))

    class Meta:
        model = Processing
        fields = ['date_add','preparat_id','preparat', 'description']
        widgets = {
            'date_add': DateInput(attrs={'type': 'date'}),
        }

class ProcessingEditForm(ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 20}))
    class Meta:
        model = Processing
        fields = ['date_add','preparat_id', 'preparat', 'description']

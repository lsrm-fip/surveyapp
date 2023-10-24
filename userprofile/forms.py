from django import forms
from .models import ProfileList, FacultyList
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class EditProfile(forms.ModelForm):
    class Meta:
        model = ProfileList
        exclude = ['owner']
        # fields = ['fullname', 'gender']
        widgets = {
            'fullname': forms.TextInput(attrs={'class':'form-control'}),
            'gender': forms.RadioSelect(attrs={'class':'form-check'}), 
            'faculty': forms.Select(attrs={'class':'form-select'}),
            'major': forms.Select(attrs={'class':'form-select'}),
            'batch': forms.Select(attrs={'class':'form-select'}),            
        }
        labels = {
            'fullname': 'Nama Lengkap',
            'gender': 'Jenis Kelamin',
            'faculty': 'Fakultas',
            'major': 'Jurusan',
            'batch': 'Angkatan'
        }
        
    FormHelper.form_class = 'form-horizontal'
    FormHelper.label_class = 'col-md-4 col-lg-3'
    FormHelper.field_class = 'col-md-8 col-lg-9'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('userprofile')
        self.helper.add_input(Submit('submit', 'Simpan'))
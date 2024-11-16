from django import forms
from .models import Disease, Discover, Country, PatientDisease, Specialize, Record

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ['disease_code', 'pathogen', 'description', 'disease_type']

class DiscoverForm(forms.ModelForm):
    class Meta:
        model = Discover
        fields = ['country', 'disease', 'first_enc_date']

    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Choose a Country")
    disease = forms.ModelChoiceField(queryset=Disease.objects.all(), empty_label="Choose a Disease")

class PatientDiseaseForm(forms.ModelForm):
    class Meta:
        model = PatientDisease
        fields = ['patient', 'disease']

class SpecializeForm(forms.ModelForm):
    class Meta:
        model = Specialize
        fields = ['disease_type', 'doctor']

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['email', 'cname', 'disease_code', 'total_deaths', 'total_patients']
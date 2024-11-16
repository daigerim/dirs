from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate,login, get_user_model
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import DiseaseForm, DiscoverForm, PatientDiseaseForm, SpecializeForm, RecordForm

def homeView(request):
    return render(request=request, template_name='home.html')


def signInView(request):
    if request.method == 'GET':
        return render(request=request, template_name='sign_in.html')

    elif request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        print(email, user)

        if user is not None:
            doctor_exists = Doctor.objects.filter(email=user).exists()
            if doctor_exists:
                login(request, user)
                return render(request=request, template_name='doctor_home.html',
                              context={'message': 'Welcome, Doctor!'})

            public_servant_exists = PublicServant.objects.filter(email=user).exists()
            if public_servant_exists:
                login(request, user)
                return render(request=request, template_name='public_servant_home.html',
                              context={'message': 'Welcome, Public Servant!'})

            return render(request=request, template_name='sign_in.html', context={'error': 'You are not authorized to sign in.'})

        return render(request=request, template_name='sign_in.html', context={'error': 'Wrong email or password!'})


def signOutView(request):
    logout(request)
    return redirect('home_url')


def diseaseView(request):
    diseases_with_discovery = Disease.objects.select_related().values(
        'disease_code',
        'pathogen',
        'description',
        'discover__country__cname',
        'discover__first_enc_date'
    )

    context = {
        'disease_list': diseases_with_discovery
    }

    return render(request=request, template_name='disease.html', context=context)


def personellView(request):
    doctors = Doctor.objects.select_related('email').all()
    public_servants = PublicServant.objects.select_related('email').all()
    context = {
        'doctors': doctors,
        'public_servants': public_servants
    }
    return render(request, 'personnel.html', context)


def recordsView(request):
    records = Record.objects.select_related('email', 'cname', 'disease_code').all()
    return render(request, 'records.html', {'records': records})



def createCountryView(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        population = request.POST.get('population')
        Country.objects.create(cname=cname, population=population)
        return redirect('country_list')
    return render(request, 'create_country.html')


def countryListView(request):
    countries = Country.objects.all()
    return render(request, 'country_list.html', {'countries': countries})


def updateCountryView(request, cname):
    country = Country.objects.get(pk=cname)
    if request.method == 'POST':
        country.population = request.POST.get('population')
        country.save()
        return redirect('country_list')
    return render(request, 'update_country.html', {'country': country})


def deleteCountryView(request, cname):
    try:
        country = Country.objects.get(pk=cname)
        if request.method == 'POST':
            country.delete()
            return redirect('country_list')
    except Country.DoesNotExist:
        return redirect('country_list')
    return render(request, 'delete_country.html', {'country': country})


def createDiseaseTypeView(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        DiseaseType.objects.create(description=description)
        return redirect('disease_type_list')
    return render(request, 'create_disease_type.html')

def diseaseTypeListView(request):
    disease_types = DiseaseType.objects.all()
    return render(request, 'disease_type_list.html', {'disease_types': disease_types})

def updateDiseaseTypeView(request, id):
    disease_type = DiseaseType.objects.get(pk=id)
    if request.method == 'POST':
        disease_type.description = request.POST.get('description')
        disease_type.save()
        return redirect('disease_type_list')
    return render(request, 'update_disease_type.html', {'disease_type': disease_type})

def deleteDiseaseTypeView(request, id):
    try:
        disease_type = DiseaseType.objects.get(pk=id)
        if request.method == 'POST':
            disease_type.delete()
            return redirect('disease_type_list')
    except DiseaseType.DoesNotExist:
        return redirect('disease_type_list')
    return render(request, 'delete_disease_type.html', {'disease_type': disease_type})


def diseaseListView(request):
    diseases = Disease.objects.all()
    return render(request, 'disease_list.html', {'diseases': diseases})

def createDiseaseView(request):
    if request.method == 'POST':
        form = DiseaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('disease_list')
    else:
        form = DiseaseForm()
    disease_types = DiseaseType.objects.all()
    return render(request, 'create_disease.html', {'form': form, 'disease_types': disease_types})

def updateDiseaseView(request, disease_code):
    disease = Disease.objects.get(disease_code=disease_code)
    if request.method == 'POST':
        form = DiseaseForm(request.POST, instance=disease)
        if form.is_valid():
            form.save()
            return redirect('disease_list')
    else:
        form = DiseaseForm(instance=disease)
    return render(request, 'update_disease.html', {'form': form, 'disease': disease})

def deleteDiseaseView(request, disease_code):
    disease = Disease.objects.get(disease_code=disease_code)
    if request.method == 'POST':
        disease.delete()
        return redirect('disease_list')
    return render(request, 'delete_disease.html', {'disease': disease})

def discoverListView(request):
    discoveries = Discover.objects.all()
    return render(request, 'discover_list.html', {'discoveries': discoveries})

def createDiscoverView(request):
    if request.method == 'POST':
        form = DiscoverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('discover_list')
    else:
        form = DiscoverForm()
    country = Country.objects.all()
    disease = Disease.objects.all()
    return render(request, 'create_discover.html', {'form': form, 'country': country, 'disease': disease})

def updateDiscoverView(request, pk):
    discover = Discover.objects.get(pk=pk)
    if request.method == 'POST':
        form = DiscoverForm(request.POST, instance=discover)
        if form.is_valid():
            form.save()
            return redirect('discover_list')
    else:
        form = DiscoverForm(instance=discover)
    return render(request, 'update_discover.html', {'form': form})

def deleteDiscoverView(request, pk):
    discover = Discover.objects.get(pk=pk)
    if request.method == 'POST':
        discover.delete()
        return redirect('discover_list')
    return render(request, 'delete_discover.html', {'discover': discover})

def createPatientDiseaseView(request):
    if request.method == 'POST':
        form = PatientDiseaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_disease_list')
    else:
        form = PatientDiseaseForm()
    return render(request, 'patient_disease_create.html', {'form': form})

def patientDiseaseListView(request):
    patient_diseases = PatientDisease.objects.all()
    return render(request, 'patient_disease_list.html', {'patient_diseases': patient_diseases})
def updatePatientDiseaseView(request, pk):
    patient_disease = PatientDisease.objects.get(pk=pk)
    if request.method == 'POST':
        form = PatientDiseaseForm(request.POST, instance=patient_disease)
        if form.is_valid():
            form.save()
            return redirect('patient_disease_list')
    else:
        form = PatientDiseaseForm(instance=patient_disease)
    return render(request, 'patient_disease_update.html', {'form': form})

def deletePatientDiseaseView(request, pk):
    patient_disease = PatientDisease.objects.get(pk=pk)
    if request.method == 'POST':
        patient_disease.delete()
        return redirect('patient_disease_list')
    return render(request, 'patient_disease_delete.html', {'patient_disease': patient_disease})

def specializeListView(request):
    specializes = Specialize.objects.all()
    return render(request, 'specialize_list.html', {'specializes': specializes})

def specializeCreateView(request):
    form = SpecializeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('specialize_list')
    return render(request, 'specialize_form.html', {'form': form})

def specializeUpdateView(request, pk):
    specialize = Specialize.objects.get(pk=pk)
    if request.method == 'POST':
        form = SpecializeForm(request.POST, instance=specialize)
        if form.is_valid():
            form.save()
            return redirect('specialize_list')
    else:
        form = SpecializeForm(instance=specialize)
    return render(request, 'specialize_form.html', {'form': form})

def specializeDeleteView(request, pk):
    specialize = Specialize.objects.get(pk=pk)
    if request.method == 'POST':
        specialize.delete()
        return redirect('specialize_list')
    return render(request, 'specialize_confirm_delete.html', {'specialize': specialize})

def recordListView(request):
    records = Record.objects.all()
    return render(request, 'record_list.html', {'records': records})

def recordCreateView(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = RecordForm()
    return render(request, 'record_form.html', {'form': form})

def recordUpdateView(request, pk):
    record = Record.objects.get(pk=pk)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = RecordForm(instance=record)
    return render(request, 'record_form.html', {'form': form})

def recordDeleteView(request, pk):
    record = Record.objects.get(pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('record_list')
    return render(request, 'record_confirm_delete.html', {'record': record})





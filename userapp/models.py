from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import CustomerManager

class Country(models.Model):
    cname = models.CharField(max_length=50, primary_key=True)
    population = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.cname} (Population: {self.population})"

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=40)
    salary = models.IntegerField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    cname = models.ForeignKey('Country', on_delete=models.CASCADE)  # FK to Country table

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'salary', 'cname']

    def __str__(self):
        return self.email

class Patient(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Patient: {self.email}"


class DiseaseType(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=140)

    def __str__(self):
        return self.description


class Disease(models.Model):
    disease_code = models.CharField(max_length=50, primary_key=True)
    pathogen = models.CharField(max_length=20)
    description = models.CharField(max_length=140)
    disease_type = models.ForeignKey(DiseaseType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.disease_code} - {self.pathogen}"


class Discover(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    first_enc_date = models.DateField()

    class Meta:
        unique_together = ('country', 'disease')
        verbose_name = 'Discover'
        verbose_name_plural = 'Discoveries'

    def __str__(self):
        return f"Discovery of {self.disease} in {self.country} on {self.first_enc_date}"



class PatientDisease(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('patient', 'disease')

    def __str__(self):
        return f"{self.patient} has {self.disease}"


class PublicServant(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"Public Servant: {self.email}, Department: {self.department}"


class Doctor(models.Model):
    email = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    degree = models.CharField(max_length=20)

    def __str__(self):
        return f"Doctor: {self.email}, Degree: {self.degree}"


class Specialize(models.Model):
    disease_type = models.ForeignKey(DiseaseType, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('disease_type', 'doctor')

    def __str__(self):
        return f"Doctor {self.doctor} specializes in {self.disease_type}"


class Record(models.Model):
    email = models.ForeignKey(PublicServant, on_delete=models.CASCADE)
    cname = models.ForeignKey(Country, on_delete=models.CASCADE)
    disease_code = models.ForeignKey(Disease, on_delete=models.CASCADE)
    total_deaths = models.IntegerField()
    total_patients = models.IntegerField()

    class Meta:
        unique_together = ('email', 'cname', 'disease_code')
        verbose_name = 'Record'
        verbose_name_plural = 'Records'

    def __str__(self):
        return (f"Record: {self.email}, Disease: {self.disease_code}, "
                f"Country: {self.cname}, Deaths: {self.total_deaths}, Patients: {self.total_patients}")

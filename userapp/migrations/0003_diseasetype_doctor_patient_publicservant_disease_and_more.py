# Generated by Django 5.1.3 on 2024-11-14 13:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_country_population'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiseaseType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('degree', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PublicServant',
            fields=[
                ('email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('department', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('disease_code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('pathogen', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=140)),
                ('disease_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.diseasetype')),
            ],
        ),
        migrations.CreateModel(
            name='Discover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_enc_date', models.DateField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.country')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.disease')),
            ],
            options={
                'verbose_name': 'Discover',
                'verbose_name_plural': 'Discoveries',
                'unique_together': {('country', 'disease')},
            },
        ),
        migrations.CreateModel(
            name='PatientDisease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.disease')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('patient', 'disease')},
            },
        ),
        migrations.CreateModel(
            name='Specialize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.diseasetype')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.doctor')),
            ],
            options={
                'unique_together': {('disease_type', 'doctor')},
            },
        ),
    ]
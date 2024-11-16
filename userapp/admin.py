from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(Country)
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(DiseaseType)
admin.site.register(Disease)
admin.site.register(Discover)
admin.site.register(PatientDisease)
admin.site.register(PublicServant)
admin.site.register(Doctor)
admin.site.register(Specialize)
admin.site.register(Record)

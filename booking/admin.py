from django.contrib import admin

# Register your models here.

from .models import Konto, Buchung

admin.site.register(Konto)
admin.site.register(Buchung)

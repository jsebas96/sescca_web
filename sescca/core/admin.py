from django.contrib import admin
from .models import InterfaceView

# Register your models here.
class InterfaceViewAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']

admin.site.register(InterfaceView, InterfaceViewAdmin)
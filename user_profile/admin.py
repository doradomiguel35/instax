from django.contrib import admin
from .models import PicturesUser


class PicturesUserAdmin(admin.ModelAdmin):
	list_display = ['user','image']


admin.site.register(PicturesUser,PicturesUserAdmin)
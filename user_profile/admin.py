from django.contrib import admin
from .models import PicturesUser


class PicturesUserAdmin(admin.ModelAdmin):
	list_display = ['username','image']


admin.site.register(PicturesUser,PicturesUserAdmin)
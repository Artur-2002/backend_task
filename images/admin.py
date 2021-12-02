from django.contrib import admin
from .views import *

# Register your models here.

class ImageAdmin(admin.ModelAdmin):
	list_display = ['name', 'width', 'height']


admin.site.register(Image, ImageAdmin)
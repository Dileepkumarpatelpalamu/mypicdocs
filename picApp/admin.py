from django.contrib import admin
from .models import ImageUpload,ImageCategory
# Register your models here.
admin.site.register([ImageUpload,ImageCategory])

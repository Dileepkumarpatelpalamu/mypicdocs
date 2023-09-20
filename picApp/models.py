from django.db import models
from datetime import datetime
import os
class ImageCategory(models.Model):
    category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category

class ImageUpload(models.Model):
    name = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=False)
    image_category = models.ForeignKey(ImageCategory, on_delete=models.CASCADE)
    image_src = models.CharField(max_length=255,blank=True)
    image = models.ImageField(upload_to='uploads')
    upload_date = models.DateTimeField(auto_now=datetime.now)
    def __str__(self):
        return self.image.name
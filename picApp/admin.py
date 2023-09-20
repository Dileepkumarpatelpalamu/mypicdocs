from django.contrib import admin
from .models import ImageUpload,ImageCategory
from django.utils.html import format_html
import os
# Register your models here.

class ImageUploadAdmin(admin.ModelAdmin):
    list_display=("id","image_file_name","image_category","image_src_path","alt_text","upload_date","image_view")
    search_fields = ('id',"upload_date",'alt_text')
    list_filter =('image_category',)
    list_display_links =("id","image_file_name")
    list_per_page=15
    def image_file_name(self, obj):
        if obj.image:
            return os.path.basename(obj.image.url)
        else:
            return ""
    image_file_name.short_description = 'Name'
    def image_view(self,obj) :
        return format_html(f'<img src="{obj.image.url}" width="50" height="50" style="border-radius:50px; margin-left:20px"/>')
    image_view.short_description = "Image Preview"

    def image_src_path(self,obj) :
        return format_html(f'<a href="{obj.image.url}" target="_blank">{obj.image}</a>')
    image_src_path.short_description = "Image Src"
class ImageCategoryAdmin(admin.ModelAdmin):
    list_display=("id",'category')
    search_fields =("id",'category')
admin.site.register(ImageUpload,ImageUploadAdmin)
admin.site.register(ImageCategory,ImageCategoryAdmin)

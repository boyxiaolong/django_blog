from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
import models

admin.site.register(models.Article)
admin.site.register(models.ExampleModel)
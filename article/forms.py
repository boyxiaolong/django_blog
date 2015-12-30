from django import forms
import models
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

class ArticleForm(forms.Form):
    content = forms.CharField(widget=SummernoteWidget())
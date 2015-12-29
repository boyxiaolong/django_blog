from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

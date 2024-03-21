from django import forms
from mysite.models import Image
  
class ImageForm(forms.ModelForm):
  
    class Meta:
        model = Image
        fields = ['Original']
from django import forms
from .models import Category,Fooditem
from accounts.validators import allow_only_images_validator
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['category_name','description']
      
class FooditemForm(forms.ModelForm):
    image=forms.ImageField(widget=forms.FileInput(attrs={'class':'btn btn-primary w-100'}),validators=[allow_only_images_validator])
    class Meta:
        model=Fooditem
        fields=['food_title','category','description','price','image','is_available']

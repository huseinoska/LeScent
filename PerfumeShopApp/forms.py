from django import forms
from django.core.validators import FileExtensionValidator
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
        }
        labels = {
            'image': 'Image (Max size: 5MB)',
        }
        validators = {
            'image': [
                FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            ]
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 15 * 1024 * 1024:  # 5MB
                raise forms.ValidationError("File size is too large. Maximum allowed size is 5MB.")
        return image
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
from cProfile import label
from django import forms
from django.core import validators
from django.forms import widgets

from .models import Order, Product

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProductForm(forms.ModelForm):
    price = forms.DecimalField(min_value=0)
    images = MultipleFileField()

    class Meta:
        model = Product
        fields = "name", "description", "price", "discount", "images"


class OrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        label="Products",
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    delivery_address = forms.CharField(
        widget=forms.Textarea(),
        required=True,
    )

    promocode = forms.CharField(required=False,)

    class Meta:
        model = Order
        fields = "user", "delivery_address", "promocode", "products"

from cProfile import label
from django import forms
from django.core import validators
from django.forms import widgets

from .models import Order, Product


class ProductForm(forms.ModelForm):
    price = forms.DecimalField(min_value=0)

    class Meta:
        model = Product
        fields = "name", "description", "price", "discount"



class OrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        label="Products",
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    delivery_address = forms.CharField(
        widget= forms.Textarea(),
        required=True,
    )

    promocode = forms.CharField(required=False,)
    class Meta:
        model = Order
        fields = "user", "delivery_address", "promocode", "products"

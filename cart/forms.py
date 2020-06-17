from django import forms
from django.forms.formsets import formset_factory


class CartAddProductForm(forms.Form):
    pass


class CartAddUnitForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': "form-control form-control-sm",
        'value': 1
    }))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


CartAddUnitSet = formset_factory(CartAddUnitForm)
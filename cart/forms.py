from django import forms
from django.forms.formsets import formset_factory

class CartAddProductForm(forms.Form):
    pass


class CartAddUnitForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={
        'class': 'form-control form-control-sm'
    }))
    price = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    id = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    title = forms.CharField(max_length=255, widget=forms.HiddenInput)
    total_price = forms.DecimalField(min_value=0, widget=forms.HiddenInput)
    img = forms.CharField(widget=forms.HiddenInput)


CartAddUnitFormSet = formset_factory(CartAddUnitForm, extra=0)
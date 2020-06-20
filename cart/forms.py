from django import forms
from django.forms.formsets import formset_factory, BaseFormSet


class BaseAddUnitSet(BaseFormSet):
    def add_fields(self, form, index, value=None):
        super(BaseAddUnitSet,self).add_fields(form, index)
        form.fields['quantity'] = forms.IntegerField(
            min_value=1,
            max_value=value,
            widget=forms.NumberInput(attrs={
        'class': 'form-control form-control-sm'
    }))
class CartAddProductForm(forms.Form):
    pass


class CartAddUnitForm(forms.Form):
    price = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    id = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    title = forms.CharField(max_length=255, widget=forms.HiddenInput)
    total_price = forms.DecimalField(min_value=0, widget=forms.HiddenInput)
    img = forms.CharField(widget=forms.HiddenInput)
    stock = forms.IntegerField(min_value=0, widget=forms.HiddenInput)


CartAddUnitFormSet = formset_factory(CartAddUnitForm, extra=0, formset=BaseAddUnitSet)
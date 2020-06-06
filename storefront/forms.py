from django import forms

from .models import ParentCategory, SubCategory


class SubCategoryForm(forms.ModelForm):
    parent_category = forms.ModelChoiceField(
        queryset=ParentCategory.objects.all(),
        empty_label=None,
        label='parent category',
        required=True
    )

    class Meta:
        model = SubCategory
        fields = '__all__'

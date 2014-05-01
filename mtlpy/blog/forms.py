from django import forms
from mtlpy.blog.models import Category


class CatTransferForm(forms.Form):
    from_cats = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(posts__isnull=False).distinct())
    to_cat = forms.ModelChoiceField(queryset=Category.objects.all())

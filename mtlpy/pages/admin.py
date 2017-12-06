from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from .models import I18NFlatPage


class I18NFlatPageForm(FlatpageForm):
    class Meta:
        model = I18NFlatPage
        exclude = []


class I18NFlatPageAdmin(FlatPageAdmin):
    form = I18NFlatPageForm
    list_display = ('url', 'title', 'language', 'listed')
    fieldsets = (
        (None, {'fields': ('url', 'language', 'title', 'content',
                           'sites', 'translation', 'listed')}),
        (_('Advanced options'), {'classes': ('collapse',),
                                 'fields': ('enable_comments',
                                            'registration_required', 'template_name')}),
    )


admin.site.unregister(FlatPage)
admin.site.register(I18NFlatPage, I18NFlatPageAdmin)

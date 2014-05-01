from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import MtlPyUser

class MtlPyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MtlPyUser

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            MtlPyUser._default_manager.get(username=username)
        except MtlPyUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

class MtlPyUserAdmin(UserAdmin):
    add_form = MtlPyUserCreationForm 

admin.site.register(MtlPyUser, MtlPyUserAdmin)

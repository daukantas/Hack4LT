from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList

from hack4lt.models import Hacker



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), max_length=128, min_length=6,
                        widget=forms.PasswordInput(render_value=False))
    password_repeat = forms.CharField(label=_('Repeat Password'), min_length=6,
            max_length=128, widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = Hacker
        fields = ('username', 'password', 'password_repeat', 'first_name',
                  'last_name', 'email', 'repository', 'website',
                  'stackoverflow_user', 'description')

    def is_valid(self):
        valid = super(RegistrationForm, self).is_valid()
        if not valid:
            return valid

        first_password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('password_repeat')

        if first_password == repeat_password:
            return True
        errors = self._errors.setdefault('password', ErrorList())
        errors.append(u'Passwords do not match')
        return False


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=100)
    password = forms.CharField(label=_('Password'), max_length=128,
                        widget=forms.PasswordInput(render_value=False))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if self.errors:
            return cleaned_data

        user = authenticate(**cleaned_data)
        if not user:
            raise forms.ValidationError(_('Username or password is incorrect'))
        cleaned_data['user'] = user
        return cleaned_data
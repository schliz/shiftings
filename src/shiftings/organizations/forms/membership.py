from typing import Optional

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from shiftings.accounts.models import User
from shiftings.organizations.models import Membership


class MembershipForm(forms.ModelForm):
    user = forms.CharField(max_length=150, label=_('Username'), required=False)

    class Meta:
        model = Membership
        fields = ['organization', 'user', 'group']
        widgets = {'organization': forms.HiddenInput()}

    def clean_user(self) -> Optional[User]:
        username = self.cleaned_data.get('user')
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            raise ValidationError(_('The user you entered could not be found.')) from e
        return user

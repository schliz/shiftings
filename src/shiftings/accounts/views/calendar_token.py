from __future__ import annotations

from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from shiftings.accounts.models import CalendarToken
from shiftings.utils.views.base import BaseLoginMixin


class CalendarTokenCreateView(BaseLoginMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        token, created = CalendarToken.objects.get_or_create(user=request.user)
        if not created:
            token.regenerate()
            messages.success(request, _('Calendar link regenerated. Old link will stop working.'))
        else:
            messages.success(request, _('Calendar link generated.'))
        return HttpResponseRedirect(reverse('user_profile'))


class CalendarTokenDeleteView(BaseLoginMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        CalendarToken.objects.filter(user=request.user).delete()
        messages.success(request, _('Calendar link revoked.'))
        return HttpResponseRedirect(reverse('user_profile'))

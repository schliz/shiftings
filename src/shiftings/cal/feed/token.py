from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from shiftings.accounts.models import CalendarToken
from shiftings.cal.feed.user import OwnShiftsFeed
from shiftings.utils.exceptions import Http403

logger = logging.getLogger(__name__)

OIDC_REFRESH_COOLDOWN = timedelta(minutes=10)


class TokenAuthMixin:
    """Authenticate iCal feed requests via a CalendarToken URL parameter."""

    def __call__(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        token_str = kwargs.pop('token', None)
        if not token_str or len(token_str) != 64:
            raise Http403()

        try:
            calendar_token = CalendarToken.objects.select_related('user').get(token=token_str)
        except CalendarToken.DoesNotExist:
            raise Http403()

        user = calendar_token.user

        if settings.OAUTH_ENABLED:
            from shiftings.accounts.models import OIDCOfflineToken
            try:
                offline_token = OIDCOfflineToken.objects.get(user=user)
                if offline_token.updated < timezone.now() - OIDC_REFRESH_COOLDOWN:
                    success = offline_token.refresh_user_info()
                    if not success:
                        return HttpResponse(
                            'OIDC token expired. Please log in via browser to renew.',
                            status=403,
                            content_type='text/plain',
                        )
                    user.refresh_from_db()
            except OIDCOfflineToken.DoesNotExist:
                return HttpResponse(
                    'No OIDC token stored. Please log in via browser.',
                    status=403,
                    content_type='text/plain',
                )

        request.user = user
        return super().__call__(request, *args, **kwargs)


class TokenOwnShiftsFeed(TokenAuthMixin, OwnShiftsFeed):
    pass

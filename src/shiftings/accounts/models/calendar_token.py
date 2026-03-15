from __future__ import annotations

import secrets
from typing import Any

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class CalendarToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='calendar_token',
        verbose_name=_('User'),
    )
    token = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        verbose_name=_('Token'),
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))

    class Meta:
        default_permissions = ()

    def __str__(self) -> str:
        return f'{self.user} ({self.token[:8]}...)'

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.token:
            self.token = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def regenerate(self) -> None:
        self.token = secrets.token_hex(32)
        self.save(update_fields=['token'])

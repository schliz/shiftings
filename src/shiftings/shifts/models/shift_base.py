from django.db import models
from django.utils.translation import gettext_lazy as _


class ShiftBase(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    shift_type = models.ForeignKey('ShiftType', verbose_name=_('Shift Type'), on_delete=models.SET_NULL, blank=True,
                                   null=True)
    place = models.CharField(max_length=255, verbose_name=_('Place'), blank=True, null=True)

    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='%(class)ss',
                                     verbose_name=_('Organization'))

    required_users = models.PositiveIntegerField(verbose_name=_('Required User'), default=0)
    max_users = models.PositiveIntegerField(verbose_name=_('Maximum User'), default=0)

    additional_infos = models.TextField(verbose_name=_('Additional Infos'), blank=True, null=True)

    class Meta:
        abstract = True
        default_permissions = ()

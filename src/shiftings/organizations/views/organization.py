from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.views.generic import DetailView, ListView

from shiftings.organizations.forms.membership import MembershipForm
from shiftings.organizations.forms.organization import OrganizationForm
from shiftings.organizations.models import MembershipType, Organization
from shiftings.utils.pagination import get_pagination_context
from shiftings.utils.permissions import has_any_permission
from shiftings.utils.typing import UserRequest
from shiftings.utils.views.base import BaseLoginMixin, BaseMixin, BasePermissionMixin
from shiftings.utils.views.create_update_view import CreateOrUpdateViewWithImageUpload


class OrganizationMemberMixin(BaseLoginMixin, UserPassesTestMixin, ABC):
    model = Organization

    organization_pk_arg: str = 'pk'

    request: UserRequest

    def get_organization(self) -> Organization:
        return self._get_object(Organization, self.organization_pk_arg)

    def test_func(self) -> bool:
        return self.request.user.has_perm('organizations.admin') or self.get_organization().is_member(self.request.user)


class OrganizationPermissionMixin(BasePermissionMixin, ABC):
    model = Organization

    require_only_one: bool = False
    organization_pk_arg: str = 'pk'

    request: UserRequest

    def get_organization(self) -> Organization:
        return self._get_object(Organization, self.organization_pk_arg)

    def has_permission(self) -> bool:
        perms = self.get_permission_required()
        if self.require_only_one:
            return has_any_permission(self.request.user, perms, self.get_organization())
        return self.request.user.has_perms(perms, self.get_organization())


class OrganizationListView(BasePermissionMixin, ListView):
    template_name = 'organizations/list.html'
    model = Organization
    permission_required = 'organization.admin'
    context_object_name = 'organizations'
    extra_context = {
        'full': True
    }

    def get_queryset(self) -> QuerySet[Organization]:
        search_param = self.request.GET.get('search_param')
        if search_param is not None:
            return Organization.objects.filter(name__icontains=search_param)
        return Organization.objects.all()


class OwnOrganizationListView(BaseLoginMixin, ListView):
    template_name = 'organizations/list.html'
    model = Organization
    context_object_name = 'organizations'
    extra_context = {
        'full': False
    }

    request: UserRequest

    def get_queryset(self) -> QuerySet[Organization]:
        search_param = self.request.GET.get('search_param')
        organizations = self.request.user.organizations
        if search_param is not None:
            return organizations.filter(name__icontains=search_param)
        return organizations


class OrganizationShiftsView(OrganizationMemberMixin, DetailView):
    template_name = 'organizations/organization_shifts.html'
    object: Organization
    context_object_name = 'organization'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        today = date.today()
        context['shifts'] = get_pagination_context(self.request,
                                                   self.object.shifts.filter(start__date__gte=today,
                                                                             end__date__gte=today),
                                                   5, 'shifts')
        return context


class OrganizationAdminView(OrganizationPermissionMixin, DetailView):
    template_name = 'organizations/organization_admin.html'
    object: Organization
    context_object_name = 'organization'
    require_only_one = True
    permission_required = (
        'organizations.see_members', 'organizations.see_statistics', 'organizations.edit_membership_types',
        'organizations.edit_members', 'organizations.edit_recurring_shifts', 'organizations.edit_shift_templates'
    )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        membership_types = []
        for membership_type in self.object.membership_types.all():
            membership_types.append({
                'object': membership_type,
                'members': self.object.members.filter(type=membership_type),
                'form': self.create_membership_form(membership_type)
            })
        context['membership_types'] = membership_types
        return context

    def create_membership_form(self, membership_type: MembershipType):
        return MembershipForm(user=self.request.user, initial={'organization': self.object, 'type': membership_type})


class OrganizationEditView(BasePermissionMixin, CreateOrUpdateViewWithImageUpload):
    form_class = OrganizationForm

    def has_permission(self):
        if self.is_create():
            return self.request.user.has_perm('organizations.admin')
        return self.request.user.has_perm('organizations.edit_organization', self.get_object())

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()

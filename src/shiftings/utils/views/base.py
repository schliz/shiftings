from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union

from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db.models import Model
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin

T = TypeVar('T', bound=Model)


class BaseMixin(AccessMixin, ContextMixin):
    request: HttpRequest
    object: Optional[T] = None

    success_url: Union[str, Callable[..., Any], None] = None
    fail_url: Optional[str] = None
    redirect_url: Optional[str] = None

    kwargs: Dict[str, Any]

    def _get_object(self, cls: Type[T], pk_url_kwarg: str) -> T:
        pk = self.kwargs.get(pk_url_kwarg)
        if self.object and isinstance(self.object, cls):
            if pk is None or pk == self.object.pk:
                return self.object
        if pk is None:
            raise Http404(_('The pk is missing from the url. This is not supposed to be possible.'))
        obj = cls.objects.filter(pk=pk).first()
        if not obj:
            raise Http404(_('There is no %(name)s with that pk.') % {'name': cls.__name__})
        return obj

    def _handle_no_permission(self) -> Optional[HttpResponse]:
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        if self.redirect_url is not None:
            return HttpResponseRedirect(self.redirect_url)
        return None

    def handle_no_permission(self) -> HttpResponse:
        handled = self._handle_no_permission()
        return handled if handled is not None else self.fail

    def get_success_url(self) -> str:
        if self.success_url is None:
            raise ImproperlyConfigured(_('No URL to redirect to. Provide a success_url.'))
        return str(self.success_url)

    @property
    def success(self) -> HttpResponse:
        return HttpResponseRedirect(self.get_success_url())

    def get_fail_url(self) -> Optional[str]:
        return self.fail_url

    @property
    def fail(self) -> HttpResponse:
        url = self.get_fail_url()
        if url is None:
            if self.raise_exception:
                raise PermissionDenied(self.get_permission_denied_message())
            return HttpResponseNotFound(_('Could not find the requested page. This might be a configuration error.'))
        return HttpResponseRedirect(url)


class BaseLoginMixin(LoginRequiredMixin, BaseMixin):
    pass


class BasePermissionMixin(PermissionRequiredMixin, BaseMixin):
    base_permission: Optional[str] = None

    def handle_no_permission(self) -> HttpResponse:
        handled = self._handle_no_permission()
        if handled:
            return handled
        if self.base_permission is not None:
            if not self.request.user.has_perm(self.base_permission):
                raise PermissionDenied(self.get_permission_denied_message())
        elif not self.request.user.has_perm(self.permission_required):
            raise PermissionDenied(self.get_permission_denied_message())
        return self.fail
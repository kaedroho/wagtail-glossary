from django.contrib.auth.models import Permission
from django.urls import path, include, reverse
from django.utils.translation import gettext as _
from django.views.i18n import JavaScriptCatalog

from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

from .views.settings import GlossaryViewSet


@hooks.register("register_admin_urls")
def register_admin_urls():
    urls = [
        path('jsi18n/', JavaScriptCatalog.as_view(packages=['wagtail_glossary']), name='javascript_catalog'),
    ]

    return [
        path(
            "glossary/",
            include(
                (urls, "wagtail_glossary"),
                namespace="wagtail_glossary",
            ),
        )
    ]


@hooks.register('register_admin_viewset')
def register_viewset():
    return GlossaryViewSet('wagtail_glossary_settings', url_prefix='glossary-settings')


class GlossariesMenuItem(MenuItem):
    def is_shown(self, request):
        return (
            request.user.has_perm('wagtail_glossary.add_glossary')
            or request.user.has_perm('wagtail_glossary.change_glossary')
            or request.user.has_perm('wagtail_glossary.delete_glossary')
        )


@hooks.register('register_settings_menu_item')
def register_glossaries_menu_item():
    return GlossariesMenuItem(
        _('Glossaries'),
        reverse('wagtail_glossary_settings:index'),
        icon_name='group',
        order=1000
    )


@hooks.register('register_permissions')
def register_permissions():
    return Permission.objects.filter(
        content_type__app_label='wagtail_glossary',
        codename__in=[
            'add_glossary',
            'change_glossary',
            'delete_glossary',
        ]
    )

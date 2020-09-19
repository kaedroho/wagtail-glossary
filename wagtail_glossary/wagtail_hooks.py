from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

from wagtail.core import hooks


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

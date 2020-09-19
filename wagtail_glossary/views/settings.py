from django.utils.translation import gettext as _

from wagtail.admin.views import generic, mixins
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.core import hooks
from wagtail.users.views.users import index

from ..models import Glossary


# FIXME: Permission checks

class IndexView(mixins.SearchableListMixin, generic.IndexView):
    page_title = _("Glossaries")
    add_item_label = _("Add a glosary")
    search_box_placeholder = _("Search glossaries")
    search_fields = ['name']
    context_object_name = 'glossaries'
    paginate_by = 20
    page_kwarg = 'page'
    ordering = ['name']

    def get_template_names(self):
        if self.request.is_ajax():
            return ['wagtail_glossary/settings/results.html']
        else:
            return ['wagtail_glossary/settings/index.html']


class CreateView(generic.CreateView):
    page_title = _("Add glossary")
    success_message = _("Glossary '{0}' created.")
    template_name = 'wagtail_glossary/settings/create.html'


class EditView(generic.EditView):
    success_message = _("Glossary '{0}' updated.")
    error_message = _("The glossary could not be saved due to errors.")
    delete_item_label = _("Delete glossary")
    context_object_name = 'glossary'
    template_name = 'wagtail_glossary/settings/edit.html'


class DeleteView(generic.DeleteView):
    success_message = _("Glossary '{0}' deleted.")
    page_title = _("Delete glossary")
    confirmation_message = _("Are you sure you want to delete this glossary?")
    template_name = 'wagtail_glossary/settings/confirm_delete.html'


class GlossaryViewSet(ModelViewSet):
    icon = 'group'
    model = Glossary

    index_view_class = IndexView
    add_view_class = CreateView
    edit_view_class = EditView
    delete_view_class = DeleteView

    exclude_form_fields = []

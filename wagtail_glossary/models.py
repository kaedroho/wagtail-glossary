from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.models import Locale, TranslatableMixin
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet



class GlossaryManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Glossary(index.Indexed, models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    language_code = models.CharField(max_length=10)
    editable = models.BooleanField(default=True)

    objects = GlossaryManager()

    class Meta:
        verbose_name_plural = "glossaries"

    search_fields = [
        index.SearchField("name"),
        index.AutocompleteField("name"),
        index.FilterField("language_code"),
    ]

    def natural_key(self):
        return self.slug

    def __str__(self):
        return self.name


@register_snippet
class Definition(index.Indexed, ClusterableModel):
    glossary = models.ForeignKey(Glossary, on_delete=models.CASCADE, related_name="definitions")
    term = models.CharField(max_length=50, db_index=True)
    definition = models.TextField(blank=True)

    search_fields = [
        index.FilterField("glossary"),
        index.SearchField("term"),
        index.AutocompleteField("term"),
        index.RelatedFields("term_variations", [
            index.SearchField("term"),
            index.AutocompleteField("term"),
        ]),
    ]

    panels = [
        FieldPanel("glossary"),
        FieldPanel("term"),
        InlinePanel("term_variations", label="Term variations", help_text="For example: nicknames, acronyms, common mis-spellings"),
        FieldPanel("definition"),
    ]

    def __str__(self):
        terms = [self.term]
        terms.extend(self.term_variations.all().values_list("term", flat=True)[:5])
        return f"Definition of: {', '.join(terms)}"


class DefinitonTermVariation(models.Model):
    definition = ParentalKey(Definition, on_delete=models.CASCADE, related_name="term_variations")
    term = models.CharField(max_length=50)

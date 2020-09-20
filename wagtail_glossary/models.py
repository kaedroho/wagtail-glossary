from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.models import Locale
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


class GlossaryManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Glossary(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    locale = models.ForeignKey(Locale, on_delete=models.CASCADE)
    editable = models.BooleanField(default=True)

    objects = GlossaryManager()

    class Meta:
        verbose_name_plural = "glossaries"

    def natural_key(self):
        return self.slug

    def __str__(self):
        return self.name


@register_snippet
class Definition(index.Indexed, ClusterableModel):
    glossary = models.ForeignKey(Glossary, on_delete=models.CASCADE, related_name="definitions")
    definition = models.TextField(blank=True)

    search_fields = [
        index.FilterField("glossary"),
        index.RelatedFields("glossary", [
            index.FilterField("locale"),
        ]),
        index.RelatedFields("terms", [
            index.SearchField("term"),
            index.AutocompleteField("term"),
        ]),
    ]

    panels = [
        FieldPanel("glossary"),
        InlinePanel("terms", label="Terms"),
        FieldPanel("definition"),
    ]

    def __str__(self):
        terms = self.terms.all().values_list("term", flat=True)[:5]
        return f"{', '.join(terms)}"


class DefinitonTerm(models.Model):
    definition = ParentalKey(Definition, on_delete=models.CASCADE, related_name="terms")
    term = models.CharField(max_length=50)
    canonical = models.BooleanField(default=False)

    class Meta:
        constraints = [
            # Allow one canonical term per definition
            UniqueConstraint(fields=['definition'], name='one_canonical_per_definition', condition=Q(caninical=True)),
        ]

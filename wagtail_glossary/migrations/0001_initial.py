# Generated by Django 3.1.1 on 2020-09-20 01:39

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.search.index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0057_page_locale_fields_notnull'),
    ]

    operations = [
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('definition', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='Glossary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('editable', models.BooleanField(default=True)),
                ('locale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.locale')),
            ],
            options={
                'verbose_name_plural': 'glossaries',
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='DefinitonTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=50)),
                ('canonical', models.BooleanField(default=False)),
                ('definition', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='terms', to='wagtail_glossary.definition')),
            ],
        ),
        migrations.AddField(
            model_name='definition',
            name='glossary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='definitions', to='wagtail_glossary.glossary'),
        ),
        migrations.AddConstraint(
            model_name='definitonterm',
            constraint=models.UniqueConstraint(condition=models.Q(canonical=True), fields=('definition',), name='one_canonical_per_definition'),
        ),
    ]

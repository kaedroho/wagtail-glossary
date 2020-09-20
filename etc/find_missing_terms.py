"""
A script that finds terms that may be missing from the glossary

TODO: Convert into a management command
"""

import string
import re

import enchant
from wagtail.core.models import Page
from wagtail_localize.segments.extract import extract_segments
from wagtail_localize.segments.types import StringSegmentValue


def is_number(text):
    try:
        int(text)
        return True
    except ValueError:
        if text.endswith('st') or text.endswith('nd') or text.endswith('th'):
            return is_number(text[:-2])

        return False


SPLIT_RE = re.compile(r'[\s\.\,\[\]\(\)\!\?]')
EMAIL_RE = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
URL_RE = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

def extract_terms_from_text(text):
    terms = SPLIT_RE.split(text)
    terms = [term.strip(string.punctuation) for term in terms]
    return [term for term in terms if term and not is_number(term) and not EMAIL_RE.match(term) and not URL_RE.match(term)]


def extract_terms(instance):
    terms = {}
    for segment in extract_segments(instance):
        if isinstance(segment, StringSegmentValue):
            if segment.path == 'slug':
                continue
            terms[segment.path] = extract_terms_from_text(segment.render_text())

    return terms


def term_in_dictionary(d, term):
    if d.check(term):
        return True

    if Definition.objects.filter(term__iexact=term + '\n').exists():
        return True

    if '-' in term:
        parts = term.split('-')
        if len(parts) == 2:
            return term_in_dictionary(d, parts[0]) and term_in_dictionary(d, parts[1])

    return False


def find_missing_terms():
    for page in Page.objects.all().specific():
        d = enchant.Dict(page.locale.language_code)
        terms_by_field = extract_terms(page)
        for field, terms in terms_by_field.items():
            for i, term in enumerate(terms):
                if not term_in_dictionary(d, term):
                    print(page.url, field, i, term)

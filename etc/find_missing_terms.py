"""
A script that finds terms that may be missing from the glossary

TODO: Convert into a management command
"""

import string
import re
from collections import Counter

import enchant
from wagtail.core.models import Page
from wagtail_localize.segments.extract import extract_segments
from wagtail_localize.segments.types import StringSegmentValue
from wagtail_glossary.models import DefinitonTerm


def is_number(text):
    text = ''.join(c for c in text if c != '.' and c != ',').lstrip('$€£').rstrip('k')
    try:
        int(text)
        return True
    except ValueError:
        if text.endswith('st') or text.endswith('nd') or text.endswith('th'):
            return is_number(text[:-2])

        return False


def extract_terms_from_text(text):
    terms = text.split()
    terms = [term.strip(string.punctuation + "‘") for term in terms]
    return [term for term in terms if term and not is_number(term)]


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

    if DefinitonTerm.objects.filter(term__iexact=term).exists():
        return True

    if term.lower().endswith("'s"):
        return term_in_dictionary(d, term[:-2])

    return False


def find_missing_terms():
    counter = Counter()
    for page in Page.objects.all().specific():
        print(page.url)
        d = enchant.Dict(page.locale.language_code)
        terms_by_field = extract_terms(page)
        for field, terms in terms_by_field.items():
            for i, term in enumerate(terms):
                if not term_in_dictionary(d, term):
                    #print(page.url, field, i, term)
                    counter[term.lower()] += 1

    for word, count in counter.most_common(50):
        print(word, count)

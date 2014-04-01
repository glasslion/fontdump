#!/usr/bin/env python
# -*- coding: utf-8 -*-
import six

from fontdump.core import GoogleFontGroup
class TestMultipleWeightGroup:
    @classmethod
    def setup_class(cls):
        cls.group = GoogleFontGroup(
            'http://fonts.googleapis.com/css?family=Open+Sans:300,400,700,800'
            '|Dosis:300,400')

    def test_has_svg(self):
        assert self.group.has_svg == False
        assert self.group.formats == ['woff', 'ttf', 'eot']

    def test_has_ie_fix(self):
        assert self.group.has_ie_fix == True

    def test_fetch_css(self):
        for css in self.group.css.values():
            assert css.type == 'text/css'


class TestSingleWeightSingleFont(object):
    @classmethod
    def setup_class(cls):
        cls.group = GoogleFontGroup(
            'http://fonts.googleapis.com/css?family=Open+Sans:400'
            )
        cls.font = cls.group.fonts[0]

    def test_local_names(self):
        assert isinstance(self.font.local_names, list)
        assert isinstance(self.font.local_names[-1], six.string_types)

    def test_primary_name(self):
        name = self.font.primary_name
        assert name.startswith('Open')
        assert name.endswith('Sans')

    def test_has_svg(self):
        assert self.group.has_svg == True
        assert self.group.formats == ['woff', 'ttf', 'eot', 'svg']

    def test_has_ie_fix(self):
        assert self.group.has_ie_fix == False
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import six
import pytest

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
    @pytest.fixture(autouse=True)
    def setup_class(cls, tmpdir):
        cls.tmpdir = tmpdir
        cls.font_dir = tmpdir.mkdir('font_dir')
        cls.output_dir = tmpdir.mkdir('output_dir')
        cls.group = GoogleFontGroup(
            'http://fonts.googleapis.com/css?family=Open+Sans:400',
            str(cls.font_dir),
            str(cls.output_dir)
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

    def test_font_dir_path(self):
        assert str(self.font_dir) == self.group.font_dir_path

    def test_download_font_files(self):
        self.font.download_font_files()
        output_dir = str(self.output_dir)
        font_name = self.font.primary_name
        for format in self.group.formats:
            assert os.path.exists(
                os.path.join(output_dir, '%s.%s' % (font_name,format)))
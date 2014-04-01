#!/usr/bin/env python
# -*- coding: utf-8 -*-#
from __future__ import print_function
import re
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import requests
import cssutils


USER_AGENTS = {
    'woff':  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, '
             'like Gecko) Chrome/30.0.1599.101 Safari/537.36',  # Chrome

    'eot':   'Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0)',  # IE9

    'ttf':   'Mozilla/5.0 (Linux; U; Android 2.2; en-us; DROID2 GLOBAL '
             'Build/S273) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 '
             'Mobile Safari/533.1',  # Andord 2

    'svg':   'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) '
             'AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 '
             'Mobile/7B334b Safari/531.21.10',  # iOS<4.2

    'ie6-8': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; '
             '.NET CLR 1.1.4322)'
}


class GoogleFont(object):
    """docstring for GoogleFont"""
    def __init__(self, group, index):
        self.group = group
        self.index = index
        self.styles = {}
        for format in self.group.formats:
            self.styles[format] = self.group.css[format].cssRules[index].style

        # e.g. [ 'Dosis Light', 'Dosis-Light']
        self.local_names = re.findall(
            r'local\(\"(.+?)\"\)',
            self.styles['woff']['src'])

        # e.g. 'Dosis-Light'
        self.primary_name = self.local_names[-1]

        self.path = urljoin(self.group.font_dir_path, self.primary_name)

    def download_font_files(self):
        for format in self.group.formats:
            style = self.styles[format]
            font_url = re.findall(r'url\((.+.%s)\)' % format, style['src'])[0]
            r = requests.get(font_url)
            filename = '%s.%s' % (self.primary_name, format)
            print('Downloading font %s ...' % filename)
            with open(filename, 'w') as f:
                f.write(r.content)

    def merge_src(self):
        self.eot_src = "url('%s.eot')" % self.path

        src = ["local(\'%s\')" % name for name in self.local_names]

        src.append("url('%s.eot?#iefix') format('embedded-opentype')" %
                   self.path)
        src.append("url('%s.woff') format('woff')" % self.path)
        src.append("url('%s.ttf') format('truetype')" % self.path)
        if self.group.has_svg:
            src.append(
                "url('%s.svg#%s') format('truetype')" % (
                    self.path,
                    self.primary_name)
                )
        self.merged_src = " ,".join(src)


class GoogleFontGroup(object):
    """docstring for GoogleFont"""

    def __init__(self, google_fonts_url, font_dir_path=''):
        self.google_fonts_url = google_fonts_url
        self.font_dir_path = font_dir_path
        self.fetch_cross_browser_csses()
        self.fonts_count = len(self.css['woff'].cssRules)
        self.has_svg = self.fonts_count == len(self.css['svg'].cssRules)
        self.formats = ['woff', 'ttf', 'eot']
        if self.has_svg:
            self.formats.append('svg')
        self.has_ie_fix = self.fonts_count != len(self.css['ie6-8'].cssRules)
        self.merged_css = self.css['woff']
        self.name_to_font = {}
        if (self.fonts_count != len(self.css['eot'].cssRules) or
                self.fonts_count != len(self.css['ttf'].cssRules)):
            raise RuntimeError(
                'The number of css rules are not same for eot, ttf, and woff')

    def fetch_cross_browser_csses(self):
        self.css = {}
        headers = {}
        for (format, user_agent) in USER_AGENTS.items():
            headers['User-Agent'] = user_agent
            r = requests.get(self.google_fonts_url, headers=headers)
            self.css[format] = cssutils.parseString(r.content)

    @property
    def fonts(self):
        if not hasattr(self, '_fonts'):
            self._fonts = [
                GoogleFont(self, index) for index in range(self.fonts_count)]
        return self._fonts

    def dump(self):
        for (index, font) in enumerate(self.fonts):
            merged_style = self.merged_css.cssRules[index].style
            font.download_font_files()
            font.merge_src()
            merged_style.setProperty("src", font.eot_src)
            merged_style.setProperty("src", font.merged_src, replace=False)
            self.name_to_font[font.primary_name] = font

        with open('webfonts.css', 'w') as f:
            f.write(self.merged_css.cssText)

        self.dump_ie_fix()

    def dump_ie_fix(self):
        if self.has_ie_fix:
            for rule in self.css['ie6-8']:
                src = rule.style.src
                local_names = re.findall(r'local\(\"(.+?)\"\)', src)
                primary_name = local_names[-1]
                rule.style.removeProperty("src")
                rule.style.src = ' ,'.join(
                    ["local(\'%s\')" % name for name in local_names] +
                    [self.name_to_font[primary_name].eot_src]
                )
            with open('webfonts-ie6-8.css', 'w') as f:
                f.write(self.css['ie6-8'].cssText)

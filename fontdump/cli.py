#!/usr/bin/env python
# -*- coding: utf-8 -*-#
"""fontdump.

Usage:
  fontdump <google-fonts-url> [--font-dir-path=<path>]
  fontdump (-h | --help)

Options:
  -h --help                 Show this screen.
  --font-dir-path=<path>    Path to the font dir(ends with /). e.g('staic/fonts/', 'http://cdn/.../fonts/')  
"""
import re
from urlparse import urljoin

import requests
import cssutils
from docopt import docopt

USER_AGENTS = {
    'woff': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36', # Chrome
    'eot': 'Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0)', # IE9
    'ttf': 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; DROID2 GLOBAL Build/S273) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1', #Andord 2
    'svg': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10', #iOS<4.2
    'ie6-8': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)'
}

def download_font(name, url, format):
    r=requests.get(url)
    with open('%s.%s' % (name, format), 'w') as f:
        f.write(r.content)

def main():
    args = docopt(__doc__)
    font_url = args['<google-fonts-url>']
    if args['--font-dir-path']:
        font_path = args['--font-dir-path']
    else:
        font_path = ''

    headers = {}

    style_sheets= {}

    # extract woff
    for (format, user_agent) in USER_AGENTS.items():
        headers['User-Agent'] =  user_agent
        r =requests.get(font_url, headers=headers)
        style_sheets[format] = cssutils.parseString(r.content)

    if len(style_sheets['woff'].cssRules) != len(style_sheets['ie6-8'].cssRules):
        with open('webfonts-ie6-8.css', 'w') as f:
            f.write(style_sheets['ie6-8'].cssText)

    if len(style_sheets['woff'].cssRules) == len(style_sheets['svg'].cssRules):
        INCLUDE_SVG = True
    else:
        INCLUDE_SVG = False

    assert(len(style_sheets['woff'].cssRules) == len(style_sheets['eot'].cssRules))
    assert(len(style_sheets['woff'].cssRules) == len(style_sheets['ttf'].cssRules))

    for (index, rule) in enumerate(style_sheets['woff'].cssRules):
        style = rule.style
        src = style['src']

        local_names = re.findall(r'local\(\"(.+?)\"\)', src)
        font_name = local_names[-1]
        font_path = urljoin(font_path, font_name)

        woff_url = re.findall(r'url\((.+.woff)\)', src)[0]
        download_font(font_name, woff_url, 'woff')

        ttf_style = style_sheets['ttf'].cssRules[index].style
        ttf_url = re.findall(r'url\((.+.ttf)\)', ttf_style['src'])[0]
        download_font(font_name, ttf_url, 'ttf')

        eot_style = style_sheets['eot'].cssRules[index].style
        eot_url = re.findall(r'url\((.+.eot)\)', eot_style['src'])[0]
        download_font(font_name, eot_url, 'eot')
        
        sources = ["local(\'%s\')" % local_name for local_name in local_names]
        sources.append("url('%s.eot?#iefix') format('embedded-opentype')" % font_path)
        sources.append("url('%s.woff') format('woff')" % font_path)
        sources.append("url('%s.ttf') format('truetype')" % font_path)

        if INCLUDE_SVG:
            svg_style = style_sheets['svg'].cssRules[index].style
            svg_url = re.findall(r'url\((.+.svg)\)', ttf_style['src'])[0]
            sources.append("url('%s.svg#%s') format('truetype')" % (font_path,fontname))
            download_font(font_name, svg_url, 'svg')

        style.setProperty("src", "url('%s.eot')" % font_path)
        style.setProperty("src", " ,".join(sources), replace=False)

    with open('webfonts.css', 'w') as f:
        f.write(style_sheets['woff'].cssText)


if __name__ == '__main__':
    main()
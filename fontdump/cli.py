#!/usr/bin/env python
# -*- coding: utf-8 -*-#
import re

import requests
import cssutils

USER_AGENTS = {
    'woff': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36', # Chrome
    'eot': 'Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0)', # IE9
    'ttf': 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; DROID2 GLOBAL Build/S273) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1', #Andord 2
    'svg': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10', #iOS<4.2
}

def main():
    font_url = 'http://fonts.googleapis.com/css?family=Open+Sans:300,400,700,800|Dosis:300,400'

    headers = {}

    style_sheets= {}

    # extract woff
    for (format, user_agent) in USER_AGENTS.items():
        headers['User-Agent'] =  user_agent
        r =requests.get(font_url, headers=headers)
        style_sheets[format] = cssutils.parseString(r.content)

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
        woff_url = re.findall(r'url\((.+.woff)\)', src)[0]

        ttf_style = style_sheets['ttf'].cssRules[index].style
        ttf_url = re.findall(r'url\((.+.ttf)\)', ttf_style['src'])[0]

        eot_style = style_sheets['eot'].cssRules[index].style
        eot_url = re.findall(r'url\((.+.eot)\)', eot_style['src'])[0]

        font_name = local_names[-1]
        font_path = font_name
        sources = ["local(\'%s\')" % local_name for local_name in local_names]
        sources.append("url('%s.eot?#iefix') format('embedded-opentype')" % font_path)
        sources.append("url('%s.woff') format('woff')" % font_path)
        sources.append("url('%s.ttf') format('truetype')" % font_path)

        if INCLUDE_SVG:
            svg_style = style_sheets['svg'].cssRules[index].style
            svg_url = re.findall(r'url\((.+.svg)\)', ttf_style['src'])[0]
            sources.append("url('%s.svg#%s') format('truetype')" % (font_path,fontname))

        style.setProperty("src", "url('%s.eot')" % font_path)
        style.setProperty("src", " ,".join(sources), replace=False)

    print style_sheets['woff'].cssText






if __name__ == '__main__':
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-#
from collections import OrderedDict

import requests
import cssutils

USER_AGENTS = OrderedDict()
USER_AGENTS['woff'] = 'Mozilla/5.0 AppleWebKit/537.36 Chrome/30', # Chrome
USER_AGENTS['ttf'] = 'Mozilla/5.0 (Linux; U; Android 2.1-update1;)', #Andord 2
USER_AGENTS['eot'] = 'Mozilla/4.0 (compatible; MSIE 6.0;)', # IE6
USER_AGENTS['woff'] = 'Mozilla/4.0 (iPad; CPU OS 4_0_1 ) AppleWebKit', #iOS<4.2


def main():
    font_url = 'http://fonts.googleapis.com/css?family=Open+Sans:300,400,700,800|Dosis:300,400'
    sheets={}
    for (format, ua) in USER_AGENTS.items():
        headers = {
            'User-Agent': ua,
        }

        r =requests.get(font_url, headers=headers)
        sheets[format] = cssutils.parseString(r.content)


if __name__ == '__main__':
    main()
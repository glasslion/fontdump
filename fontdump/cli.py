#!/usr/bin/env python
# -*- coding: utf-8 -*-#
"""fontdump heps you dump google web fonts.
  __            _      _
 / _|          | |    | |
| |_ ___  _ __ | |_ __| |_   _ _ __ ___  _ __
|  _/ _ \| '_ \| __/ _` | | | | '_ ` _ \| '_ \.
| || (_) | | | | || (_| | |_| | | | | | | |_) |
|_| \___/|_| |_|\__\__,_|\__,_|_| |_| |_| .__/
                                        | |
                                        |_|
Usage:
  fontdump <google-fonts-url> [--font-dir-path=<path>]
  fontdump (-h | --help)

Options:
  -h --help                 Show this screen.
  --font-dir-path=<path>    Path to the font dir(ends with /).
                            e.g('staic/fonts/', 'http://cdn/.../fonts/')
"""
from docopt import docopt

from fontdump.core import GoogleFontGroup


def main():
    args = docopt(__doc__)
    google_fonts_url = args['<google-fonts-url>']
    if args['--font-dir-path']:
        font_dir_path = args['--font-dir-path']
    else:
        font_dir_path = ''

    g = GoogleFontGroup(google_fonts_url, font_dir_path)
    g.dump()


if __name__ == '__main__':
    main()
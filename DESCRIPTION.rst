fontdump
========

A command line tool to dump the CSS and different formats of fonts for
`Google Fonts <https://www.google.com/fonts>`__, so you can serve them
on your local servers.

Usage
~~~~~

::

    $ fontdump -h
    fontdump heps you dump google web fonts.
      __            _      _
     / _|          | |    | |
    | |_ ___  _ __ | |_ __| |_   _ _ __ ___  _ __
    |  _/ _ \| '_ \| __/ _` | | | | '_ ` _ \| '_ \
    | || (_) | | | | || (_| | |_| | | | | | | |_) |
    |_| \___/|_| |_|\__\__,_|\__,_|_| |_| |_| .__/
                                            | |
                                            |_|
    Usage:
      fontdump <google-fonts-url> [--font-dir-path=<path>]
      fontdump (-h | --help)

    Options:
      -h --help                 Show this screen.
      --font-dir-path=<path>    Path to the font dir(ends with /). e.g('staic/fonts/', 'http://cdn/.../fonts/')

FAQs
~~~~

**Question**: What’s wrong with Google Fonts? Why do I want to serve the
fonts on my own server?

**Answer**: Google Fonts is Great. You shall use it normally. But for
users in some countries, Google Fonts is very slow and sometimes even
inaccessible. Serving your own fonts is the only choice for them.
Besides, some developers may wish to have more control over web fonts.
They might want to embed fonts as base64 strings into the css to bypass
crazy firewalls. They might to store the fonts as jsons to the
localstorage to speed up page loading.

**Question**: Why do I need to install a software to download these
fonts? Can't I just open the Chrome developer tools and download the css
and fonts manually?

**Answer**: Making css font rules compatible with different browsers is
not easy. Thus Google detects the browser's User Agent string and serve
the css that is only compatible with the given browser.

As a web developer/designer, it is very likely that you are using a
modern browser, so the css you get from Google only works in modern
browsers. To improve the user experience for old browser users , we need
to download the 4 differnet formats of fonts and merge the css rules
into a single stylesheet. A tool can simplify the process.

**Question**: What would the merged css look like?

**Answer**:

like this:

::

    @font-face {
      font-family: 'WebFont';
      src: url('webfont.eot'); /* IE9 Compat Modes */
      src: local('WebFont'),
           url('webfont.eot?#iefix') format('embedded-opentype'), /* IE6-IE8 */
           url('webfont.woff') format('woff'), /* Modern Browsers */
           url('webfont.ttf')  format('truetype'), /* Safari, Android, iOS */
           url('webfont.svg#svgFontName') format('svg'); /* Legacy iOS */
    }

Reference:
~~~~~~~~~~

`Using
@font-face <http://css-tricks.com/snippets/css/using-font-face/>`__

`Bulletproof @font-face
Syntax <http://www.paulirish.com/2009/bulletproof-font-face-implementation-syntax/>`__

`WEBFONT
GENERATOR <http://www.fontsquirrel.com/tools/webfont-generator>`__

`Avoiding Faux Weights And Styles With Google Web
Fonts <http://www.smashingmagazine.com/2012/07/11/avoiding-faux-weights-styles-google-web-fonts/>`__

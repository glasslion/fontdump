fontdump
========

A command line tool to dump the CSS and different formats of fonts for [Google Fonts][1], so you can serve them on your local servers.

FAQs
----
**Question**: 
What’s wrong with Google Fonts? Why do I want to serve the fonts on my own server? 

**Answer**: 
Google Fonts is Great. You shall use it normally. But for users in some countries, Google Fonts is very slow and sometimes even inaccessible. Serving your own fonts is the only choice for them. Besides, some developers may wish to have more control over web fonts. They might want to embed fonts as base64 strings into the css to bypass crazy  firewalls. They might to store the fonts as jsons to the localstorage to speed up page loading.


**Question**: 
Why do I need to install a software to download these fonts? Can't I just open the Chrome developer tools and download the css and fonts manually?

**Answer**:
Making css font rules compatible with different browsers is not easy. Thus Google detects the browser's User Agent string and serve the css that is only compatible with the given browser. 

As a web developer/designer, it is very likely that you are using a modern browser, so the css you get from Google only works in modern browsers. To improve the user experience for old browser users , we need to download the 4 differnet formats of fonts and merge the css rules into a single stylesheet. A tool can simplify the process.

  [1]: https://www.google.com/fonts

# Kirsle.net

![Kirsle](https://raw.githubusercontent.com/kirsle/kirsle.net/master/www/solar/kirsle.png)

This is the source code of my personal website,
[Kirsle.net](http://www.kirsle.net/). It runs on top of my Python CMS called
[Rophako](https://github.com/kirsle/rophako).

This Git repo only contains templates and design files for the main Kirsle.net
website. This means only the files that are served directly by the Python CMS
(all pages with the "solar" web design) are here; but there are a decently
large number of static files and one-off CGI scripts that get served directly
by nginx instead. For example the `projects/` folder where I keep downloads of
my various software projects, and the `creativity/` and `wizards` folders.

So, feel free to look around in this repo, but you won't find anything too
interesting in here. It's mostly just Jinja2 HTML templates and the odd web
design file (CSS, JS, and some images).

## Dev Environment Quick Start

Run `bootstrap.py` to automatically clone and configure the Rophako CMS to run
a local dev instance of Kirsle.net.

# Kirsle.net

![Kirsle](https://raw.githubusercontent.com/kirsle/kirsle.net/master/www/solar/kirsle.png)

This is the source code of my personal website, [Kirsle.net][1]. It runs on
top of my Go blog application, [kirsle/blog][2].

This Git repo only contains templates and design files for the main Kirsle.net
website. This means only the files that are served directly by the Go CMS
(all pages with the "solar" web design) are here; but there are a decently
large number of static files and one-off CGI scripts that get served directly
by nginx instead. For example the `projects/` folder where I keep downloads of
my various software projects, and the `creativity/` and `wizards/` folders.

So, feel free to look around in this repo, but you won't find anything too
interesting in here. It's mostly just Go HTML templates, Markdown pages, and the
odd web design file (CSS, JS, and some images).

For the version of Kirsle.net that ran on my Python CMS, [Rophako][3], check
out the `rophako` branch of this repo.

## Dev Environment Quick Start

```bash
# Make sure you have a Go environment set up. Quickly:
export GOPATH="${HOME}/go"
export PATH="${PATH}:${GOPATH}/bin"

# Install my Go blog
go get github.com/kirsle/blog/...

# Run it on the kirsle.net www folder.
blog ./www
```

[1]: https://www.kirsle.net/
[2]: https://github.com/kirsle/blog
[3]: https://github.com/kirsle/rophako

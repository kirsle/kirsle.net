# SiikirPerl

How to install the Perl Siikir CMS.

# Perlbrew

Recommended to install a custom Perl w/ perlbrew instead of using your vendor
version of Perl. I made a dedicated user, `bob` that "owns" the Perl
installation.

```bash
[bob]$ sudo mkdir /opt/perl5 && chown bob:bob /opt/perl5
[bob]$ export PERLBREW_ROOT="/opt/perl5"
[bob]$ wget -O - http://install.perlbrew.pl | bash
[bob]$ perlbrew init
[bob]$ perlbrew install perl-5.18.0
[bob]$ perlbrew switch perl-5.18.0
```

After installing Perl, make a symlink so that `/opt/perl` points to the Perl
root, for example:

```bash
/opt/perl -> /opt/perl5/perls/perl-5.18.0
```

So that `/opt/perl/bin/perl` exists.

# Apache Configuration

You'll need `mod_fcgid`, `mod_rewrite`, and probably `mod_suexec`. On
Debian, install the package `apache2-suexec-custom` so that you can change
suexec to use `/home` as its root (not needed if you plan to put your site
under `/var/www`). The suexec config file is usually at
`/etc/apache2/suexec/www-data`.

Typical VirtualHost configuration for mod\_fcgid:

```apache
    <VirtualHost *:80>
      ServerName www.yoursite.com
      DocumentRoot /home/www/public_html
      CustomLog /home/www/logs/access_log combined
      ErrorLog /home/www/logs/error_log
      SuexecUserGroup www www
      <Directory "/home/www/public_html">
        Options Indexes FollowSymLinks ExecCGI
        AllowOverride All
        Order allow,deny
        Allow from all
      </Directory>
      <Directory "/home/www/public_html/fcgi">
        SetHandler fcgid-script
        Options +ExecCGI
        AllowOverride All
        Order allow,deny
        Allow from all
      </Directory>
    </VirtualHost>
```

Follow that up with a `.htaccess` in your document root:

```apache
    <IfModule mod_rewrite.c>
      RewriteEngine on
      RewriteBase /
      RewriteCond %{REQUEST_FILENAME} !-f
      RewriteCond %{REQUEST_FILENAME} !-d
      RewriteRule . /fcgi/index.cgi [L]
      RewriteRule ^$ /fcgi/index.cgi [L]
    </IfModule>
```

# Perl Modules

The typical Siikir installation requires these modules. Install them using
cpanminus as your Perl user (`bob` in my case).

```bash
$ cpan App::cpanminus
```

The required modules (install each with `cpanm $NAME`):

* CGI::Fast
* FCGI
* JSON
* JSON::XS
* Image::Magick*
* LWP::UserAgent
* Mail::Sendmail
* Template*
* Digest::SHA1
* Net::DNS

You'll __need__ JSON::XS. JSON::PP doesn't quite cut it.

A couple modules have special cases and might not be installable via `cpanm`:

## Image::Magick

Because of Image::Magick's ties with the C ImageMagick library, they need to
be installed by hand. You'll need to download and build ImageMagick from
imagemagick.org (it includes the Perl module, so you don't need to deal with
CPAN at all for this one).

```bash
$ wget http://www.imagemagick.org/download/ImageMagick.tar.gz
$ tar -xzvf ImageMagick.tar.gz
$ cd ImageMagick-*/
$ ./configure --with-perl
$ make
$ make perl-sources
$ sudo make install
$ sudo ldconfig /usr/local/lib
$ cd PerlMagick
$ perl Makefile.PL
$ make
$ make test
$ make install
```

__Note:__ If your site ever starts crashing (particularly after a software
update) saying it can't find `libmagick.so` or something, run
`sudo ldconfig /usr/local/lib` to rebuild the library cache.

### Misc Notes

You'll need `libperl-dev` installed on the system (if you get an error like
"`can't find -lperl`" when building).

## Template

I sometimes have problems installing Template::Toolkit through cpanm because
the test suite doesn't pass completely (35 out of several thousand tests fail).
You can just download and install this module by hand and it works.

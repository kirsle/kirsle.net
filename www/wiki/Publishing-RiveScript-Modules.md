# Publishing RiveScript Modules

My personal notes on how to distribute releases of RiveScript to various language module repositories.

# Python

If this is the first time publishing from a new computer, create `~/.pypirc` with your PyPI credentials:

```
[distutils]
index-servers=pypi

[pypi]
repository = https://pypi.python.org/pypi
username = $USERNAME
password = $PASSWORD
```

Make sure everything's ready to go (version numbers incremented, documentation rebuilt, etc.) and run this command to create all the distributable items:

```bash
# Install the requirements to get the bdist_wheel command
$ pip install -r requirements.txt
$ python setup.py sdist bdist_wheel
```

This generates files in the `dist/` folder:

* `sdist` creates the source tarball
* `bdist_wheel` creates a portable pre-built wheel file (the new "egg")
* `bdist_rpm` creates an RPM (not necessary to upload this to PyPI)
* `bdist_wininst` creates a Win32 installer (not necessary to upload this to PyPI)

And to upload to PyPI:

```bash
$ pip install twine
$ twine upload dist/*
```

See also: <https://python-packaging-user-guide.readthedocs.org/en/latest/distributing/#packaging-your-project>

## Build RPM

See also: <https://fedoraproject.org/wiki/Packaging:Python>

To build the RPM for Fedora:

```bash
$ rpmbuild -ba python-rivescript.spec
```

# JavaScript

* Prepare it for NPM distribution:
    1. Build distributable (compiled JS) files: `grunt dist`
    2. Test an installation from a different directory: `npm install ../rivescript-js` and make sure it works.
    3. From the rivescript-js folder, `npm login` if it's the first time on a new PC and `npm publish` to publish.
* Create release tarballs for GitHub binary distribution:
    1. Build distributable files: `grunt dist`
    2. Remove cruft: `rm -rf node_modules`
    3. Go up a directory to create zip/tar files
        * zip -r rivescript-js-1.1.2.zip rivescript-js -x '*.git*'
        * tar -czvf rivescript-js-1.1.2.tar.gz rivescript-js --exclude .git

See also: [npm developers](https://docs.npmjs.com/misc/developers)

# Perl

1. `perl Makefile.PL`
2. `make`
3. `make dist`

Upload resulting tarball to [PAUSE](http://pause.perl.org/) for indexing on CPAN.
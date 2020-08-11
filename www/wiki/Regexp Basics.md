# Regexp Basics

A small reference for some basic things you can do with regular expressions
that you can get a lot of mileage out of without getting too in the weeds with
crazy features.

Recommended links:

* [Regexr](https://regexr.com/), an interactive regexp explorer.
* [perlretut](https://metacpan.org/pod/distribution/perl/pod/perlretut.pod),
  where I learned regexp back in the day. It's Perl documentation but the
  regexp knowledge inside is universally applicable to other programming languages.

This page includes examples and code snippets in various programming languages.

## String Search (& Replace)

The simplest regexps deal with just plain old raw text.

```javascript
// JavaScript
"Hello world".match(/world/);
```

```perl
# Perl
"Hello world" =~ /world/;
```

```python
# Python
import re
re.match(r'world', "Hello world")
```

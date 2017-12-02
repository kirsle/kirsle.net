# Unicode Problems

A collection of problems I've discovered with [Unicode](https://en.wikipedia.org/wiki/Unicode). Many of these came up in the context of RiveScript (my chatbot scripting language), because people wanna be able to support foreign language chatbots and RiveScript wasn't originally designed with that in mind and UTF-8 support was added later and these are some of the problems encountered.

tl;dr. of some problems:

* [You can't just do `toUppercase()` or `toLowercase()` without risking losing information](#case-folding)
* [Regular expressions are more complicated](#regular-expressions)
* [String equality comparisons are more complicated](#unicode-normalization)

Bug tickets concerning Unicode problems in RiveScript:

* [JavaScript](https://github.com/aichaos/rivescript-js/issues?utf8=%E2%9C%93&q=label%3Aunicode)
* [Python](https://github.com/aichaos/rivescript-python/issues?utf8=%E2%9C%93&q=label%3Aunicode)
* [Perl](https://github.com/aichaos/rivescript-perl/issues?utf8=%E2%9C%93&q=label%3Aunicode)

## Case folding

Some Unicode characters, when made upper- or lowercase, actually transform entirely into separate characters (sometimes multiple separate characters). When reversing the operation, you don't get the original text back as what you started with.

Example: the German symbol `ß`, when made uppercase, becomes two ASCII letters `SS`, which then become two ASCII letters `ss` when made lowercased again:

```javascript
"ß".toUpperCase().toLowerCase() !== "ß";
```

Example: in Turkish, the lowercase letter `i` when uppercased becomes a capital dotted letter `İ`, and when lowercased again becomes a dotless lowercase letter `ı`. This is only the case of your system locale is set to Turkish; if your system locale is English for example `i` becomes `I` becomes `i` again.

```javascript
// Works in English but not in Turkish, exact same code
"i".toUpperCase().toLowerCase() === "i";
```

For this reason I've never updated RiveScript to force-lowercase your triggers. People hated writing a lowercase word `i` for English triggers, but case folding can be a real problem.

[Case folding on W3.org](https://www.w3.org/International/wiki/Case_folding)

## Regular Expressions

Unicode makes dealing with regular expressions more difficult. If you ever found yourself writing a character class like `[A-Za-z0-9]`, this will not work if you expect Unicode. Neither will `\w` or `\W` depending on your programming language of choice.

If you want to make a regexp that matches, say, "letters but not numbers", you can't take a whitelist approach of only matching letters because there's too damn many of them. Instead you have to take a blacklist approach, and use a regexp like `[^0-9]` which will probably work in a lot of cases until somebody starts getting fancy foreign numeric symbols involved, and then the `[0-9]` character class won't work either.

In JavaScript land, regular expressions have trouble in Unicode for many reasons until ES2015 when they added the `/u` flag. Before that, the `.` metacharacter only matches characters in the BMP plane, but not astral characters, and `/u` makes it match astral characters. But, there's still a problem with using the `\b` word-boundary metacharacter, which still deals only with the boundaries between `[A-Za-z0-9]` and spaces and will break with Unicode symbols, even those in the BMP plane. [Unicode-aware regular expressions in ES6](https://mathiasbynens.be/notes/es6-unicode-regex).

Examples (GitHub Issues):

* [UTF-8 and Optionals](https://github.com/aichaos/rivescript-python/issues/37) (Python) - The `\b` word boundary doesn't work with some Unicode symbols.
* [regex doesnt work for UTF8](https://github.com/aichaos/rivescript-js/issues/147) (JavaScript) - The `\b` doesn't work with non-ASCII, and even using Unicode-aware regexps from ES2015+ doesn't change this behavior.

## Unicode Normalization

You can have multiple binary representations of exactly the same string of characters in Unicode.

For example, the accented letter `é` can be represented as either U00E9 Unicode accented letter é, or a combination of two characters, ASCII letter `e` and combining accent mark. Visually the two characters are exactly the same, but a string equality comparison would fail.

Fortunately there are Unicode normalization libraries available for most popular programming languages.
# RiveScript Discussions

Links to particularly interesting RiveScript discussions.

These are mostly GitHub issues that I wanted to keep track of easily after they're closed. I'll slowly add to this list as I dig up more interesting topics.

## Common Topics

These topics are so common that I use GitHub Issue labels to categorize them.

### Unicode (UTF-8)

* [JavaScript](https://github.com/aichaos/rivescript-js/issues?utf8=%E2%9C%93&q=label%3Aunicode)
* [Python](https://github.com/aichaos/rivescript-python/issues?utf8=%E2%9C%93&q=label%3Aunicode)
* [Perl](https://github.com/aichaos/rivescript-perl/issues?utf8=%E2%9C%93&q=label%3Aunicode)

See also [Unicode Problems](/wiki/Unicode-Problems) on my wiki.

### Async (JS)

Of the programming languages I've ported RiveScript to, JavaScript is the most heavily centered around asynchronous programming. As such it has a lot of discussions on GitHub and even its own wiki page there.

* [Promises for user variable functions](https://github.com/aichaos/rivescript-js/issues/146) - lots of backstory on async in RiveScript.
* [All Async Issues](https://github.com/aichaos/rivescript-js/issues?utf8=%E2%9C%93&q=label%3Aasync%20)
* [Asynchronous Support](https://github.com/aichaos/rivescript-js/wiki/Asynchronous-Support) (wiki)

## Performance and Scale

* [RiveScript Performance](https://github.com/aichaos/rivescript-js/issues/153) (JS)
    * @atladmin had success with 20K replies and no performance dips.
    * Discussion of getting databases involved (RiveScript won't do that).
    * Compliments on RiveScript being high performance with no moving parts, unlike SuperScript (it depends on MongoDB and other deployment headaches).
# Optimize RiveScript

# Problem

None of the RiveScript modules can effectively handle a brain the size of Alice's. The Golang version is able to *load* Alice the fastest (< 1 second) whereas the others take closer to 20+ seconds. However, when actually fetching a reply they all take about 15 seconds.

The root problem is probably in the sorted reply structure, which looks generally like this:

```javascript
sorted = {
    "random": [ // topic name
        ["how are you", pointer ], // triggers ordered by priority
        ["hello bot", pointer ],
        ["*", pointer]
    ]
};
```

Under a topic, all triggers are sorted in their optimal sort order, which is generally: atomic triggers with the most number of words are first, less specific triggers later, least specific last. But triggers with custom priorities (`{weight}` tags, or from a topic that inherits other topics, etc.) always come before lower priority sets of triggers.

In the Alice reply set this means there's about 68,000 triggers in one giant array under the "random" topic, so the code has to scan through several tens of thousands of triggers when finding a match.

# Alicebot Program V

Alicebot Program V is an AIML bot and it stores patterns in a more efficient way: it separates the first word of the pattern away from the rest. When looking up a response for the user, it can then use the first word as a dictionary key (there's a relatively small set of distinct first words), and then have a much simpler array of triggers to look at. Example:

```perl
# The following patterns are represented here:
# ITS *
# ITS BORING
# ITS FUN
# ITS GOOD *

$data = {
   aiml => {
      matches => {
         'ITS' => [
            '* <that> * <topic> * <pos> 17818',
            'BORING <that> * <topic> * <pos> 17819',
            'FUN <that> * <topic> * <pos> 17820',
            'GOOD * <that> * <topic> * <pos> 17821',
         ],
      },
   },
};
```

My [blog entry](/blog/entry/alicebot-program-v) has more details. The `<pos>` refers to an array index where the pattern's details are; in the more recent RiveScript implementations (CoffeeScript and Go) we keep pointers with the triggers in the sorted structure so we don't need to worry about that.

# Complex Triggers

At first glance a Program V style way of sorting triggers looks good, but in RiveScript triggers are much more complicated and "regexp-y", for example:

`(what is|what was) your name`

These things would still need to be taken into account. Also the relative priority of each trigger via `{weight}` and topic inheritance.

# Possible Solution

Change the sort structure to look more like this:

```javascript
sorted = {
    "random": [ // topic name
        [ // these arrays are for priority level, higher on top
            [
                "hello", // first word
                [ // list of triggers under that word
                    ["hello bot", pointer]
                ]
            ],
            ["how", [ ["how are you", pointer] ],
            ["*", [ ["*", pointer] ]
        ]
    ]
}
```

So the logic for matching a trigger would be along these lines:

```python
user_first_word = re.split(r'\s+', message)[0]

for priority in self._sorted.topics[topic]:
    for first_word in priority:
        # this next line would actually be a regexp for * triggers, etc.
        if user_first_word == first_word[0]:
            # Their first word matches! Look through all the triggers for this word.
            for trigger in first_word[1]:
                # Again this would be a regexp in reality
                if message == trigger[0]:
                    # Have a match!
                    matched = trigger[1]

                    # now `matched` points to the trigger's details for the
                    # replies, conditions, etc.
```

For finding the first words, a function like `getFirstWords(trigger)` could be added that returns one or multiple first words.

* If the trigger begins with `[` or `(`, return the first words of all the regexp-y parts.
    * Example: `(what time|when) is it` would return `["what", "when"]`
    * Example: `how are you` would return `["how"]`
* The first words would be sorted by length, with words like `*` at the bottom.
* All triggers that share a first word get placed in an array under that word, sorted in the normal order (most optimal matching first).
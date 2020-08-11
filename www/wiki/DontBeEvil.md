# Mirror of Project Veritas Google Leak 2019

The folders in this repo came from the "Everything" zip (Don't Be Evil.zip); this README
is my own commentary on what's good in the leak.

# Censorship

* Several conversation threads about Breitbart and InfoWars being blocked for hate
  speech and conspiracy theory, respectively.
* A few slides of Google powerpoints suggesting human reviewers of news videos,
  maybe taken out of context, not too interesting.

#### youtube_controversial_query_blacklist.pdf

* a list of keywords that Google blacklists
  from YouTube searches (or videos? not sure)
  * Mass shooting attacks in Las Vegas, New York, Texas etc.
  * Conspiracy theories like Crisis Actors
  * Porn queries
  * Depression? Colgate?
  * Abortion

# Election Tampering

* Just some threads (3 PDF files) of googlers wanting to add an easter egg to Google Translate
  to say what "covfefe" means, which looks like they had problems adding it and
  backed out of the idea altogether.
* Easter egg translates "cov fe'fe" and "covfefe" into `( ̄\_(ツ)_/ ̄)`.
* Had problems with Arabic trying to actually translate it into something else in
  their language and had to roll it back.

Not much to see here.

# Fake News

* Lots of documents on how Google is combatting fake news, by withholding AdSense
  on sites they deem to be misrepresenting information. Sounds reasonable to me.
* Study end-to-end how a publisher's traffic is promoted (i.e. on social media),
  the content of the site, how the publisher represents their content, their
  relationship to other scammers, and other properties by manual human review to
  see if it falls under the Fake News policy. Sounds reasonable.
* Only AdSense is blocked on these Take News Sites, but DoubleClick ads may still
  be used on those sites (global politics and "ads as a platform" standards)

There's also a couple resumes in here of Googlers where they describe the products
they've worked on and the features they've added. Pretty entertaining look at the
"behind the scenes" at Google but nothing crazy jumps out at me. Worked with Google
search ranking algorithms.

#### Fwd_ Fake News-letter 11_27_ Efforts to combat spread of (mis_dis)information - Google Groups.pdf

Some interesting stuff in here:

> Goal: Establish “single point of truth” for definition of “news” across Google products. Mitigate risk of
> low-quality sources and misinformation in Google News corpus.

> Goal: Establish and streamline news escalation processes to detect and handle misinformation across
> products during crises. Install 24/7 team of trained analysts ready to make policy calls and take
> actions across news surfaces including News, News 360 and Feed.

These _could_ be abused maybe? No indication they intend to misuse them.

#### news black list site for google now.txt

```
# Manual list of sites excluded from appearing as Google Now stories to read
# results. The urls are used with a UrlMatcher, and should be in the format
# specified in: webutil/urlutil/urlmatcher.h
```

**Notice:** per the filename and comment at the top of the file, this is a
blacklist for stories appearing in the Google Now app on Android. Some sites
(GTA 5 Mods, APK Mirror) make sense to be suppressed from the feed IMHO.
You also don't want to throw a page from 4Chan on somebody unexpectedly.

Some sites I recognized or have heard of before:

* apkmirror.com: Android app mirror site, not sure why it's on here.
* play.google.com, drive.google.com, docs.google.com
* ebay.com
* torrentfreak.com and several similar (thepiratebay)
* dailystormer.com
* newsbusters.org (pointed out in Veritas interview, I don't otherwise know of it)
* glennbeck.com (know the name, don't know about him though)
* naturalnews.com
* yugiohblog.konami.com: a site about the Yu-Gi-Oh trading card game?
* infowars.com
* smosh.com: YouTuber site
* boards.4chan.org
* queerty.com - LGBT magazine
* voat.co - a Reddit clone, login required now o.O
* ebaumsworld.com
* reddit.com/r/interestingasfuck - oh they even filter by subreddits, how nice
* reddit.com/r/gentlemanboners
* reddit.com/r/exmormon
* dealsplus.com
* gta5-mods.com

Lots of domains that sound like fake news sites, but I didn't check them out myself.
See the file for yourself.

* conservativespirit.com
* toprightnews.com
* hangthebankers.com

This section of the file has what looks like a bunch of fake news sites
(.com.co domain suffix? really?):

```
# START: sites flagged for peddling hoax stories.
abcnews.com.co/
actionnews3.com/
cbsnews.com.co/
channel-7-news.com/
civictribune.com/
drudge-report.co/
independencetribune.com/
nbc.com.co/
neonnettle.com/
now8news.com/
tdtalliance.com/
theracketreport.com/
therightists.com/
thirdestatenewsgroup.com/
tipsforsurvivalists.com/
worldnewsdailyreport.com/
# END: sites flagged for peddling hoax stories.
```

I pinged a few and a lot of them don't even exist anymore.

#### Page level domain restrction 2017_10_02_us_las-vegas-attack-deadliest-us-mass-shooting-trnd_index.pdf

A bug ticket within Google to add "page level domain restriction" on several
links to news articles talking about the Las Vegas attack. Some example pages:

* http://www.cnn.com/2017/10/02/us/las-vegas-attack-deadliest-us-mass-shooting-trnd/index.html
* http://abcnews.go.com/US/wireStory/las-vegas-attack-deadliest-shooting-modern-us-history-50227779
* http://www.foxnews.com/politics/2017/10/02/las-vegas-shooting-lawmakers-condemn-senseless-attack-thank-police.html
* http://www.bbc.co.uk/news/av/world-us-canada-41471532/las-vegas-shooting-witnesses-describe-attack
* http://www.bbc.com/news/av/world-us-canada-41471532/las-vegas-shooting-witnesses-describe-attack

427 URLs in total.

> 3) Are you adding or removing violations?
>
> Add
>
> 4) Which violations would you like to add?
>
> LEGACY_SENSITIVE
>
> 5) Please provide a brief justification for this request.
>
> Las Vegas Mandalay Bay Shooting

Per a commenter in the bug ticket thread this is a "URL takedown request", but
not clear what service. Probably Google Search listing. Could be just adding a
"Sensitive" label to these links too.

#### Realtime Boost.pdf

PowerPoint slide about responding quickly to real-world events.

* Detect real world events
* Is this Query Trending?
* Fast triggering: <5 mins after the event
* Fast serving: 5ms average / 40ms 99% percentile

* They use Twitter as a signal for rapid-fire tweets about breaking news
* Updates Google search autocomplete quickly (type "p" and auto-suggest "prince dead"
  as one example in the slides)

Neat!

# Hiring Practices

To be checked.

# Leadership Training

To be checked.

# Machine Learning Fairness

What it seems they're going for at Google:

* Machine learning collects data from the real world and then produces results
  based on real world data, which isn't always comfortable with people. Things
  like implicit stereotypes or social biases that fully exist in the real world
  get reflected "by default" when machine learning studies the real world.
* Google is working on algorithms to try and steer the "actual results" into a
  more equal output, so no group of people feel marginalized by the Google
  machine learning results.
* Similar in concept to a "random number generator" in many videogames or music
  playing programs aren't _actually_ random and have algorithmic bias to seem
  more in line with what the user expects. If your music player picks the same
  song twice in a row -- that's true randomness and happens, so instead it runs
  an algorithm to be more in line with the ideal expectation of the user.

Some people may have a problem with that and expect that Google Search reflects
the world exactly as it is without changing it and I'm sure arguments could be
made for either side.

The folder contains some examples:

* Google search for "american inventors" returns mostly African American
  inventors (George Washington Carver, Lewis Howard Latimer...).
  * A discussion thread about how it's a bug in the search algorithm.
  * Google Image Team is working on forcing diversity into search results
    to work around the bug.

> **Quote:**
>
> As is the 'our algorithm isn't actually that smart, it's just that
> "African American" has the word "American" in it'

Other examples of why ML Fairness was needed to intervene in Google Search:

* The term "doctor" would primarily return photos of men.
  * Real-world diversity in surgeons: 81% Male, 19% Female
  * 89,000 results for "male surgeon" on Google
  * 119,000 results for "female surgeon" on Google

Still working through powerpoints on this but so far not very worrisome.

# Partisanship

TBD.

# Psychological Research

TBD.

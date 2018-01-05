# Things Learned with jQuery Mobile

## No global top/bottom headers

Each individual page needs the markup for their own header/footer bars. I ended up using Perl Template::Toolkit to build the index.html from a template so I could reuse these components without copying/pasting them all over the place!

## Can't mix it with FontAwesome

Just doesn't work.

## Difficult to mix it with Knockout

This sort of thing doesn't work:

```html
<div data-role="navbar">
	<ul>
		<!-- ko if: logged_in() && my_username() == this_username() -->
			<li>Edit Profile</li>
		<!-- /ko -->
		<li>Other stuff</li>
	</ul>
</div>
```

jQuery Mobile does all the styling and rendering in JS, and if Knockout is hiding DOM elements at this phase, then jQuery Mobile can't style them and they'll look default and stupid.

## Transition performance sucks

Even when you set transitions to `none`, you get a white screen flicker between loading pages on Android 4.3

Most reliable fix as of late is to do this in two parts:

First, disable all transitions in the JS for Android only.

```javascript
$(document).bind("mobileinit", function() {
	if (navigator.userAgent.match(/Android/i)) {
		$.extend($.mobile, {
			defaultPageTransition: "none"
		});
	}
});
```

Secondly, disable hardware acceleration, because the screen will still flash white between pages even with `none` set as the transition. Unfortunately you can't just use `phonegap run android` because it will always set `hardwareAccelerated=true` in the manifest file (even if you manually change it *and* mark the file immutable in Linux). Instead navigate to the Android platform and build it manually.

```bash
cd platforms/android
ant debug
# copy bin/Siikir-debug.apk to your phone or whatever
```

The PhoneGap Build service probably won't be able to do this for you, so for Android you'll always need to build locally.

Allegedly iOS has better hardware acceleration and shouldn't need you to disable transitions or acceleration, and PhoneGap Build should be able to be used. To be investigated.

**Better Solution**

http://www.fishycode.com/post/40863390300/fixing-jquery-mobiles-none-transition-flicker-in

Change from this:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

To:

```html
<meta name="viewport" content="width=device-width, user-scalable=no" />
```

Then HW accel can be used in Android and the flickering is gone too!
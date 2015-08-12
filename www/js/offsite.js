/*
 * Hyperlink Editor Script || Copyright 2014 Kirsle
 *
 * This script makes all offsite links open in a new window.
 */

$(document).ready(function() {
	$("a").each(function() {
		var $a = $(this);
		var href = $a.attr("href");
		if (href === undefined) {
			return;
		}

		// Detect offsite links.
		if (href.indexOf("http:") == 0 || href.indexOf("https:") == 0) {
			$a.attr("target", "_blank");
		}
	});
});

/*
   ##########################################################
   # Hyperlink Editor Script || Copyright 2007 Casey Kirsle #
   #--------------------------------------------------------#
   # This script makes all offsite links open in a new      #
   # window, and turns all e-mail links in the format of    #
   # "name-at-domain.com" into "name@domain.com"            #
   #--------------------------------------------------------#
   # Use content only with permission. Get permission from  #
   # casey "at" cuvou.org                                   #
   ##########################################################
*/
var localAddr = new Array();
localAddr[0] = "kirsle.com";
localAddr[1] = "www.kirsle.com";
localAddr[2] = "kirsle.net";
localAddr[3] = "www.kirsle.net";
localAddr[4] = "kirsle.org";
localAddr[5] = "www.kirsle.org";
localAddr[6] = "epsilon.kirsle.com";
localAddr[7] = "dev.kirsle.com";
localAddr[8] = "www.dev.kirsle.com";
localAddr[9] = "local.kirsle.com";
localAddr[10] = "ds.kirsle.net";
localAddr[11] = "kirsle.noahpwns.com";
localAddr[12] = "localhost";

if (document.getElementsByTagName) {
	var links = document.getElementsByTagName("a");

	for (var i = 0; i < links.length; i++) {
		var loc = links[i].href;

		// Deobfuscate Siikir-encoded e-mail links.
		if (links[i].className == "cms-email") {
			// Rot13-decode everything.
			var parts = links[i].href.split("to=");
			email = rot13(parts[1]);
			var newmail = email.split("+").join("@");
			links[i].href = "mailto:" + newmail;

			// If the label is an e-mail format too, do the same to it.
			var lab = links[i].innerHTML;
			if (lab.indexOf("+") > -1) {
				lab = rot13(lab);
				var newlab = lab.split("+").join("@");
				links[i].innerHTML = newlab;
			}
		}
		else {
			// Continue with link formatting by protocol.
			var parts = loc.split ("/"); // http, null, domain name, request
			var prot = parts[0].split(":");
			var protocol = prot[0];
			protocol.toLowerCase;
			if (protocol == "http" || protocol == "https") {
				// This is an absolute URL.
				var isLocal = 0;

				for (var j = 0; j < localAddr.length; j++) {
					if (parts[2] == localAddr[j]) {
						isLocal = 1;
					}
				}

				if (isLocal == 1) {
					// Local links don't need to be modified.
				}
				else {
					// Remote links need to open in a new window.
					links[i].target = "_blank";
				}
			}
			else if (protocol == "mailto" || protocol=="msnim" || protocol=="xmpp") {
				// MailTo link. See if this isn't a normal link.
				if (loc.indexOf("-at-") > -1) {
					var newhref = loc.split("-at-").join("@");
					links[i].href = newhref;

					// Convert it in the text too.
					if (links[i].innerHTML.indexOf("-at-") > -1) {
						var mailLabel = links[i].innerHTML.split("-at-");
						var newLabel = mailLabel.join ("@");
						links[i].innerHTML = newLabel;
					}
				}
			}
		}
	}
}

function sblogShowMoreTags() {
	if (document.getElementById) {
		document.getElementById("sblog-tags-hidden").style.display = "block";
		document.getElementById("sblog-tags-hiddenlink").style.display = "none";
	}
	return false;
}

/*
   ##########################################################
   # Rot13 Encoder/Decoder Functions                        #
   ##########################################################
*/

function rot13(txt) {
	var result = '';

	for (var i = 0; i < txt.length; i++) {
		var b = txt.charCodeAt(i);

		// 65 = A    97 = a
		// 77 = M   109 = m
		// 78 = N   110 = n
		// 90 = Z   122 = z

		var isLetter = 0;

		if (b >= 65 && b <= 77) {
			isLetter = 1;
			b += 13;
		}
		else if (b >= 97 && b <= 109) {
			isLetter = 1;
			b += 13;
		}
		else if (b >= 78 && b <= 90) {
			isLetter = 1;
			b -= 13;
		}
		else if (b >= 110 && b <= 122) {
			isLetter = 1;
			b -= 13;
		}

		if (isLetter) {
			result += String.fromCharCode(b);
		}
		else {
			result += String.fromCharCode(b);
		}
	}

	return result;
}

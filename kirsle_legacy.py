# -*- coding: utf-8 -*-

# Legacy endpoint compatibility from kirsle.net.

from flask import g, request, redirect, url_for, flash
import re
import os
import json

from rophako.settings import Config
from rophako.app import app
from rophako.utils import template, login_required
import rophako.model.blog as Blog
import rophako.jsondb as JsonDB


@app.route("/+")
def google_plus():
    return redirect("https://plus.google.com/+NoahPetherbridge/posts")


@app.route("/blog.html")
def ancient_legacy_blog():
    post_id = request.args.get("id", None)
    if post_id is None:
        return redirect(url_for("blog.index"))

    # Look up the friendly ID.
    post = Blog.get_entry(post_id)
    if not post:
        flash("That blog entry wasn't found.")
        return redirect(url_for("blog.index"))

    return redirect(url_for("blog.entry", fid=post["fid"]), code=301)


@app.route("/blog/kirsle/<fid>")
def legacy_blog(fid):
    return redirect(url_for("blog.entry", fid=fid), code=301)


@app.route("/rss.cgi")
def legacy_rss():
    return redirect(url_for("blog.rss"), code=301)


@app.route("/firered/<page>")
@app.route("/firered")
def legacy_firered(page=""):
    g.info["page"] = str(page) or "1"
    return template("firered.html")


@app.route("/download", methods=["GET", "POST"])
def legacy_download():
    form = None
    if request.method == "POST":
        form = request.form
    else:
        # CNET links to the MS-DOS download using semicolon delimiters in the
        # query string. Fix that if detected.
        query = request.query_string.decode()
        if not '&' in query and ';' in query:
            url = re.sub(r';|%3b', '&', request.url, flags=re.IGNORECASE)
            return redirect(url)

        form = request.args

    method   = form.get("method", "index")
    project  = form.get("project", "")
    filename = form.get("file", "")

    root = "/home/kirsle/www/projects"

    if project and filename:
        # Filter the sections.
        project = re.sub(r'[^A-Za-z0-9]', '', project) # Project name is alphanumeric only.
        filename = re.sub(r'[^A-Za-z0-9\-_\.]', '', filename)

        # Check that all the files exist.
        if os.path.isdir(os.path.join(root, project)) and os.path.isfile(os.path.join(root, project, filename)):
            # Hit counters.
            hits = { "hits": 0 }
            db = "data/downloads/{}-{}".format(project, filename)
            if JsonDB.exists(db.format(project, filename)):
                hits = JsonDB.get(db)

            # Actually getting the file?
            if method == "get":
                # Up the hit counter.
                hits["hits"] += 1
                JsonDB.commit(db, hits)

            g.info["method"] = method
            g.info["project"] = project
            g.info["file"] = filename
            g.info["hits"] = hits["hits"]
            return template("download.html")

    flash("The file or project wasn't found.")
    return redirect(url_for("index"))


@app.route("/<page>.html")
def legacy_url(page):
    return redirect("/{}".format(page), code=301)


@app.route("/metacity")
def legacy_metacity():
    return redirect("https://github.com/kirsle/linux-themes", code=301)


@app.route("/ssl_test")
@login_required
def ssl_test():
    return "<pre>{}</pre>".format(json.dumps({
        "SSLify criteria": {
            "request.is_secure": request.is_secure,
            "app.debug": app.debug,
            "X-Forwarded-Proto is http": request.headers.get("X-Forwarded-Proto", "http") == "https",
        },
        "App Configuration": {
            "Session cookies secure": app.config["SESSION_COOKIE_SECURE"],
            "config.FORCE_SSL": Config.security.force_ssl,
        },
    }))

import requests
from flask import render_template, session, flash

FEED_URL = "http://localhost:8082/feed"

def feed():
    token = session.get('token')

    if not token:
        flash("You must be logged in to view the feed.", "error")
        return render_template("feed.html", publications=[])

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(FEED_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            publications = data.get("feed", [])
            return render_template("feed.html", publications=publications)
        else:
            flash("Failed to load feed.", "error")
            return render_template("feed.html", publications=[])
    except requests.exceptions.RequestException:
        flash("Feed service is unreachable.", "error")
        return render_template("feed.html", publications=[])

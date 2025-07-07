# routes/followers.py

import requests
from flask import render_template, session, redirect, url_for, flash

#FOLLOWERS_URL = "http://52.0.8.145:8080/followers"
#LOGIN_URL = "http://52.203.72.116:8080/login"
#Api Gateway URLs
FOLLOWERS_URL = "http://107.22.173.138:8080/followers"
LOGIN_URL = "http://107.22.173.138:8080/login"


def followers():
    token = session.get("token")
    if not token:
        flash("You must be logged in to view followers.", "error")
        return redirect(url_for("login"))

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(FOLLOWERS_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            followers_list = data.get("followers", [])
            return render_template("followers.html", followers=followers_list)
        else:
            flash("Failed to retrieve followers.", "error")
    except Exception as e:
        flash(f"Error contacting followers service: {str(e)}", "error")

    return render_template("followers.html", followers=[])

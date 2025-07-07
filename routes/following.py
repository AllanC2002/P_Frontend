import requests
from flask import render_template, redirect, url_for, session, flash

#FOLLOWING_URL = "http://52.205.152.205:8080/following"
#Api Gateway URLs
FOLLOWING_URL = "http://107.22.173.138:8080/following"

def following():
    token = session.get("token")
    if not token:
        flash("You must be logged in to view this page.", "error")
        return redirect(url_for("login"))

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(FOLLOWING_URL, headers=headers)
        if response.status_code == 200:
            following_list = response.json().get("following", [])
        else:
            flash("Failed to retrieve following list.", "error")
            following_list = []
    except Exception as e:
        flash("An error occurred while connecting to the following service.", "error")
        following_list = []

    return render_template("following.html", following=following_list)

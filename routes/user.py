import requests
from flask import render_template, session, flash, request, redirect

SEARCH_URL = "http://107.22.173.138:8080/search-user"
#FOLLOW_URL = "http://54.163.143.185:8080/follow"
#UNFOLLOW_URL = "http://34.203.68.1:8080/unfollow"
FOLLOW_URL = "http://107.22.173.138:8080/follow"
UNFOLLOW_URL = "http://107.22.173.138:8080/unfollow"

def search_user():
    token = session.get('token')
    if not token:
        flash("Login required", "error")
        return redirect("/feed")

    user_mail = request.form.get("user_mail")
    if not user_mail:
        flash("Missing search input", "error")
        return redirect("/feed")

    try:
        response = requests.post(SEARCH_URL, json={"user_mail": user_mail})
        if response.status_code in [200,201]:
            user_data = response.json()
            return render_template("feed.html", publications=[], searched_user=user_data)
        else:
            flash("User not found", "error")
    except Exception as e:
        flash(f"Search error: {str(e)}", "error")

    return redirect("/feed")


def view_user():
    token = session.get('token')
    if not token:
        flash("Login required", "error")
        return redirect("/feed")

    user_mail = request.form.get("userMail")
    if not user_mail:
        flash("Invalid user", "error")
        return redirect("/feed")

    try:
        response = requests.post(SEARCH_URL, json={"user_mail": user_mail})
        if response.status_code == 200:
            user_data = response.json()
            return render_template("user_profile.html", user=user_data)
        else:
            flash("Failed to fetch user profile", "error")
    except Exception as e:
        flash(f"Profile view error: {str(e)}", "error")

    return redirect("/feed")


def follow_user():
    token = session.get('token')
    if not token:
        flash("Login required", "error")
        return redirect("/feed")

    user_id = request.form.get("id_following")
    if not user_id:
        flash("User ID missing", "error")
        return redirect("/feed")

    headers = {"Authorization": f"Bearer {token}"}
    payload = {"id_following": int(user_id)}

    try:
        unfollow_resp = requests.post(UNFOLLOW_URL, json=payload, headers=headers)
        print("UNFOLLOW STATUS:", unfollow_resp.status_code)
        print("UNFOLLOW RESPONSE:", unfollow_resp.text)

        if unfollow_resp.status_code in [200, 201]:
            flash("🚫 User unfollowed!", "success")
        elif unfollow_resp.status_code == 404:
            follow_resp = requests.post(FOLLOW_URL, json=payload, headers=headers)
            print("FOLLOW STATUS:", follow_resp.status_code)
            print("FOLLOW RESPONSE:", follow_resp.text)

            if follow_resp.status_code in [200 in 201]:
                flash("✅ User followed!", "success")
            else:
                flash("❌ Failed to follow user", "error")
        else:
            flash(f"❌ Unexpected error: {unfollow_resp.status_code}", "error")

    except Exception as e:
        flash(f"⚠️ Request error: {str(e)}", "error")

    return redirect("/feed")

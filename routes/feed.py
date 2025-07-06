import requests
from flask import render_template, session, flash, request, redirect

#FEED_URL = "http://54.147.87.111:8080/feed"
#LIKE_URL = "http://52.204.158.214:8080/like"
#UNLIKE_URL = "http://3.222.208.200:8080/unlike"
#GET_LIKES_URL = "http://34.226.18.62:8080/get-likes"
#COMMENT_URL = "http://3.221.235.171:8080/create-comment"
# Api Gateway URLs
FEED_URL = "http://107.22.173.138:8080/feed"
LIKE_URL = "http://107.22.173.138:8080/like"
UNLIKE_URL = "http://107.22.173.138:8080/unlike"
GET_LIKES_URL = "http://107.22.173.138:8080/get-likes"
COMMENT_URL = "http://107.22.173.138:8080/create-comment"
SEARCH_URL = "http://107.22.173.138:8080/search-user"

def get_likes_count(publication_id, token=None):
    if isinstance(publication_id, dict) and "$oid" in publication_id:
        publication_id = publication_id["$oid"]

    if not isinstance(publication_id, str):
        print("Invalid publication ID format:", publication_id)
        return 0

    payload = { "id": publication_id }
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.post("http://34.226.18.62:8080/get-likes", json=payload, headers=headers)
        print("GET-LIKES STATUS:", response.status_code, "FOR ID:", publication_id)
        if response.status_code == 200:
            data = response.json()
            print("GET-LIKES RESPONSE:", data)
            print("Requesting get-likes for:", publication_id)
            return data.get("count", 0)
        else:
            print("Failed get-likes:", response.status_code, response.text)
            print("Requesting get-likes for:", publication_id)
            return 0
    except Exception as e:
        print("Exception get-likes:", str(e))
        return 0
    

def feed():
    token = session.get('token')
    if not token:
        flash("You must be logged in to view the feed.", "error")
        return render_template("feed.html", publications=[])

    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(FEED_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            publications = data.get("feed", [])

            for pub in publications:
                pub_id = pub.get("publication_id") or pub.get("_id")
                if isinstance(pub_id, dict) and "$oid" in pub_id:
                    pub_id = pub_id["$oid"]
                pub["publication_id"] = pub_id
                pub["likes"] = get_likes_count(pub_id, token)
                pub["liked_by_user"] = False  # Esto puedes actualizar luego con lógica real

            return render_template("feed.html", publications=publications)
        else:
            flash("Failed to load feed.", "error")
            return render_template("feed.html", publications=[])
    except requests.exceptions.RequestException:
        flash("Feed service is unreachable.", "error")
        return render_template("feed.html", publications=[])

def toggle_like():
    token = session.get('token')
    if not token:
        flash("Login required to like a publication.", "error")
        return redirect("/feed")

    pub_id = request.form.get("publication_id")
    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Intentar dar like
        like_payload = {"_id": pub_id}
        like_resp = requests.post(LIKE_URL, json=like_payload, headers=headers)
        if like_resp.status_code == 200:
            flash("Liked successfully", "success")
        else:
            # Si ya está dado, intentar unlike
            unlike_payload = {"IdPublication": pub_id}
            unlike_resp = requests.post(UNLIKE_URL, json=unlike_payload, headers=headers)
            if unlike_resp.status_code == 200:
                flash("Unliked successfully", "success")
            else:
                flash("Could not like/unlike.", "error")
    except Exception as e:
        flash(f"Like error: {str(e)}", "error")

    return redirect("/feed")

def comment():
    token = session.get('token')
    if not token:
        flash("Login required to comment.", "error")
        return redirect("/feed")

    pub_id = request.form.get("publication_id")
    comment_text = request.form.get("comment")

    if not pub_id or not comment_text:
        flash("Missing comment or publication.", "error")
        return redirect("/feed")

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "Id_publication": pub_id,
        "Comment": comment_text.strip()
    }

    try:
        response = requests.post(COMMENT_URL, json=payload, headers=headers)
        if response.status_code in [200,201]:
            flash("Comment added", "success")
        else:
            flash("Failed to add comment", "error")
    except Exception as e:
        flash(f"Comment error: {str(e)}", "error")

    return redirect("/feed")


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
        if response.status_code == 200:
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
            return render_template("feed.html", publications=[], viewed_user=user_data)
        else:
            flash("Failed to fetch user profile", "error")
    except Exception as e:
        flash(f"Profile view error: {str(e)}", "error")

    return redirect("/feed")



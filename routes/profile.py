import requests
import base64
from flask import render_template, request, session, flash, redirect, url_for

# Microservicios
GET_PHOTO_URL = "http://174.129.238.113:8080/get-photo"
GET_PUBLICATIONS_URL = "http://3.219.144.22:8080/my-publications"
CREATE_PUBLICATION_URL = "http://35.173.89.233:8080/create-publication"
DELETE_PUBLICATION_URL = "http://44.219.87.84:8080/delete-publication"

def profile():
    token = session.get('token')
    if not token:
        flash("You must be logged in.", "error")
        return redirect(url_for('login'))

    headers = {"Authorization": f"Bearer {token}"}

    # POST: Create a new publication
    if request.method == 'POST':
        text = request.form.get("text", "").strip()
        if not text:
            flash("Publication text is required.", "error")
        else:
            payload = { "Text": text }

            # Imagen opcional
            image_file = request.files.get("image")
            if image_file and image_file.filename != "":
                content_type = image_file.content_type
                image_bytes = image_file.read()
                encoded_image = base64.b64encode(image_bytes).decode("utf-8")
                payload["Multimedia"] = {
                    "image_base64": encoded_image,
                    "content_type": content_type
                }

            # Send the request to create the publication
            try:
                response = requests.post(CREATE_PUBLICATION_URL, json=payload, headers=headers)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get("message", "").lower().startswith("publication created"):
                            flash("Publication created successfully.", "success")
                        else:
                            flash(data.get("message", "Publication saved, but response unclear."), "warning")
                    except Exception:
                        flash("Publication saved, but no readable response.", "warning")
                else:
                    try:
                        flash(response.json().get("message", "Failed to create publication."), "error")
                    except:
                        flash("Failed to create publication.", "error")
            except:
                flash("Publication service unreachable.", "error")

        return redirect(url_for('profile'))

    # GET: Photo of the user
    photo_data = None
    try:
        photo_resp = requests.get(GET_PHOTO_URL, headers=headers)
        if photo_resp.status_code == 200:
            content_type = photo_resp.headers.get("Content-Type", "image/jpeg")
            encoded_image = base64.b64encode(photo_resp.content).decode("utf-8")
            photo_data = f"data:{content_type};base64,{encoded_image}"
    except:
        flash("Could not load profile photo.", "warning")

    # GET: Publications of the user
    publications = []
    try:
        pub_resp = requests.get(GET_PUBLICATIONS_URL, headers=headers)
        if pub_resp.status_code == 200:
            publications = pub_resp.json()
    except:
        flash("Could not load publications.", "warning")

    return render_template("profile.html", photo_data=photo_data, publications=publications)


def delete_publication():
    token = session.get('token')
    if not token:
        flash("Login required.", "error")
        return redirect(url_for('login'))

    publication_id = request.form.get("publication_id")
    if not publication_id:
        flash("Publication ID is missing.", "error")
        return redirect(url_for('profile'))

    headers = {"Authorization": f"Bearer {token}"}
    payload = { "publication_id": publication_id }

    try:
        response = requests.put(DELETE_PUBLICATION_URL, json=payload, headers=headers)
        if response.status_code == 200:
            flash("Publication deleted successfully.", "success")
        else:
            flash("Failed to delete publication.", "error")
    except:
        flash("Delete service unreachable.", "error")

    return redirect(url_for('profile'))

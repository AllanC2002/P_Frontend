import requests
import base64
from flask import render_template, request, session, flash, redirect, url_for

# URLs de los microservicios
GET_PHOTO_URL = "http://174.129.238.113:8080/get-photo"
UPLOAD_PHOTO_URL = "http://13.219.191.189:8080/upload-photo"
UPDATE_PROFILE_URL = "http://44.214.216.202:8080/update-profile"
UPDATE_USER_URL = "http://13.219.132.102:8080/update-user"

def edit():
    token = session.get("token")
    if not token:
        flash("You must be logged in.", "error")
        return redirect(url_for("login"))

    headers = {"Authorization": f"Bearer {token}"}

    # --- FOTO DE PERFIL ---
    photo_url = None
    try:
        response = requests.get(GET_PHOTO_URL, headers=headers)
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "image/jpeg")
            encoded = base64.b64encode(response.content).decode("utf-8")
            photo_url = f"data:{content_type};base64,{encoded}"
    except:
        flash("Could not load profile photo.", "warning")

    # --- PROCESAR FORMULARIOS POST ---
    if request.method == "POST":
        action = request.form.get("action")

        # SUBIR NUEVA FOTO
        if action == "update_photo":
            file = request.files.get("new_photo")
            if file and file.filename:
                try:
                    files = {"file": (file.filename, file.stream, file.content_type)}
                    resp = requests.post(UPLOAD_PHOTO_URL, files=files, headers=headers)
                    if resp.status_code == 200:
                        flash("Profile photo updated.", "success")
                        return redirect(url_for("edit"))
                    else:
                        flash("Failed to upload photo.", "error")
                except:
                    flash("Photo upload service unreachable.", "error")
            else:
                flash("No photo selected.", "warning")

        # ACTUALIZAR INFO DE PERFIL
        elif action == "update_info":
            payload = {}
            if request.form.get("type"): payload["Id_type"] = int(request.form.get("type"))
            if request.form.get("preferences"): payload["Id_preferences"] = int(request.form.get("preferences"))
            if request.form.get("description"): payload["Description"] = request.form.get("description").strip()

            if not payload:
                flash("No profile info provided to update.", "warning")
            else:
                try:
                    resp = requests.patch(UPDATE_PROFILE_URL, json=payload, headers=headers)
                    if resp.status_code == 200:
                        flash("Profile updated successfully.", "success")
                        return redirect(url_for("edit"))
                    else:
                        flash("Failed to update profile.", "error")
                except:
                    flash("Profile update service unreachable.", "error")

        # CAMBIAR CONTRASEÑA Y DATOS PERSONALES
        elif action == "update_password":
            payload = {}
            if request.form.get("name"): payload["Name"] = request.form.get("name").strip()
            if request.form.get("lastname"): payload["Lastname"] = request.form.get("lastname").strip()
            if request.form.get("new_password"): payload["Password"] = request.form.get("new_password")

            if not payload:
                flash("No data provided to update user info.", "warning")
            else:
                try:
                    resp = requests.patch(UPDATE_USER_URL, json=payload, headers=headers)
                    if resp.status_code == 200:
                        flash("User info updated.", "success")
                        return redirect(url_for("edit"))
                    else:
                        flash("Failed to update user info.", "error")
                except:
                    flash("User update service unreachable.", "error")

    # Datos simulados para mostrar en el formulario (puedes integrar una consulta real luego)
    dummy_data = {
        "name": "Allan",
        "lastname": "Correa",
        "preferences": 1,
        "type": 1,
        "description": "I like music."
    }

    return render_template("edit.html", photo_url=photo_url, user_data=dummy_data)

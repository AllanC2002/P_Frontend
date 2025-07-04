import requests
from flask import render_template, request, redirect, url_for, flash, session

# Endpoints
UPDATE_PROFILE_URL = "http://44.214.216.202:8080/update-profile"
UPDATE_USER_URL = "http://13.219.132.102:8080/update-user"
UPLOAD_PHOTO_URL = "http://13.219.191.189:8080/upload-photo"
GET_PHOTO_URL = "http://174.129.238.113:8080/get-photo"

def edit():
    if "token" not in session:
        flash("You must be logged in to edit your profile.", "error")
        return redirect(url_for('login'))

    token = session["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Subir foto de perfil
    if request.method == "POST" and request.form.get("action") == "update_photo":
        image = request.files.get("new_photo")
        if not image or image.filename == "":
            flash("No photo selected.", "error")
        else:
            try:
                files = {"file": image}
                response = requests.post(UPLOAD_PHOTO_URL, headers=headers, files=files)
                if response.status_code == 200:
                    flash("Profile photo updated successfully.", "success")
                else:
                    flash(response.json().get("message", "Failed to upload photo."), "error")
            except Exception:
                flash("Upload service unreachable.", "error")
        return redirect(url_for("edit"))

    # Editar info personal
    elif request.method == "POST" and request.form.get("action") == "update_info":
        success = True

        # Enviar a update-user (nombre, apellido y contraseña)
        user_data = {
            "Name": request.form.get("name"),
            "Lastname": request.form.get("lastname"),
            "Password": request.form.get("password")
        }

        try:
            user_response = requests.patch(UPDATE_USER_URL, json=user_data, headers=headers)
            if user_response.status_code != 200:
                flash("Failed to update name/lastname/password.", "error")
                success = False
        except Exception:
            flash("User update service unreachable.", "error")
            success = False

        # Enviar a update-profile (preferencias, tipo, descripción)
        profile_data = {
            "Description": request.form.get("description"),
            "Id_preferences": int(request.form.get("preferences")),
            "Id_type": int(request.form.get("type"))
        }

        try:
            profile_response = requests.patch(UPDATE_PROFILE_URL, json=profile_data, headers=headers)
            if profile_response.status_code != 200:
                flash("Failed to update profile info.", "error")
                success = False
        except Exception:
            flash("Profile update service unreachable.", "error")
            success = False

        if success:
            flash("Profile updated successfully.", "success")

        return redirect(url_for("edit"))

    # GET: Cargar imagen de perfil para mostrar
    photo_url = None
    try:
        photo_resp = requests.get(GET_PHOTO_URL, headers=headers)
        if photo_resp.status_code == 200:
            content_type = photo_resp.headers.get("Content-Type", "image/jpeg")
            import base64
            encoded_image = base64.b64encode(photo_resp.content).decode("utf-8")
            photo_url = f"data:{content_type};base64,{encoded_image}"
    except:
        pass

    # Datos para poblar el formulario (pueden venir de sesión o simulado)
    dummy_data = {
        "name": "",
        "lastname": "",
        "preferences": 1,
        "type": 1,
        "description": ""
    }

    return render_template("edit.html", photo_url=photo_url, user_data=dummy_data)

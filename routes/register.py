import requests
from flask import render_template, request, redirect, url_for, flash

CREATE_ACCOUNT_URL = "http://3.212.156.160:8080/create_account"

def register():
    if request.method == 'POST':
        data = {
            "Name": request.form.get("Name"),
            "Lastname": request.form.get("Lastname"),
            "User_mail": request.form.get("User_mail"),
            "Password": request.form.get("Password"),
            "Id_type": int(request.form.get("Id_type")),
            "Id_preferences": int(request.form.get("Id_preferences"))
        }

        try:
            response = requests.post(CREATE_ACCOUNT_URL, json=data)
        except requests.exceptions.RequestException:
            flash("Registration service is unreachable.", "error")
            return render_template("register.html")

        if response.status_code == 200:
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('login'))
        else:
            flash(response.json().get('message', 'Registration failed.'), "error")

    return render_template("register.html")

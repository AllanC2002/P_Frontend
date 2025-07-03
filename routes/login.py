import requests
from flask import render_template, request, redirect, url_for, session, flash

LOGIN_SERVICE_URL = "http://52.203.72.116:8080/login"

def login():
    if request.method == 'POST':
        email = request.form.get("User_mail")
        password = request.form.get("password")

        payload = {
            "User_mail": email,
            "password": password
        }

        try:
            response = requests.post(LOGIN_SERVICE_URL, json=payload)
        except requests.exceptions.RequestException as e:
            flash("Login service unreachable.", "error")
            return render_template("login.html")

        if response.status_code == 200:
            data = response.json()
            session['token'] = data.get('token')
            return redirect(url_for('feed'))  # Rute/feed
        else:
            flash("Invalid credentials.", "error")

    return render_template("login.html")

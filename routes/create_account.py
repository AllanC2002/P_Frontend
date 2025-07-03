from flask import render_template, request, redirect, url_for

def create_account():
    if request.method == 'POST':
        data = {
            "Name": request.form.get("Name"),
            "Lastname": request.form.get("Lastname"),
            "User_mail": request.form.get("User_mail"),
            "Password": request.form.get("Password"),
            "Id_type": int(request.form.get("Id_type")),
            "Id_preferences": int(request.form.get("Id_preferences"))
        }

        # Aquí podrías hacer validaciones, enviar a un microservicio o a la base de datos
        print("Received data:", data)

        # Redirigir al login luego del registro exitoso
        return redirect(url_for('login'))  # Asumiendo que tienes la función 'login' registrada

    return render_template('create_account.html')

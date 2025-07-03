from flask import render_template, jsonify, request

def login():
    if request.method == 'POST':
        data = request.get_json()
        print("Received login data:", data)

        if data["User_mail"] == "user@example.com" and data["password"] == "yourpassword":
            print("Login successful")
            return jsonify({"token": "mocked-jwt-token"}), 200
        else:
            print("Login failed")
            return jsonify({"message": "Invalid credentials"}), 401
        
    return render_template('login.html')

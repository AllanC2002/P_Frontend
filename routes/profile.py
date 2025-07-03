from flask import render_template

def profile():
    user_data = {
        "name": "John",
        "lastname": "Doe",
        "email": "john@example.com",
        "description": "Lover of coding and photography.",
        "photo": "images/profile.jpg"
    }

    publications = [
        {"image": "images/post1.jpg", "text": "Sunset by the beach."},
        {"image": "images/post2.jpg", "text": "Coffee vibes."},
        {"image": "images/post3.jpg", "text": "Exploring nature."},
        {"image": "images/post4.jpg", "text": "City lights."},
    ]

    return render_template("profile.html", user=user_data, publications=publications)

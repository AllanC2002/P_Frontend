from flask import Flask, session, redirect, url_for
from routes import home, login, feed, profile, register  
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Session management
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped_view

# Ruotes public
app.add_url_rule('/', view_func=home.home)
app.add_url_rule('/login', view_func=login.login, methods=['GET', 'POST'])
app.add_url_rule('/register', view_func=register.register, methods=['GET', 'POST'])

# Routes proteccted (token required)
app.add_url_rule('/feed', view_func=login_required(feed.feed), methods=['GET', 'POST'])
app.add_url_rule('/profile', view_func=login_required(profile.profile), methods=['GET', 'POST'])
app.add_url_rule('/delete-publication', view_func=login_required(profile.delete_publication), methods=['POST'])


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")

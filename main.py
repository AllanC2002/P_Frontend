from flask import Flask, session, redirect, url_for
from routes import home, login, feed, profile, register, edit, followers, following, user, logout    
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

# Public routes
app.add_url_rule('/', view_func=home.home)
app.add_url_rule('/login', view_func=login.login, methods=['GET', 'POST'])
app.add_url_rule('/register', view_func=register.register, methods=['GET', 'POST'])

# Protected routes
app.add_url_rule('/feed', view_func=login_required(feed.feed), methods=['GET'])
app.add_url_rule('/comment', view_func=login_required(feed.comment), methods=['POST'])
app.add_url_rule('/toggle-like', view_func=login_required(feed.toggle_like), methods=['POST'])
app.add_url_rule('/profile', view_func=login_required(profile.profile), methods=['GET', 'POST'])
app.add_url_rule('/delete-publication', view_func=login_required(profile.delete_publication), methods=['POST'])
app.add_url_rule('/edit', view_func=login_required(edit.edit), methods=['GET', 'POST'])
app.add_url_rule('/followers', view_func=login_required(followers.followers), methods=['GET'])
app.add_url_rule('/following', view_func=login_required(following.following), methods=['GET'])
app.add_url_rule('/search-user', view_func=login_required(feed.search_user), methods=['POST'])
app.add_url_rule('/view-user', view_func=login_required(feed.view_user), methods=['POST'])
app.add_url_rule('/follow-user', view_func=login_required(user.follow_user), methods=['POST'])
app.add_url_rule('/logout', view_func=logout.logout, methods=['GET'])





if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")

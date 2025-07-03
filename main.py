from flask import Flask
from routes import home, login, create_account, feed, profile  

app = Flask(__name__)

# Routes
app.add_url_rule('/', view_func=home.home)
app.add_url_rule('/login', view_func=login.login,methods=['GET', 'POST'])
app.add_url_rule('/register', view_func=create_account.create_account, methods=['GET', 'POST'])
app.add_url_rule('/feed', view_func=feed.feed, methods=['GET', 'POST'])
app.add_url_rule('/profile', view_func=profile.profile, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")

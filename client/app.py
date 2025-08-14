from flask import Flask, render_template, session, redirect, url_for
from auth.routes import auth_bp
from users.routes import users_bp
from contacts.routes import contacts_bp
from config.settings import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(contacts_bp)

@app.route('/')
def index():
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
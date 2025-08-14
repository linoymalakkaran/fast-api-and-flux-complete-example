from flask import Blueprint, render_template, request, redirect, url_for, session
import requests
from config.settings import API_BASE_URL

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f'{API_BASE_URL}/token', data={
            'username': username,
            'password': password
        })
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            role = data.get('role', 'user')  # Default to 'user' if not present
            session['access_token'] = token
            session['username'] = username
            session['role'] = role
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

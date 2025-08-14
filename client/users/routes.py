from flask import Blueprint, render_template, request, redirect, url_for, session
import requests
from utils.api import get_auth_headers
from config.settings import API_BASE_URL

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
def users():
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    response = requests.get(f'{API_BASE_URL}/users', headers=get_auth_headers())
    users = response.json() if response.status_code == 200 else []
    return render_template('users.html', users=users)

@users_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    error = None
    success = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        response = requests.post(f'{API_BASE_URL}/users', json={
            'username': username,
            'password': password,
            'role': role
        }, headers=get_auth_headers())
        if response.status_code == 200 or response.status_code == 201:
            success = 'User added successfully.'
        else:
            error = response.json().get('detail', 'Failed to add user.')
    return render_template('add_user.html', error=error, success=success)

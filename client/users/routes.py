
from flask import Blueprint, render_template, request, redirect, url_for, session
import requests
from utils.api import get_auth_headers
from config.settings import API_BASE_URL

users_bp = Blueprint('users', __name__)

# Delete user route
@users_bp.route('/users/delete/<int:user_id>', methods=['POST', 'GET'])
def delete_user(user_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    response = requests.delete(f'{API_BASE_URL}/users/{user_id}', headers=get_auth_headers())
    if response.status_code == 204:
        return redirect(url_for('users.users'))
    error = response.json().get('detail', 'Failed to delete user.')
    return render_template('users.html', error=error)

# Edit user route
@users_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    error = None
    success = None
    # Fetch user details
    response = requests.get(f'{API_BASE_URL}/users/{user_id}', headers=get_auth_headers())
    if response.status_code != 200:
        error = 'User not found.'
        return render_template('edit_user.html', error=error)
    user = response.json()
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        # Optionally handle password update if needed
        payload = {
            'username': username,
            'role': role
        }
        # If password is provided, add to payload
        password = request.form.get('password')
        if password:
            payload['password'] = password
        put_response = requests.put(f'{API_BASE_URL}/users/{user_id}', json=payload, headers=get_auth_headers())
        if put_response.status_code == 200:
            success = 'User updated successfully.'
            user = put_response.json()
        else:
            error = put_response.json().get('detail', 'Failed to update user.')
    return render_template('edit_user.html', user=user, error=error, success=success)

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
        contacts_json = request.form.get('contacts_json')
        import json
        contacts = json.loads(contacts_json) if contacts_json else []
        payload = {
            'username': username,
            'password': password,
            'role': role,
            'contacts': contacts
        }
        response = requests.post(f'{API_BASE_URL}/users_with_contacts', json=payload, headers=get_auth_headers())
        if response.status_code == 200 or response.status_code == 201:
            success = 'User and related contacts added successfully.'
        else:
            error = response.json().get('detail', 'Failed to add user.')
    return render_template('add_user.html', error=error, success=success)

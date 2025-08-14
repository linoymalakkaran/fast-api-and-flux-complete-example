from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
from utils.api import get_auth_headers
from config.settings import API_BASE_URL

contacts_bp = Blueprint('contacts', __name__)

# List all contacts
@contacts_bp.route('/contacts')
def contacts():
    """Display all contacts."""
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    try:
        response = requests.get(f'{API_BASE_URL}/contacts', headers=get_auth_headers())
        contacts = response.json() if response.status_code == 200 else []
        return render_template('contacts.html', contacts=contacts)
    except Exception as e:
        flash(f"Error fetching contacts: {str(e)}", "danger")
        return render_template('contacts.html', contacts=[])

# Add a new contact
@contacts_bp.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    """Add a new contact."""
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    error = None
    success = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        try:
            response = requests.post(f'{API_BASE_URL}/contacts', json={
                'name': name,
                'email': email,
                'phone': phone,
                'address': address
            }, headers=get_auth_headers())
            if response.status_code == 200 or response.status_code == 201:
                flash('Contact added successfully.', 'success')
                return redirect(url_for('contacts.contacts'))
            else:
                flash(response.json().get('detail', 'Failed to add contact.'), 'danger')
        except Exception as e:
            flash(f"Error adding contact: {str(e)}", "danger")
    return render_template('add_contact.html')

# Edit a contact
@contacts_bp.route('/contacts/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    """Edit an existing contact."""
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        try:
            response = requests.put(f'{API_BASE_URL}/contacts/{contact_id}', json={
                'name': name,
                'email': email,
                'phone': phone,
                'address': address
            }, headers=get_auth_headers())
            if response.status_code == 200:
                flash('Contact updated successfully.', 'success')
                return redirect(url_for('contacts.contacts'))
            else:
                flash(response.json().get('detail', 'Failed to update contact.'), 'danger')
        except Exception as e:
            flash(f"Error updating contact: {str(e)}", "danger")
    else:
        try:
            response = requests.get(f'{API_BASE_URL}/contacts/{contact_id}', headers=get_auth_headers())
            if response.status_code == 200:
                contact = response.json()
                return render_template('edit_contact.html', contact=contact)
            else:
                flash('Contact not found.', 'danger')
                return redirect(url_for('contacts.contacts'))
        except Exception as e:
            flash(f"Error fetching contact: {str(e)}", "danger")
            return redirect(url_for('contacts.contacts'))

# Delete a contact
@contacts_bp.route('/contacts/delete/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    """Delete a contact."""
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    try:
        response = requests.delete(f'{API_BASE_URL}/contacts/{contact_id}', headers=get_auth_headers())
        if response.status_code == 200:
            flash('Contact deleted successfully.', 'success')
        else:
            flash(response.json().get('detail', 'Failed to delete contact.'), 'danger')
    except Exception as e:
        flash(f"Error deleting contact: {str(e)}", "danger")
    return redirect(url_for('contacts.contacts'))

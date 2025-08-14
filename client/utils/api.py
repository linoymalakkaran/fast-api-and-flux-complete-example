from flask import session

def get_auth_headers():
    token = session.get('access_token')
    if token:
        return {'Authorization': f'Bearer {token}'}
    return {}

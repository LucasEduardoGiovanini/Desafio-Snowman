from flask import jsonify

def user_registration_presenter(success,user_email=None):
    if not success:
        return jsonify({'messege': 'O usuário já existe'}), 403
    else:
        return jsonify({'user_email': user_email}), 201
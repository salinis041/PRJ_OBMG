import re
from repository import user_master_repository


def get_users():
    return user_master_repository.list_users()


def get_user(uid):
    return user_master_repository.get_user(uid)


def _form_data(form, editing=False):
    data = {
        'user_type': form.get('user_type', '').strip(),
        'first_name': form.get('first_name', '').strip(),
        'last_name': form.get('last_name', '').strip(),
        'home_phone': form.get('home_phone', '').strip(),
        'mobile_phone': form.get('mobile_phone', '').strip(),
        'work_phone': form.get('work_phone', '').strip(),
        'fax': form.get('fax', '').strip(),
        'email': form.get('email', '').strip(),
        'direct_email': form.get('direct_email', '').strip(),
        'username': form.get('username', '').strip(),
        'password': form.get('password', ''),
        'confirm_password': form.get('confirm_password', ''),
        'change_password': form.get('change_password') == 'on',
        'proxy_uids': [int(v) for v in form.getlist('proxy_uids') if v.isdigit()],
    }
    required = {'User type': data['user_type'], 'First name': data['first_name'],
                'Last name': data['last_name'], 'Username': data['username']}
    if not editing:
        required['Password'] = data['password']
    missing = [label for label, value in required.items() if not value]
    if missing:
        raise ValueError('Please complete the required fields: ' + ', '.join(missing) + '.')
    if len(data['username']) > 30:
        raise ValueError('Username must be 30 characters or fewer.')
    if data['password'] or data['confirm_password']:
        if data['password'] != data['confirm_password']:
            raise ValueError('Password and confirmation do not match.')
        if len(data['password']) < 12:
            raise ValueError('Use a password with at least 12 characters.')
    elif not editing:
        raise ValueError('Password is required.')
    for label, value in [('Email', data['email']), ('Direct email', data['direct_email'])]:
        if value and not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', value):
            raise ValueError('Enter a valid ' + label.lower() + ' address.')
    return data


def create_user(form):
    return user_master_repository.create_user(_form_data(form, editing=False))


def update_user(uid, form):
    return user_master_repository.update_user(uid, _form_data(form, editing=True))

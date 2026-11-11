from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from service import user_master_service

user_master_routes = Blueprint('user_master_routes', __name__, url_prefix='/user-master')


@user_master_routes.route('/index', methods=['GET'])
def index():
    try:
        users = user_master_service.get_users()
    except Exception:
        current_app.logger.exception('Could not load User Master')
        flash('Could not load User Master. Check the database tables and application log.', 'error')
        users = []
    return render_template('user_master.html', users=users)


@user_master_routes.route('/new', methods=['GET', 'POST'])
def create():
    try:
        users = user_master_service.get_users()
    except Exception:
        current_app.logger.exception('Could not load users for creation form')
        users = []
    if request.method == 'POST':
        try:
            new_uid = user_master_service.create_user(request.form)
            flash(f'User created successfully (UID: {new_uid}).', 'success')
            return redirect(url_for('user_master_routes.index'))
        except ValueError as exc:
            flash(str(exc), 'error')
        except Exception:
            current_app.logger.exception('User creation failed')
            flash('The user could not be created. Check the PyCharm Run console for details.', 'error')
    return render_template('user_master_form.html', users=users, user=None, is_edit=False)


@user_master_routes.route('/<int:uid>/edit', methods=['GET', 'POST'])
def edit(uid):
    try:
        user = user_master_service.get_user(uid)
        if user is None:
            flash('User not found.', 'error')
            return redirect(url_for('user_master_routes.index'))
        users = user_master_service.get_users()
        if request.method == 'POST':
            user_master_service.update_user(uid, request.form)
            flash(f'User {uid} updated successfully.', 'success')
            return redirect(url_for('user_master_routes.index'))
        return render_template('user_master_form.html', users=users, user=user, is_edit=True)
    except ValueError as exc:
        flash(str(exc), 'error')
    except Exception:
        current_app.logger.exception('User update failed')
        flash('The user could not be updated. Check the PyCharm Run console for details.', 'error')
    user = user_master_service.get_user(uid)
    users = user_master_service.get_users()
    return render_template('user_master_form.html', users=users, user=user, is_edit=True)

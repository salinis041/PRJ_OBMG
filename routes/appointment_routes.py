from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from service import appointment_service

appointment_routes = Blueprint('appointment_routes', __name__, url_prefix='/appointments')


def _form_page(appointment=None, is_edit=False):
    providers = appointment_service.get_providers()
    if not providers:
        flash("No active users with User Type 'Provider' were found.", 'error')
    return render_template('appointments_form.html', appointment=appointment,
                           providers=providers, is_edit=is_edit)


@appointment_routes.route('/', methods=['GET'])
def index():
    try:
        appointments = appointment_service.get_appointments()
    except Exception:
        current_app.logger.exception('Could not load appointments')
        flash('Could not load appointments. Check that dbo.Appmnt exists.', 'error')
        appointments = []
    return render_template('appointments.html', appointments=appointments)


@appointment_routes.route('/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            appointment_service.create_appointment(request.form)
            flash('Appointment created successfully.', 'success')
            return redirect(url_for('appointment_routes.index'))
        except ValueError as exc:
            flash(str(exc), 'error')
        except Exception:
            current_app.logger.exception('Appointment creation failed')
            flash('Appointment could not be created. Check the PyCharm Run console.', 'error')
    return _form_page()


@appointment_routes.route('/<int:aid>/edit', methods=['GET', 'POST'])
def edit(aid):
    appointment = appointment_service.get_appointment(aid)
    if appointment is None:
        flash('Appointment not found.', 'error')
        return redirect(url_for('appointment_routes.index'))
    if request.method == 'POST':
        try:
            appointment_service.update_appointment(aid, request.form)
            flash('Appointment updated successfully.', 'success')
            return redirect(url_for('appointment_routes.index'))
        except ValueError as exc:
            flash(str(exc), 'error')
        except Exception:
            current_app.logger.exception('Appointment update failed')
            flash('Appointment could not be updated. Check the PyCharm Run console.', 'error')
    return _form_page(appointment, True)

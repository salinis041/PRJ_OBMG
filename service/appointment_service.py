from datetime import datetime
from repository import appointment_repository


def get_providers():
    return appointment_repository.list_providers()


def get_appointments(acct=None):
    return appointment_repository.list_appointments(acct=acct)


def get_appointment(aid):
    return appointment_repository.get_appointment(aid)


def _flag(form, name):
    return 'Y' if form.get(name) == 'on' else 'N'


def parse_form(form):
    date_value = form.get('app_date', '').strip()
    if not date_value:
        raise ValueError('Appointment date is required.')
    try:
        datetime.strptime(date_value, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Enter a valid appointment date.')
    provider = form.get('provider_id', '').strip()
    if not provider.isdigit():
        raise ValueError('Please select a provider.')
    record_type = form.get('record_type', 'N').strip().upper()
    if record_type not in ('N', 'L'):
        raise ValueError('Select a valid record type.')
    return {
        'acct': form.get('acct', '').strip() or None,
        'mrn': form.get('mrn', '').strip() or None,
        'record_type': record_type,
        'provider_id': int(provider),
        'address': form.get('address', '').strip() or None,
        'date': date_value,
        'time': form.get('app_time', '').strip() or None,
        'status': form.get('app_status', '').strip() or 'Pending',
        'instructions': form.get('app_instr', '').strip() or None,
        'established': _flag(form, 'established'),
        'discharge': _flag(form, 'discharge'),
        'in_network': _flag(form, 'in_network'),
        'restricted_insurance': _flag(form, 'restricted_insurance'),
        'chosen_patient': _flag(form, 'chosen_patient'),
        'assigned_insurance': _flag(form, 'assigned_insurance'),
        'availability': _flag(form, 'availability'),
        'far_hospital': _flag(form, 'far_hospital'),
        'chosen_pcp': _flag(form, 'chosen_pcp'),
        'selection_notes': form.get('selection_notes', '').strip() or None,
    }


def create_appointment(form, user_id=None):
    appointment_repository.save_appointment(parse_form(form), user_id=user_id)


def update_appointment(aid, form, user_id=None):
    appointment_repository.save_appointment(parse_form(form), user_id=user_id, aid=aid)

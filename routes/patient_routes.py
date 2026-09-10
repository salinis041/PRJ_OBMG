from flask import Blueprint, render_template

from service.patient_service import get_patient_list


patient_routes = Blueprint(
    "patient_routes",
    __name__
)


@patient_routes.route("/")
def patients():

    patients = get_patient_list()

    return render_template(
        "patients.html",
        patients=patients
    )
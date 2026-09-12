from flask import Blueprint, render_template

from service.patcoordi_service import get_patCordinat_list
from service.patient_service import get_patient_list

coodinator_routes = Blueprint(
    "coodinator_routes",
    __name__
)


@coodinator_routes.route("/")
def patients():

    patients = get_patCordinat_list()
    # for x in patients:
    #  print(x)
    return render_template(
        "coordin_home.html",
        patients=patients
    )
@coodinator_routes.route("/patient")
def user_home():
    patients = get_patient_list()
    return render_template("patients.html",
        patients=patients)
@coodinator_routes.route("/home")
def home():
    patients = get_patCordinat_list()
    # for x in patients:
    #  print(x)
    return render_template(
        "coordin_home.html",
        patients=patients
    )
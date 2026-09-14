from flask import Blueprint, render_template

from service.patcoordi_service import get_patCordinat_list,get_patCordinat_Visit
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
        patts=patients
    )
    # return render_template(
    #     "coordin_main.html",
    #     patients=patients
    # )
@coodinator_routes.route("/patient")
def user_home():
    patients = get_patient_list()
    return render_template("patients.html",
        patients=patients)
@coodinator_routes.route("/home")
def home():
    pat = get_patCordinat_list()
    # for x in pat:
    #  print(x)
    return render_template(
        "coordin_home.html",
        patts=pat
    )
@coodinator_routes.route("/CoordinatorMain/<visit_id>")
def Coordinatormain(visit_id):
    # print(visit_id)
    patvisit = get_patCordinat_Visit(visit_id)
    # for x in patvisit:
    #  print(x)
    return render_template(
        "coordin_main.html",
        patv=patvisit
    )
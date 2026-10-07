from flask import Blueprint, render_template, request, jsonify

from service.patcoordi_service import get_patCordinat_list,get_patCordinat_Visit,get_patVisit
from service.patient_service import get_patient_list
from ldap3 import Server, Connection, NTLM

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
        "login.html"
    )
    # return render_template(
    #     "coordin_home.html",
    #     patts=patients
    # )
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
@coodinator_routes.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Username and password are required"
        }), 400

    domain = "POLLYRYON"
    server_address = "OMC-PDC01.pollyryon.org"

    try:

        server = Server(
            server_address,
            port=389,
            get_info="NONE"
        )

        user = f"{domain}\\{username}"

        print("======================================")
        print("AD LOGIN ATTEMPT")
        print("Server   :", server_address)
        print("Domain   :", domain)
        print("User     :", user)
        print("======================================")

        conn = Connection(
            server,
            user=user,
            password=password,
            authentication=NTLM,
            auto_bind=False
        )

        if conn.bind():

            print("AD BIND SUCCESS")
            print("Result:", conn.result)

            conn.unbind()

            return jsonify({
                "success": True,
                "message": "Login successful"
            })

        print("AD BIND FAILED")
        print("Result:", conn.result)

        result = conn.result

        conn.unbind()

        return jsonify({
            "success": False,
            "message": "AD authentication failed",
            "details": str(result)
        }), 401

    except Exception as e:

        print("AD CONNECTION ERROR")
        print("Error type:", type(e).__name__)
        print("Error:", str(e))

        return jsonify({
            "success": False,
            "message": "AD authentication failed",
            "error_type": type(e).__name__,
            "error": str(e)
        }), 401

@coodinator_routes.route("/Demographics/<visit_id>")
def Demographics(visit_id):
    # print(visit_id)
    patvisit = get_patVisit(visit_id)
    # for x in patvisit:
    #  print(x)
    return render_template(
        "pat_demographics.html",
        patv=patvisit
    )
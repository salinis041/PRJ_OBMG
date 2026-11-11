from flask import (Blueprint, render_template, request,
                   session, jsonify,json, redirect, url_for, flash, current_app)

from service.patcoordi_service import (get_patCordinat_list,get_patCordinat_Visit,
                                       get_patVisit,get_EnTask_list_VId,get_EnTaskCont_VId,get_patVisit,get_user_list,get_EnTaskVId
,get_EnTask_list_TId,addedit_ETask,get_EnTaskCmnt_VstId)
from service.patient_service import get_patient_list
from service.provider_service import get_provider_list
from service import appointment_service

from ldap3 import Server, Connection, NTLM

coodinator_routes = Blueprint(
    "coodinator_routes",
    __name__
)


@coodinator_routes.route("/")
def patients():
    # search = request.args.get(
    #     "search",
    #     default="",
    #     type=str
    # )
    #
    # data = get_provider_list(
    #     search=search
    # )


    #patients = get_patCordinat_list()
    # for x in data:
    #  print(x)
    # return render_template(
    #     "provider.html",
    #     details=data["details"],
    #     search=search
    # )
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
# @coodinator_routes.route("/CoordinatorMain/<visit_id>")
# def Coordinatormain(visit_id):
#     # print(visit_id)
#     session['Vst'] = visit_id
#     patvisit = get_patCordinat_Visit(visit_id)
#     # for x in patvisit:
#     #  print(x)
#     return render_template(
#         "coordin_main.html",
#         patv=patvisit
#     )
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

        conn = Connection(
            server,
            user=f"{domain}\\{username}",
            password=password,
            authentication=NTLM,
            auto_bind=True
        )

        if conn.bound:
            conn.unbind()

            return jsonify({
                "success": True,
                "message": "Login successful"
            })

        result = conn.result
        conn.unbind()

        return jsonify({
            "success": False,
            "message": "AD authentication failed",
            "details": str(result)
        }), 401

    except Exception as e:

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
@coodinator_routes.route("/EncouterTask/<string:mrn>/<string:vist>", methods=["POST"])
def Generate_EncounterTask(mrn,vist):

    # data = request.json or {}
    # delusrname = data.get("delUsername")
    # print(vist)
    # print(mrn)
    TaslList = get_EnTask_list_VId(mrn,vist)
    TaskCount = get_EnTaskCont_VId(vist)

    return jsonify({
        "success": True,
        "TaslList": TaslList,
        "TaskCount": TaskCount
    })
@coodinator_routes.route("/EncounterLoad", methods=['GET'])
def EncounterLoad():
    # print(visit_id)
    VisitId=session['Vst']
    print(VisitId)
    TaslList = get_EnTaskVId(VisitId)
    TaskCount = get_EnTaskCont_VId(VisitId)
    # for x in patvisit:
    #  print(x)
    return jsonify({
        "success": True,
        "TaslList": TaslList,
        "TaskCount": TaskCount
    })
#
@coodinator_routes.route("/EncoutTaskTID/<TId>/<string:vist>", methods=["POST"])
def EncoutTaskTID(TId,vist):

    # data = request.json or {}
    # delusrname = data.get("delUsername")
    # print(vist)
    # print(mrn)
    TaskDetails = get_EnTask_list_TId(TId)
    TaskCmnt = get_EnTaskCmnt_VstId(vist)
    return jsonify({
        "success": True,
        "TaskDetails": TaskDetails,
        "TaskCmnt": TaskCmnt
    })
@coodinator_routes.route('/edit_EncouterTask', methods=['POST'])
def edit_EncouterTask():
    data = request.form.to_dict()
    commentData = json.loads(request.form.get("commentData", "[]"))
    print(commentData)
    try:
        TaslList = addedit_ETask(data,commentData)

        TaskCount=get_EnTaskCont_VId(data.get("vist"))

        return jsonify({
        "success": True,
        "TaslList": TaslList,
        "TaskCount": TaskCount
    })

    except Exception  as e:
        traceback.print_exc()

        return jsonify({
            "inserted": False,
            "message": str(e)
        }), 500
@coodinator_routes.route("/CoordinatorMain/<visit_id>", methods=["GET"])
def Coordinatormain(visit_id):
    session['Vst'] = visit_id
    patvisit = get_patCordinat_Visit(visit_id)
    usrlist = get_user_list()
    appointment_rows = []
    providers = []
    selected_appointment = None
    try:
        current_account = patvisit[0].get("AccountNumber") if patvisit else visit_id
        appointment_rows = appointment_service.get_appointments(acct=current_account)
        providers = appointment_service.get_providers()
        edit_id = request.args.get("edit_appointment", type=int)
        if edit_id:
            selected_appointment = appointment_service.get_appointment(edit_id)
    except Exception:
        current_app.logger.exception("Could not load appointment tab data")
        flash("Appointment information could not be loaded. Check the server log.", "error")

    return render_template(
        "coordin_main.html",
        patv=patvisit,
        usrlist=usrlist,
        appointments=appointment_rows,
        appointment_providers=providers,
        appointment_form_open=bool(request.args.get("add_appointment") or selected_appointment),
        appointment=selected_appointment,
        appointment_is_edit=selected_appointment is not None
    )


@coodinator_routes.route("/CoordinatorMain/<visit_id>/appointment", methods=["POST"])
def save_coordinator_appointment(visit_id):
    aid = request.form.get("aid", type=int)
    try:
        if aid:
            appointment_service.update_appointment(aid, request.form)
            flash("Appointment updated successfully.", "success")
        else:
            appointment_service.create_appointment(request.form)
            flash("Appointment created successfully.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("coodinator_routes.Coordinatormain",
                                visit_id=visit_id,
                                edit_appointment=aid) if aid else
                        url_for("coodinator_routes.Coordinatormain",
                                visit_id=visit_id, add_appointment=1) + "#appoint")
    except Exception:
        current_app.logger.exception("Appointment save failed")
        flash("Appointment could not be saved. Check the server log.", "error")
    return redirect(url_for("coodinator_routes.Coordinatormain", visit_id=visit_id) + "#appoint")


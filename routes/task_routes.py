from flask import (Blueprint, render_template, request,
                   session, jsonify,json, redirect, url_for, )
from service.task_service import (get_EnTask_list)
from service.patcoordi_service import (get_user_list)

task_routes = Blueprint(
    "task_routes",
    __name__
)
@task_routes.route("/tasks_home")
def tasks_home():
    usrlist = get_user_list()
    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    search = request.args.get(
        "search",
        default="",
        type=str
    )
    search2 = request.args.get(
        "search2",
        default="",
        type=str
    ).strip()

    data = get_EnTask_list(
        page=page,
        search=search,
        search2=search2)
    return render_template("Tasks.html",
        tasklist=data["details"],
        usrlist=usrlist,
        total_records=data["total_records"],
        total_pages=data["total_pages"],
        start_record=data["start_record"],
        end_record=data["end_record"],
        page_numbers=data["page_numbers"],
        page=page,
        search=search,
        search2=search2)

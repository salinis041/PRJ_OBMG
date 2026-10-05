from flask import Blueprint, render_template, request, redirect, url_for, flash

from service.available_details_service import get_available_details_page
from service.added_details_service import add_detail


available_details_routes = Blueprint(
    "available_details_routes",
    __name__
)


@available_details_routes.route("/details", methods=["GET"])
def available_details():

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

    data = get_available_details_page(
        page=page,
        search=search
    )

    return render_template(
        "available_details.html",
        details=data["details"],
        total_records=data["total_records"],
        total_pages=data["total_pages"],
        start_record=data["start_record"],
        end_record=data["end_record"],
        page_numbers=data["page_numbers"],
        page=page,
        search=search
    )


@available_details_routes.route(
    "/details/add",
    methods=["POST"]
)
def add_available_detail():

    visit_id = request.form.get("visit_id")

    search = request.form.get(
        "search",
        ""
    )

    page = request.form.get(
        "page",
        "1"
    )

    if not visit_id:
        flash("Please select a patient first.")

        return redirect(
            url_for(
                "available_details_routes.available_details",
                page=page,
                search=search
            )
        )

    result = add_detail(visit_id)

    flash(result)

    return redirect(
        url_for(
            "available_details_routes.available_details",
            page=page,
            search=search
        )
    )
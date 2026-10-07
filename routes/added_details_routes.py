from flask import (
    Blueprint,
    render_template, request
)

from service.added_details_service import (
    get_added_Visit_list
)


added_details_routes = Blueprint(
    "added_details_routes",
    __name__
)


@added_details_routes.route(
    "/added-details"
)
def added_details():
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

    data = get_added_Visit_list(
        page=page,
        search=search,
        search2=search2
    )


    # return render_template(
    #     "added_details.html",
    #     details=details
    # )
    return render_template(
        "added_details.html",
        details=data["details"],
        total_records=data["total_records"],
        total_pages=data["total_pages"],
        start_record=data["start_record"],
        end_record=data["end_record"],
        page_numbers=data["page_numbers"],
        page=page,
        search=search,
        search2=search2
    )

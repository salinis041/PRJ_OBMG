from flask import (
    Blueprint,
    render_template
)

from service.added_details_service import (
    get_added_details_list
)


added_details_routes = Blueprint(
    "added_details_routes",
    __name__
)


@added_details_routes.route(
    "/added-details"
)
def added_details():

    details = get_added_details_list()

    return render_template(
        "added_details.html",
        details=details
    )
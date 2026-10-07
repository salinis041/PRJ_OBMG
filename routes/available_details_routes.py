from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)

from repository.available_details_repository import (
    get_available_details_page,
    get_available_visit,
    get_full_remote_visit,
)

from repository.visits_repository import (
    visit_exists,
    insert_visit,
    update_visit,
)


available_details_routes = Blueprint(
    "available_details_routes",
    __name__
)


# ============================================================
# AVAILABLE DETAILS PAGE
# ============================================================

@available_details_routes.route(
    "/details",
    methods=["GET"]
)
def available_details():

    mode = request.args.get(
        "mode",
        "census"
    ).strip().lower()

    visit_id = request.args.get(
        "visit_id",
        ""
    ).strip()

    search = request.args.get(
        "q",
        ""
    ).strip()


    # ========================================================
    # SEARCH BY VISIT ID / ACCOUNT NUMBER MODE
    # ========================================================
    #
    # IMPORTANT:
    # Even when visit_id is empty, we MUST remain in
    # visit mode. This is what allows the radio button to
    # switch correctly.
    # ========================================================

    if mode == "visit":

        visit = None

        if visit_id:

            visit = get_available_visit(
                visit_id
            )

        return render_template(
            "available_details.html",

            mode="visit",

            visit_id=visit_id,

            visit=visit,

            details=None,

            total_records=0,

            total_pages=0,

            start_record=0,

            end_record=0,

            page_numbers=[],

            page=1,

            search=""
        )


    # ========================================================
    # CURRENT CENSUS MODE
    # ========================================================

    page = request.args.get(
        "page",
        1,
        type=int
    )

    if page < 1:
        page = 1


    census = get_available_details_page(
        page=page,
        search=search
    )


    return render_template(
        "available_details.html",

        mode="census",

        visit_id="",

        visit=None,

        **census
    )


# ============================================================
# ADD AVAILABLE DETAIL
# ============================================================

@available_details_routes.route(
    "/details/add",
    methods=["POST"]
)
def add_available_detail():

    visit_id = request.form.get(
        "visit_id",
        ""
    ).strip()


    if not visit_id:

        return jsonify({
            "inserted": False,
            "exists": False,
            "error": "Account Number is required."
        }), 400


    try:

        # ----------------------------------------------------
        # Page 6 sends the external Account Number.
        # This is vst_ext_id.
        # ----------------------------------------------------

        data = get_full_remote_visit(
            visit_id
        )


        if not data:

            return jsonify({
                "inserted": False,
                "exists": False,
                "error": "The visit could not be found."
            }), 404


        # ----------------------------------------------------
        # Account Number must come from vst_ext_id.
        # ----------------------------------------------------

        account_number = data.get(
            "Account Number"
        )


        if not account_number:

            return jsonify({
                "inserted": False,
                "exists": False,
                "error": "The Account Number could not be determined."
            }), 500


        # ----------------------------------------------------
        # Check whether Account Number already exists.
        # ----------------------------------------------------

        if visit_exists(
            account_number
        ):

            return jsonify({
                "inserted": False,
                "exists": True,
                "visit_id": account_number
            })


        # ----------------------------------------------------
        # Insert the complete visit.
        # ----------------------------------------------------

        inserted = insert_visit(
            data
        )


        if not inserted:

            return jsonify({
                "inserted": False,
                "exists": True,
                "visit_id": account_number
            })


        # ----------------------------------------------------
        # Redirect using Account Number.
        # ----------------------------------------------------

        redirect_url = (
            "/Demographics/"
            + str(account_number)
        )


        return jsonify({
            "inserted": True,
            "exists": False,
            "visit_id": account_number,
            "redirect_url": redirect_url
        })


    except Exception as exc:

        return jsonify({
            "inserted": False,
            "exists": False,
            "error": str(exc)
        }), 500


# ============================================================
# UPDATE EXISTING AVAILABLE DETAIL
# ============================================================

@available_details_routes.route(
    "/details/update",
    methods=["POST"]
)
def update_available_detail():

    visit_id = request.form.get(
        "visit_id",
        ""
    ).strip()


    if not visit_id:

        return jsonify({
            "updated": False,
            "error": "Account Number is required."
        }), 400


    try:

        # ----------------------------------------------------
        # Fetch the latest complete remote visit.
        # ----------------------------------------------------

        data = get_full_remote_visit(
            visit_id
        )


        if not data:

            return jsonify({
                "updated": False,
                "error": "The visit could not be found."
            }), 404


        account_number = data.get(
            "Account Number"
        )


        if not account_number:

            return jsonify({
                "updated": False,
                "error": "The Account Number could not be determined."
            }), 500


        # ----------------------------------------------------
        # Update local record.
        # ----------------------------------------------------

        update_visit(
            data
        )

        redirect_url = (
                "/Demographics/"
                + str(account_number)
        )


        return jsonify({
            "updated": True,
            "visit_id": account_number,
            "redirect_url": redirect_url
        })


    except Exception as exc:

        return jsonify({
            "updated": False,
            "error": str(exc)
        }), 500
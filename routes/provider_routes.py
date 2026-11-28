from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,url_for
)
import traceback
import json
from service.provider_service import (register_user,get_provider_list,get_provider_list_UId
,addedit_provider,get_provider_Addlist_UId,delete_providerAddress)
provider_routes = Blueprint(
    "provider_routes",
    __name__
)
@provider_routes.route('/provider/add', methods=['POST'])
def add_provider():
    data = request.form.to_dict()

    try:
        result = register_user(data)
        search = request.args.get(
            "search",
            default="",
            type=str
        )

        data = get_provider_list(
            search=search
        )

        return render_template(
            "provider.html",
            details=data["details"],
            search=search
        )

        # return jsonify({
        #     "inserted": True,
        #     "exists": False,
        #     "message": "Provider added successfully",
        #     "visit_id": result,
        #     "redirect_url": ""
        # }), 200

    except Exception:


        return jsonify({
            "inserted": False,
            "message": "Failed to add provider"
        }), 500


@provider_routes.route(
    "/prov_details"
)
def prov_details():


    search = request.args.get(
        "search",
        default="",
        type=str
    )


    data = get_provider_list(
        search=search
    )


    # return render_template(
    #     "added_details.html",
    #     details=details
    # )
    return render_template(
        "provider.html",
        details=data["details"],
        search=search
    )
@provider_routes.route('/provider/<int:user_id>', methods=['GET'])
def get_provider(user_id):
    provider = get_provider_list_UId(user_id)
    AddList = get_provider_Addlist_UId(user_id)
    # print(AddList)
    # print(provider)
    # for x in provaddlist:
    #  print(x)
    if not AddList:
        return jsonify({"error": "Provider address not found"}), 404
    return jsonify({
        "success": True,
        "provider": provider,
        "AddList": AddList
    })

    # return jsonify(provider)
@provider_routes.route('/providerUser/<int:user_id>', methods=['GET'])
def get_providerUser(user_id):
    provider = get_provider_list_UId(user_id)

    # print(provider)
    # for x in provaddlist:
    #  print(x)
    # if not AddList:
    #     return jsonify({"error": "Provider address not found"}), 404
    # return jsonify({
    #     "success": True,
    #     "provider": provider,
    #     "AddList": AddList
    # })

    return jsonify(provider)
@provider_routes.route('/provider/edit', methods=['POST'])
def edit_provider():
    data = request.form.to_dict()
    addresses = json.loads(request.form.get("addresses", "[]"))


    try:
        result = addedit_provider(data,addresses)
        search = request.args.get(
            "search",
            default="",
            type=str
        )

        data = get_provider_list(
            search=search
        )

        # return render_template(
        #     "provider.html",
        #     details=data["details"],
        #     search=search
        # )

        return jsonify({
            "inserted": True,
            "message": "Provider added successfully",
            "visit_id": result,
            "redirect_url": url_for(
                'provider_routes.prov_details'
            )
        }), 200

        # return jsonify({
        #     "inserted": True,
        #     "exists": False,
        #     "message": "Provider added successfully",
        #     "visit_id": result,
        #     "redirect_url": ""
        # }), 200

    except Exception  as e:
        traceback.print_exc()

        return jsonify({
            "inserted": False,
            "message": str(e)
        }), 500
        # return jsonify({
        #     "inserted": False,
        #     "message": "Failed to add provider"
        # }), 500
@provider_routes.route('/provider/delete-address/<int:address_id>', methods=['POST'])
def delete_address(address_id):

    try:
        result = delete_providerAddress(address_id)



        return jsonify({
            "success": True,
            "message": "Address deleted successfully",
            "result": result
        })

    except Exception as e:
        print("Address Delete Error:", repr(e))

        return jsonify({
            "success": False,
            "message": "Unable to delete address"
        }), 500


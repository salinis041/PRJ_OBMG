from repository.visits_repository import (
    visit_exists,
    insert_visit,
    update_visit,
)


def save_visit(data):
    """
    Insert the visit if it does not already exist.

    Account Number is the external visit identifier
    (remote vst_ext_id) and is stored in dbo.Visits.AccountNumber.

    Returns:
        "inserted" -> new visit inserted
        "exists"   -> visit already exists
    """

    account_number = data.get(
        "Account Number"
    )

    if not account_number:
        raise ValueError(
            "Account Number is required."
        )

    if visit_exists(
        account_number
    ):
        return "exists"

    inserted = insert_visit(
        data
    )

    if inserted:
        return "inserted"

    return "exists"


def update_saved_visit(data):
    """
    Update an existing visit.

    Account Number is the external visit identifier
    stored in dbo.Visits.AccountNumber.

    Returns:
        "updated" -> visit updated successfully
        "not_found" -> visit does not exist
    """

    account_number = data.get(
        "Account Number"
    )

    if not account_number:
        raise ValueError(
            "Account Number is required."
        )

    if not visit_exists(
        account_number
    ):
        return "not_found"

    updated = update_visit(
        data
    )

    if updated:
        return "updated"

    return "not_found"
from repository.added_details_repository import (
    get_added_details,
    insert_added_detail
)


def get_added_details_list():
    """
    Get all records that have already been added
    to the application database.
    """
    return get_added_details()


def add_detail(visit_id):
    """
    Add one selected patient visit.
    """
    return insert_added_detail(visit_id)
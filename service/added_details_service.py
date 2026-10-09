import math
from repository.added_details_repository import (
    get_added_details,
    insert_added_detail,get_added_Visitdetails,
    get_available_details_count
)


def get_added_details_list():
    """
    Get all records that have already been added
    to the application database.
    """
    return get_added_details()
PAGE_SIZE = 50
def get_added_Visit_list(page=1,
    search=None,
    search2=None):
    if page < 1:
        page = 1

    details = get_added_Visitdetails(
        page=page,
        search=search,
        search2=search2
    )

    total_records = get_available_details_count(
        search=search,
        search2=search2
    )

    total_pages = math.ceil(
        total_records / PAGE_SIZE
    )

    start_record = 0
    end_record = 0

    if total_records > 0:
        start_record = (
                               (page - 1) * PAGE_SIZE
                       ) + 1

        end_record = min(
            page * PAGE_SIZE,
            total_records
        )

    page_numbers = range(
        max(1, page - 2),
        min(total_pages, page + 2) + 1
    )
    """
    Get all records that have already been added
    to the application database.
    """
    return {
        "details": details,
        "total_records": total_records,
        "total_pages": total_pages,
        "start_record": start_record,
        "end_record": end_record,
        "page_numbers": page_numbers,
        "page": page,
        "search": search or "",
        "search2": search2 or ""
    }

def add_detail(visit_id):
    """
    Add one selected patient visit.
    """
    return insert_added_detail(visit_id)
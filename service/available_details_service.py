import math

from repository.available_details_repository import (
    get_available_details,
    get_available_details_count,
    get_remote_visit_for_display,
    get_full_remote_visit,
)

PAGE_SIZE = 50


def get_available_details_page(page=1, search=""):
    """
    Get one page of the current census.

    Supports server-side progressive search.
    """

    if page < 1:
        page = 1

    search = (search or "").strip()

    # Get total count first so the requested page can be
    # corrected before fetching the actual records.
    total_records = get_available_details_count(
        search=search
    )

    total_pages = (
        math.ceil(total_records / PAGE_SIZE)
        if total_records
        else 0
    )

    # Keep the requested page within the valid range.
    if total_pages and page > total_pages:
        page = total_pages

    details = get_available_details(
        page=page,
        search=search,
    )

    start_record = 0
    end_record = 0

    if details:
        start_record = ((page - 1) * PAGE_SIZE) + 1
        end_record = min(
            page * PAGE_SIZE,
            total_records,
        )

    page_numbers = []

    if total_pages:
        page_numbers = list(
            range(
                max(1, page - 2),
                min(total_pages, page + 2) + 1,
            )
        )

    return {
        "details": details,
        "total_records": total_records,
        "total_pages": total_pages,
        "start_record": start_record,
        "end_record": end_record,
        "page_numbers": page_numbers,
        "page": page,
        "search": search,
    }


def get_available_visit(visit_id):
    """
    Get a single visit for displaying the search result.
    """

    rows = get_remote_visit_for_display(visit_id)

    if not rows:
        return None

    return rows[0]


def get_full_visit(visit_id):
    """
    Get the complete remote visit record.
    """

    return get_full_remote_visit(visit_id)
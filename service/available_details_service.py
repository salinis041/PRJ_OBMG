import math

from repository.available_details_repository import (
    get_available_details,
    get_available_details_count
)


PAGE_SIZE = 50


def get_available_details_page(
    page=1,
    search=None
):

    if page < 1:
        page = 1

    details = get_available_details(
        page=page,
        search=search
    )

    total_records = get_available_details_count(
        search=search
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

    return {
        "details": details,
        "total_records": total_records,
        "total_pages": total_pages,
        "start_record": start_record,
        "end_record": end_record,
        "page_numbers": page_numbers,
        "page": page,
        "search": search or ""
    }
from database.connection import get_connection
from flask import (request)
from datetime import datetime
PAGE_SIZE = 25
def get_EnTaskList(page=1, search=None,
        search2=None):
    from_date = request.args.get('from_date', '')
    to_date = request.args.get('to_date', '')

    search = request.args.get('search', '')
    facility = request.args.getlist('facility')
    status = request.args.getlist('TKstatus')
    assign = request.args.get('assign', '')

    offset = (page - 1) * PAGE_SIZE

    connection = get_connection()
    cursor = connection.cursor()

    conditions = []
    parameters = []

    try:
        # Date filter
        if from_date and to_date:
            from_date = datetime.strptime(
                from_date, '%Y-%m-%d'
            ).date()

            to_date = datetime.strptime(
                to_date, '%Y-%m-%d'
            ).date()

            conditions.append("""
                   TRY_CONVERT(DATE, Due_date, 110) >= ?
                   AND TRY_CONVERT(DATE, Due_date, 110) <= ?
               """)
            parameters.extend([from_date, to_date])

        # Patient name search
        if search:
            conditions.append("""
                   CONCAT(ISNULL(v.LastName, ''), ' ',
                          ISNULL(v.FirstName, '')) LIKE ?
               """)
            parameters.append('%' + search + '%')

        # Status filter
        if status:
            placeholders = ','.join('?' for _ in status)
            conditions.append(
                f"Task_status IN ({placeholders})"
            )
            parameters.extend(status)

        # Assign To filter
        if assign:
            conditions.append("EncoutTask.Assigto = ?")
            parameters.append(int(assign))

        # Build WHERE clause
        search_condition = ""

        if conditions:
            search_condition = " WHERE " + " AND ".join(conditions)

        query = f"""
               SELECT
                   TId,
                   Acct,
                   Mrn,
                   v.LastName + ' ' + v.FirstName AS Patname,
                   ISNULL(Task, '') AS Task,
                   ISNULL(Tags, '') AS Tags,
                   ISNULL(Task_status, '') AS Task_status,
                   ISNULL(Task_method, '') AS Task_method,
                   ISNULL(Dispos, '') AS Dispos,
                   ISNULL(FORMAT(
                       TRY_CONVERT(DATE, Due_date, 110),
                       'MM-dd-yyyy'
                   ), '') AS Due_date,
                   ISNULL(Due_time, '') AS Due_time,
                   ISNULL(u1.Lname, '') + ' ' +
                       ISNULL(u1.Fname, '') AS Assigto,
                   ISNULL(u2.Lname, '') + ' ' +
                       ISNULL(u2.Fname, '') AS Assigby,
                   ISNULL(v.Facility,'') AS Facility

               FROM EncoutTask
               LEFT JOIN Umaster u1
                   ON u1.Uid = EncoutTask.Assigto
               LEFT JOIN Umaster u2
                   ON u2.Uid = EncoutTask.Assigby
               LEFT JOIN Visits v
                   ON v.AccountNumber = EncoutTask.Acct

               {search_condition}

               ORDER BY TId DESC
               OFFSET ? ROWS
               FETCH NEXT ? ROWS ONLY
           """

        # Pagination parameters must come last
        parameters.extend([offset, PAGE_SIZE])

        # print("SQL markers:", query.count('?'))
        # print("Parameters:", parameters)
        # print("Parameter count:", len(parameters))

        cursor.execute(query, parameters)

        columns = [column[0] for column in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    finally:
        connection.close()


def get_available_details_count(search=None,
        search2=None):
    from_date = request.args.get('from_date', '')
    to_date = request.args.get('to_date', '')

    search = request.args.get('search', '')
    facility = request.args.getlist('facility')
    status = request.args.getlist('TKstatus')
    assign = request.args.get('assign', '')

    connection = get_connection()
    cursor = connection.cursor()

    conditions = []
    parameters = []

    try:
        # Date filter
        if from_date and to_date:
            from_date = datetime.strptime(
                from_date, '%Y-%m-%d'
            ).date()

            to_date = datetime.strptime(
                to_date, '%Y-%m-%d'
            ).date()

            conditions.append("""
                       TRY_CONVERT(DATE, Due_date, 110) >= ?
                       AND TRY_CONVERT(DATE, Due_date, 110) <= ?
                   """)
            parameters.extend([from_date, to_date])

        # Patient name search
        if search:
            conditions.append("""
                       CONCAT(ISNULL(v.LastName, ''), ' ',
                              ISNULL(v.FirstName, '')) LIKE ?
                   """)
            parameters.append('%' + search + '%')

        # Status filter
        if status:
            placeholders = ','.join('?' for _ in status)
            conditions.append(
                f"Task_status IN ({placeholders})"
            )
            parameters.extend(status)
            # facility filter
        if facility:
            placeholders = ','.join('?' for _ in facility)
            conditions.append(
                f"v.Facility IN ({placeholders})"
            )
            parameters.extend(facility)

        # Assign To filter
        if assign:
            conditions.append("EncoutTask.Assigto = ?")
            parameters.append(int(assign))

        # Build WHERE clause
        search_condition = ""

        if conditions:
            search_condition = " WHERE " + " AND ".join(conditions)

        query = f"""
            SELECT COUNT(*)

            FROM EncoutTask left join Umaster u1 on u1.Uid=EncoutTask.Assigto
                left join Umaster u2 on u2.Uid=EncoutTask.Assigby left join Visits v on v.AccountNumber=EncoutTask.Acct

            {search_condition}
        """

        cursor.execute(
            query,
            parameters
        )

        return cursor.fetchone()[0]

    finally:

        connection.close()
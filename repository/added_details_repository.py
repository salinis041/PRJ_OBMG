from database.connection import get_connection


def add_detail(detail):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        check_query = """
            SELECT COUNT(*)
            FROM AddedPatientDetails
            WHERE VisitID = ?
        """

        cursor.execute(
            check_query,
            detail["Visit ID"]
        )

        already_exists = cursor.fetchone()[0]

        if already_exists > 0:
            return False

        insert_query = """
            INSERT INTO AddedPatientDetails
            (
                VisitID,
                AccountNumber,
                MedicalRecordNumber,
                PatientFirstName,
                PatientMiddleName,
                PatientLastName,
                PatientDOB,
                PatientGender,
                Facility,
                AttendingPhysician,
                AdmitDate,
                DischargeDate,
                PatientType,
                AdmitFC,
                AdmitFCName,
                CurrentFC,
                CurrentFCName,
                Address1,
                Address2,
                City,
                State,
                Zip,
                Race,
                Language
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?
            )
        """

        cursor.execute(
            insert_query,

            detail.get("Visit ID"),

            detail.get("Account Number"),

            detail.get("Med Rec Nbr"),

            detail.get("Pat First Nm"),

            detail.get("Pat Middle Nm"),

            detail.get("Pat Last Nm"),

            detail.get("Pat DOB"),

            detail.get("Pat Gender"),

            detail.get("Facility"),

            detail.get("Phys Name Attending"),

            detail.get("Admit Date"),

            detail.get("Discharge Date"),

            detail.get("Patient Type"),

            detail.get("Admit FC"),

            detail.get("Admit FC Name"),

            detail.get("Curr FC"),

            detail.get("Curr FC Nm"),

            detail.get("Pat Addr 1"),

            detail.get("Pat Addr 2"),

            detail.get("Pat City"),

            detail.get("Pat State"),

            detail.get("Pat Zip"),

            detail.get("Race"),

            detail.get("Language")
        )

        connection.commit()

        return True

    finally:

        connection.close()


def get_added_details():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        query = """
            SELECT
                ID,
                VisitID,
                AccountNumber,
                MedicalRecordNumber,
                PatientFirstName,
                PatientMiddleName,
                PatientLastName,
                PatientDOB,
                PatientGender,
                Facility,
                AttendingPhysician,
                AdmitDate,
                DischargeDate,
                PatientType,
                AdmitFC,
                AdmitFCName,
                CurrentFC,
                CurrentFCName,
                Address1,
                Address2,
                City,
                State,
                Zip,
                Race,
                Language,
                CreatedDate
            FROM AddedPatientDetails
            ORDER BY CreatedDate DESC
        """

        cursor.execute(query)

        columns = [
            column[0]
            for column in cursor.description
        ]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    finally:

        connection.close()

def insert_added_detail(visit_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Prevent duplicate VisitID
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM AddedPatientDetails
            WHERE VisitID = ?
            """,
            visit_id
        )

        exists = cursor.fetchone()[0]

        if exists > 0:
            return "This patient has already been added."

        # Get the selected patient from the application/source data
        # This part should be connected to your remote database query.
        #
        # We will complete the remote lookup using your actual
        # available-details query in the next step.

        return "Patient selected successfully."

    finally:
        connection.close()
PAGE_SIZE = 50
def get_added_Visitdetails(page=1, search=None,
        search2=None):

    offset = (page - 1) * PAGE_SIZE
    connection = get_connection()

    try:

        cursor = connection.cursor()
        search_condition = ""
        parameters = []

        if search:
            search_condition = """
                        WHERE (
                            AccountNumber LIKE ?
                            OR MedicalRecordNumber LIKE ?
                            OR FirstName LIKE ?
                            OR LastName LIKE ?
                        )
                    """

            search_value = f"%{search}%"

            parameters.extend([
                search_value,
                search_value,
                search_value,
                search_value
            ])
            # ---------------------------------------
            # SECOND SEARCH
            # Account Number only
            # ---------------------------------------

        elif search2:

            search_condition = """
                     WHERE  CAST(AccountNumber AS VARCHAR(50)) = ?
                   """

            parameters.append(
                search2.strip()
            )

        query = f"""
            SELECT
                
                AccountNumber,
                MedicalRecordNumber,
                LastName + ' ' + FirstName AS Patname,

                CONVERT(varchar(10), BirthDate, 101) AS BirthDate,
               [Patient Type] as PatientType,
             FORMAT(
    TRY_CONVERT(datetime2, AdmitDateTime, 121),
    'MM/dd/yyyy hh:mm:ss tt'
) AS AdmitDateTime,
                 [Phys Name Attending ] as AttendingPhysician
                
            FROM Visits  
            {search_condition}

            ORDER BY
                AdmitDateTime DESC,
                AccountNumber DESC

            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
            
        """
        parameters.extend([
            offset,
            PAGE_SIZE
        ])

        cursor.execute(query,
            parameters)

        columns = [
            column[0]
            for column in cursor.description
        ]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    finally:

        connection.close()

def get_available_details_count(search=None,
        search2=None):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        search_condition = ""
        parameters = []

        if search:

            search_condition = """
                WHERE (
                    AccountNumber LIKE ?
                    OR MedicalRecordNumber LIKE ?
                    OR FirstName LIKE ?
                    OR LastName LIKE ?
                )
            """

            search_value = f"%{search}%"

            parameters.extend([
                search_value,
                search_value,
                search_value,
                search_value
            ])
        elif search2:

            search_condition = """
                      WHERE  CAST(AccountNumber AS VARCHAR(50)) = ?
                    """

            parameters.append(
                search2.strip()
            )

        query = f"""
            SELECT COUNT(*)

            FROM Visits

            {search_condition}
        """

        cursor.execute(
            query,
            parameters
        )

        return cursor.fetchone()[0]

    finally:

        connection.close()




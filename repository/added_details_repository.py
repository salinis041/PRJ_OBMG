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
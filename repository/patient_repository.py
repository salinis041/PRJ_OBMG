from database.connection import get_connection
import pyodbc


def get_patients():
    query = """
        SELECT
            PatID,
            LastName,
            FirstName,
            MiddleName,
            BirthDate,
            MedicalRecordNumber,
            AccountNumber,
            PatientType,
            ServicingFacility,
            AdmitDateTime,
            DischargeDateTimeDisplay,
            PCP,
            PAYOR
        FROM PatientVisits
        ORDER BY AdmitDateTime DESC
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]

        patients = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return patients

    except pyodbc.Error as e:
        print(f"Database error while fetching patients: {e}")
        raise

    except Exception as e:
        print(f"Unexpected error while fetching patients: {e}")
        raise

    finally:
        if connection:
            connection.close()
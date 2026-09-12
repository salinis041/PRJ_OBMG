from database.connection import get_connection


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

    finally:
        connection.close()


def get_coorpathome():
    query = """
        SELECT
            PatID,
            LastName+' '+FirstName as Patname,
            convert(varchar(10),BirthDate,101) as BirthDate,
            convert(varchar(3),DATEDIFF(month, BirthDate, GETDATE()) / 12) AS Age ,
            case when Gender='M' then 'Male' when Gender='F' then 'Female' else 'Other' end as Gender,
            MedicalRecordNumber,
            AccountNumber


        FROM PatientVisits
        ORDER BY AdmitDateTime DESC
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]

        patcordinate = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return patcordinate

    finally:
        connection.close()

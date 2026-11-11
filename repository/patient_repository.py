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


def get_patientVisit(visit_id):
    query = """
            SELECT
                PatID,

                LastName + ' ' + FirstName AS Patname,

                CONVERT(varchar(10), BirthDate, 101) AS BirthDate,

                CONVERT(
                    varchar(3),
                    DATEDIFF(month, BirthDate, GETDATE()) / 12
                ) AS Age,

                CASE
                    WHEN Gender = 'M' THEN 'Male'
                    WHEN Gender = 'F' THEN 'Female'
                    ELSE 'Other'
                END AS Gender,

                MedicalRecordNumber,
                AccountNumber,

                 ISNULL(Address1,'') Address1,
                 ISNULL(Address2,'') Address2,
                 ISNULL(City,'') City,
                 ISNULL(State,'') State,
                 ISNULL(Zip,'') Zip,
                 ISNULL(Country,'') Country,

                ISNULL([Pat Home Ph],'') HomePhone,
                ISNULL([Pat Work Ph],'') WorkPhone,
                CASE
                WHEN Langu = 'en' THEN 'ENGLISH'
                WHEN Langu = 'spa' THEN 'SPANISH'
                ELSE Langu
            END AS PrimaryLang,
                MaritalStatus,
                Race,
               ISNULL([Patient Type],'')  PatientType,
                '' AdmitReason,
                 '' ServicingFacility,
               ISNULL([Admit FC Name],'') PAYOR,
               '' Room

                --HospitalService,
                -- Location,
                -- AdmitDateTime,
                -- AdmitDateTimeDisplay,
                -- DischargeDateTimeDisplay,
                -- AdmitSource,
                -- FinancialClass,
                -- PCP,
                -- AttendingPhysicianID,
                -- AttendingPhysicianFirstName,
                -- AttendingPhysicianLastName,
                -- ReferringPhysicianID,
                -- ReferringPhysicianFirstName,
                -- ReferringPhysicianLastName,
                -- ConsultingPhysicianID,
                -- ConsultingPhysicianFirstName,
                -- ConsultingPhysicianLastName

            FROM Visits

            WHERE AccountNumber = ?
        """
    # query = """
    #     SELECT
    #         PatID,
    #
    #         LastName + ' ' + FirstName AS Patname,
    #
    #         CONVERT(varchar(10), BirthDate, 101) AS BirthDate,
    #
    #         CONVERT(
    #             varchar(3),
    #             DATEDIFF(month, BirthDate, GETDATE()) / 12
    #         ) AS Age,
    #
    #         CASE
    #             WHEN Gender = 'M' THEN 'Male'
    #             WHEN Gender = 'F' THEN 'Female'
    #             ELSE 'Other'
    #         END AS Gender,
    #
    #         MedicalRecordNumber,
    #         AccountNumber,
    #
    #         NamePrefix,
    #         NameSuffix,
    #         MiddleName,
    #
    #         Address1,
    #         Address2,
    #         City,
    #         State,
    #         Zip,
    #         Country,
    #
    #         HomePhone,
    #         WorkPhone,
    #         PrimaryLang,
    #
    #         Alias,
    #         MothersName,
    #         MaritalStatus,
    #         Race,
    #         Religion,
    #
    #         PatientType,
    #         HospitalService,
    #         Location,
    #
    #         ServicingFacility,
    #         Room,
    #
    #         AdmitDateTime,
    #         AdmitDateTimeDisplay,
    #         DischargeDateTimeDisplay,
    #
    #         AdmitReason,
    #         AdmitSource,
    #
    #         FinancialClass,
    #         PCP,
    #         PAYOR,
    #
    #         AttendingPhysicianID,
    #         AttendingPhysicianFirstName,
    #         AttendingPhysicianLastName,
    #
    #         ReferringPhysicianID,
    #         ReferringPhysicianFirstName,
    #         ReferringPhysicianLastName,
    #
    #         ConsultingPhysicianID,
    #         ConsultingPhysicianFirstName,
    #         ConsultingPhysicianLastName
    #
    #     FROM PatientVisits
    #
    #     WHERE AccountNumber = ?
    # """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(query, visit_id)

        columns = [
            column[0]
            for column in cursor.description
        ]

        patcordinate = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return patcordinate

    finally:
        connection.close()


def get_patVisitDetails(visit_id):
    """
    Load the demographics view from the local dbo.Visits record.
    AccountNumber is the external visit/account number used by the portal.
    """
    query = """
        SELECT TOP 1
            PatID,
            LTRIM(RTRIM(CONCAT(
                ISNULL(FirstName, ''), ' ',
                ISNULL(MiddleName, ''), ' ',
                ISNULL(LastName, '')
            ))) AS Patname,
            FirstName AS FirstName,
            MiddleName AS MiddleName,
            LastName AS LastName,
            [Pat Name Suf] AS NameSuffix,
            CONVERT(varchar(10), TRY_CONVERT(date, BirthDate), 101) AS BirthDate,
            CASE
                WHEN BirthDate IS NULL THEN ''
                ELSE CONVERT(varchar(3), DATEDIFF(year, BirthDate, GETDATE())
                     - CASE WHEN DATEADD(year, DATEDIFF(year, BirthDate, GETDATE()), BirthDate) > GETDATE()
                            THEN 1 ELSE 0 END)
            END AS Age,
            CASE WHEN Gender = 'M' THEN 'Male'
                 WHEN Gender = 'F' THEN 'Female'
                 ELSE ISNULL(Gender, 'Other') END AS Gender,
            MedicalRecordNumber,
            AccountNumber,
            ISNULL(Address1, '') AS Address1,
            ISNULL(Address2, '') AS Address2,
            ISNULL(City, '') AS City,
            ISNULL(State, '') AS State,
            ISNULL(Zip, '') AS Zip,
            ISNULL(Country, '') AS Country,
            ISNULL([Pat Home Ph], '') AS HomePhone,
            ISNULL([Pat Work Ph], '') AS WorkPhone,
            ISNULL([Pat Cell Ph], '') AS CellPhone,
            CASE WHEN Langu = 'en' THEN 'ENGLISH'
                 WHEN Langu = 'spa' THEN 'SPANISH'
                 ELSE ISNULL(Langu, '') END AS PrimaryLang,
            ISNULL(MaritalStatus, '') AS MaritalStatus,
            ISNULL(Race, '') AS Race,
            ISNULL([Patient Type], '') AS PatientType,
            CASE WHEN [Patient Type] LIKE 'JS%' THEN 'Jacksonstreet'
                 WHEN [Patient Type] LIKE 'WW%' THEN 'WilliamWay'
                 WHEN [Patient Type] LIKE 'WH%' THEN 'Wharton'
                 ELSE '' END AS ServicingFacility,
            TRY_CONVERT(datetime2, AdmitDateTime) AS AdmitDateTime,
            CONVERT(varchar(10), TRY_CONVERT(date, AdmitDateTime), 101) AS AdmitDateTimeDisplay,
            CONVERT(varchar(10), TRY_CONVERT(date, [Discharge Date]), 101) AS DischargeDateTimeDisplay,
            ISNULL(AdmitSource, '') AS AdmitSource,
            ISNULL([Admit FC], '') AS FinancialClass,
            ISNULL([Admit FC Name], '') AS AdmitFCName,
            ISNULL([Curr FC Nm], '') AS PAYOR,
            ISNULL([primary I-Plan description], '') AS PrimaryInsurance,
            ISNULL([secondary I-Plan description], '') AS SecondaryInsurance,
            ISNULL(Insurance1PolicyID, '') AS MemberID,
            ISNULL([Phys ID], '') AS AttendingPhysicianID,
            ISNULL([Phys Name Attending ], '') AS AttendingPhysicianName,
            ISNULL([Phys NPI], '') AS AttendingPhysicianNPI,
            ISNULL(Guar, '') AS Guar,
            ISNULL([Guar Relation], '') AS gurrelat,
            ISNULL([Guar Home Ph], '') AS GurHomeph,
            ISNULL([Guar Addr 1], '') AS GurAdd1,
            ISNULL([Guar Addr 2], '') AS GurAdd2,
            ISNULL([Guar City], '') AS GurCity,
            ISNULL([Guar State], '') AS GurState,
            ISNULL([Guar Zipcode], '') AS GurZip
        FROM dbo.Visits
        WHERE AccountNumber = ?
        ORDER BY AdmitDateTime DESC
    """
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query, visit_id)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        connection.close()

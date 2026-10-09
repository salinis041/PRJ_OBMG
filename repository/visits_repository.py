from database.connection import get_connection


def visit_exists(account_number):
    """
    Check whether the external Account Number already exists
    in dbo.Visits.AccountNumber.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM dbo.Visits
            WHERE AccountNumber = ?
            """,
            account_number
        )

        count = cursor.fetchone()[0]

        return count > 0

    finally:
        connection.close()


def _visit_values(data):
    """
    Convert the full remote visit dictionary into the values
    required by dbo.Visits.

    IMPORTANT:
    dbo.Visits.AccountNumber stores the external Account Number
    from remote vst_ext_id.

    Remote Visit ID (vst_int_id) is NOT stored in
    dbo.Visits.AccountNumber.
    """

    return (
        data.get("Account Number"),
        data.get("Med Rec Nbr"),
        data.get("Phys Name Attending"),
        data.get("Phys NPI"),
        data.get("Phys ID"),
        data.get("Admit Date"),
        data.get("Discharge Date"),
        data.get("Patient Type"),
        data.get("Admit FC"),
        data.get("Admit FC Name"),
        data.get("Curr FC"),
        data.get("Curr FC Nm"),
        data.get("Pat Last Nm"),
        data.get("Pat Middle Nm"),
        data.get("Pat First Nm"),
        data.get("Pat Name Suf"),
        data.get("Pat DOB"),
        data.get("Pat Gender"),
        data.get("Pat SSN"),
        data.get("Pat Addr 1"),
        data.get("Pat Addr 2"),
        data.get("Pat City"),
        data.get("Pat State"),
        data.get("Pat Zip"),
        data.get("Pat Country"),
        data.get("Pat Province"),
        data.get("Pat Home Ph"),
        data.get("Pat Work Ph"),
        data.get("Pat Cell Ph"),
        data.get("Pat Empl Nm"),
        data.get("Guar Relation"),
        data.get("Guar"),
        data.get("Guar First Nm"),
        data.get("Guar Middle Nm"),
        data.get("Guar Last Nm"),
        data.get("Guar Name Suf"),
        data.get("Guar DOB"),
        data.get("Guar SSN"),
        data.get("Guar Gender"),
        data.get("Guar Addr 1"),
        data.get("Guar Addr 2"),
        data.get("Guar City"),
        data.get("Guar State"),
        data.get("Guar Zipcode"),
        data.get("Guar Country"),
        data.get("Guar Province"),
        data.get("Guar Home Ph"),
        data.get("Guar Work Ph"),
        data.get("Guar Cell Ph"),
        data.get("Guar Empl"),
        data.get("LOSHours"),
        data.get("DRG Weight"),
        data.get("AdmitSource"),
        data.get("DischStat"),
        data.get("primary I-Plan description"),
        data.get("secondary I-Plan description"),
        data.get("Race"),
        data.get("Language"),
        data.get("Insurance1PolicyID"),
    )


def insert_visit(data):
    """
    Insert a complete visit into dbo.Visits.

    AccountNumber:
        External Account Number / remote vst_ext_id

    Audit fields:
        CreatedBy = 1
        CreatedDate = GETDATE()
        ModifiedBy = 1
        ModifiedDate = GETDATE()
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        account_number = data.get("Account Number")

        if not account_number:
            raise ValueError(
                "Account Number is required."
            )

        # ----------------------------------------------------
        # Protect against duplicate Account Numbers.
        # ----------------------------------------------------

        cursor.execute(
            "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
        )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM dbo.Visits WITH (UPDLOCK, HOLDLOCK)
            WHERE AccountNumber = ?
            """,
            account_number
        )

        if cursor.fetchone()[0] > 0:
            connection.rollback()
            return False

        # ----------------------------------------------------
        # Get the 59 visit values.
        # ----------------------------------------------------

        values = _visit_values(data)

        if len(values) != 59:
            raise ValueError(
                f"Expected 59 visit values, got {len(values)}."
            )

        # ----------------------------------------------------
        # Generate exactly 59 parameter markers.
        # This avoids manual counting errors.
        # ----------------------------------------------------

        placeholders = ", ".join(
            ["?"] * len(values)
        )

        sql = f"""
            INSERT INTO dbo.Visits (
                AccountNumber,
                MedicalRecordNumber,
                [Phys Name Attending ],
                [Phys NPI],
                [Phys ID],
                AdmitDateTime,
                [Discharge Date],
                [Patient Type],
                [Admit FC],
                [Admit FC Name],
                [Curr FC],
                [Curr FC Nm],
                LastName,
                MiddleName,
                FirstName,
                [Pat Name Suf],
                BirthDate,
                Gender,
                SSN,
                Address1,
                Address2,
                City,
                State,
                Zip,
                Country,
                [Pat Province],
                [Pat Home Ph],
                [Pat Work Ph],
                [Pat Cell Ph],
                [Pat Empl Nm],
                [Guar Relation],
                Guar,
                [Guar First Nm],
                [Guar Middle Nm],
                [Guar Last Nm],
                [Guar Name Suf],
                [Guar DOB],
                [Guar SSN],
                [Guar Gender],
                [Guar Addr 1],
                [Guar Addr 2],
                [Guar City],
                [Guar State],
                [Guar Zipcode],
                [Guar Country],
                [Guar Province],
                [Guar Home Ph],
                [Guar Work Ph],
                [Guar Cell Ph],
                [Guar Empl],
                LOSHours,
                [DRG Weight],
                AdmitSource,
                DischStat,
                [primary I-Plan description],
                [secondary I-Plan description],
                Race,
                Langu,
                Insurance1PolicyID,
                CreatedBy,
                CreatedDate,
                ModifiedBy,
                ModifiedDate
            )
            VALUES (
                {placeholders},
                1,
                GETDATE(),
                1,
                GETDATE()
            )
        """

        cursor.execute(
            sql,
            values
        )

        connection.commit()

        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def update_visit(data):
    """
    Update an existing visit in dbo.Visits.

    AccountNumber:
        External Account Number / remote vst_ext_id

    The Account Number is used in the WHERE clause.

    Audit fields:
        ModifiedBy = 1
        ModifiedDate = GETDATE()
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        values = _visit_values(data)

        cursor.execute(
            """
            UPDATE dbo.Visits
            SET
                MedicalRecordNumber = ?,
                [Phys Name Attending ] = ?,
                [Phys NPI] = ?,
                [Phys ID] = ?,
                AdmitDateTime = ?,
                [Discharge Date] = ?,
                [Patient Type] = ?,
                [Admit FC] = ?,
                [Admit FC Name] = ?,
                [Curr FC] = ?,
                [Curr FC Nm] = ?,
                LastName = ?,
                MiddleName = ?,
                FirstName = ?,
                [Pat Name Suf] = ?,
                BirthDate = ?,
                Gender = ?,
                SSN = ?,
                Address1 = ?,
                Address2 = ?,
                City = ?,
                State = ?,
                Zip = ?,
                Country = ?,
                [Pat Province] = ?,
                [Pat Home Ph] = ?,
                [Pat Work Ph] = ?,
                [Pat Cell Ph] = ?,
                [Pat Empl Nm] = ?,
                [Guar Relation] = ?,
                Guar = ?,
                [Guar First Nm] = ?,
                [Guar Middle Nm] = ?,
                [Guar Last Nm] = ?,
                [Guar Name Suf] = ?,
                [Guar DOB] = ?,
                [Guar SSN] = ?,
                [Guar Gender] = ?,
                [Guar Addr 1] = ?,
                [Guar Addr 2] = ?,
                [Guar City] = ?,
                [Guar State] = ?,
                [Guar Zipcode] = ?,
                [Guar Country] = ?,
                [Guar Province] = ?,
                [Guar Home Ph] = ?,
                [Guar Work Ph] = ?,
                [Guar Cell Ph] = ?,
                [Guar Empl] = ?,
                LOSHours = ?,
                [DRG Weight] = ?,
                AdmitSource = ?,
                DischStat = ?,
                [primary I-Plan description] = ?,
                [secondary I-Plan description] = ?,
                Race = ?,
                Langu = ?,
                Insurance1PolicyID = ?,
                ModifiedBy = 1,
                ModifiedDate = GETDATE()
            WHERE AccountNumber = ?
            """,
            values[1:] + (values[0],)
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
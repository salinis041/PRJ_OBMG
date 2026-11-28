from database.connection import get_connection
def Add_CareTeam(uid,mrn,vist,task):
    connection = get_connection()
    cursor = connection.cursor()
    tsk = ''
    try:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM dbo.CareTeam WITH (UPDLOCK, HOLDLOCK)
            WHERE Mrn = ? AND Uid = ? AND IsActive='Y'
            """,
            mrn,
            uid
        )

        count = cursor.fetchone()[0]
        if count == 0:
            insert_sql = """
                                      INSERT INTO dbo.CareTeam
                                      (
                                          Uid,Acct, Mrn,  
                                          LstAct_Dt, CreateBy, CreateDt
                                      )
                                      VALUES (?, ?, ?,GETDATE() , 1, GETDATE())
                                                """

            cursor.execute(
                insert_sql,
                uid,
                vist,
                mrn,
            )
        else:

            update_sql = """
                               UPDATE dbo.CareTeam
                               SET
                                   LstAct_Dt = GETDATE(),
                                   ModifyBy = 1,
                                   ModifyDt = GETDATE()
                               WHERE Mrn = ? AND Uid = ? 
                           """

            cursor.execute(
                update_sql,
                mrn,
                uid)


        connection.commit()

    except Exception:
        connection.rollback()
        # traceback.print_exc()
        raise

    finally:
        cursor.close()
        connection.close()
def get_CareTeam(visit):

    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = f"""
                       SELECT
                           CTId,
                           u1.Lname  + ' ' + u1.Fname  AS CareName,
                           ISNULL(FORMAT(
                               TRY_CONVERT(DATE, LstAct_Dt , 110),
                               'MM-dd-yyyy'
                           ), '') AS LstAct_Dt ,
                           case when u1.Utype='Provider' then u2.Spety else u1.Utype end as SPECIALTY,
                            u1.Hphone  as OffPhone
                           

                       FROM CareTeam
                       LEFT JOIN Umaster u1
                           ON u1.Uid = CareTeam.Uid
                       LEFT JOIN PractInfo u2
                           ON u2.Uid  = u1.Uid
                           
                       WHERE Mrn in(select distinct MedicalRecordNumber from Visits v where  v.AccountNumber = ?) AND CareTeam.IsActive='Y'

                       ORDER BY CTId DESC
                   """

        cursor.execute(query, visit)

        columns = [column[0] for column in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    finally:
        connection.close()



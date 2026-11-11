from database.connection import get_connection
from datetime import datetime


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
            MiddleName,

            Address1,
            Address2,
            City,
            State,
            Zip,
            Country,

            [Pat Home Ph] as HomePhone,
            [Pat Work Ph] as WorkPhone,
            CASE
                WHEN Langu = 'en' THEN 'ENGLISH'
                WHEN Langu = 'spa' THEN 'SPANISH'
                ELSE Langu
            END AS PrimaryLang,

            MaritalStatus,
            Race,

            [Patient Type] as PatientType,
            

           FORMAT(
    TRY_CONVERT(datetime2, AdmitDateTime, 121),
    'MM/dd/yyyy hh:mm:ss tt'
) AS AdmitDateTime,
            [Discharge Date] as DischargeDateTimeDisplay,

            
            [Curr FC Nm] as PAYOR,

            [Phys ID] as AttendingPhysicianID,
            [Phys Name Attending ] as AttendingPhysicianFirstName,
            [Phys NPI] as AttendingPhysicianLastName,
            Guar,
            [Guar Relation] as gurrelat,
            [Guar Home Ph] as GurHomeph,
            [Guar Addr 1] as GurAdd1

            

        FROM Visits

        WHERE AccountNumber = ?
    """

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
def get_EncTask_list(mrn,vist):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM dbo.EncoutTask WITH (UPDLOCK, HOLDLOCK)
        WHERE Acct = ?
        """,
        vist
    )

    if cursor.fetchone()[0] == 0:
        sql = """
                INSERT INTO dbo.EncoutTask
    (
        Acct, Mrn, [Task], Tags, [Task_status], [CreateBy], CreateDt
    )
    VALUES
        (?, ?, 'Registration Issue', NULL, 'Pending', 1, GETDATE()),
        (?, ?, 'High Risk', 'High Risk', 'Pending', 1, GETDATE()),
        (?, ?, 'Contact Patient', 'Task|Contact', 'Pending', 1, GETDATE())
                """
        cursor.execute(
            sql,
            vist,mrn,vist,mrn,vist,mrn
        )

        connection.commit()
    try:
        query = """
                SELECT
                    TId,Acct, Mrn,
                    ISNULL(Task,'') Task,
                    ISNULL(Tags,'') Tags,
                    ISNULL(Task_status,'') Task_status ,ISNULL(Task_method,'') Task_method,
                    ISNULL(Dispos,'') Dispos


                FROM EncoutTask
                Where Acct = ? 
                ORDER BY
                        TId ASC
            """

        cursor.execute(query,vist)

        columns = [column[0] for column in cursor.description]

        patcordinate = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return patcordinate

    finally:
        connection.close()
def get_EncTask_count(vist):
    query = """
        SELECT
            COUNT(*) as Tcount


        FROM EncoutTask
        Where Acct = ?
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query, vist)

        columns = [column[0] for column in cursor.description]

        patcordinate = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return patcordinate

    finally:
        connection.close()
def get_EnTaskVIdList(vist):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = """
                SELECT
                    TId,Acct, Mrn,
                    ISNULL(Task,'') Task,
                    ISNULL(Tags,'') Tags,
                    ISNULL(Task_status,'') Task_status ,ISNULL(Task_method,'') Task_method,
                    ISNULL(Dispos,'') Dispos,ISNULL((FORMAT(Due_date, 'MM-dd-yyyy')),'') Due_date,ISNULL(Due_time,'') Due_time


                FROM EncoutTask
                Where Acct = ?
                ORDER BY
                        TId ASC
            """

        cursor.execute(query,vist)

        columns = [column[0] for column in cursor.description]

        patcordinate = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return patcordinate

    finally:
        connection.close()
def get_EnTaskList_TId(TId):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = """
                    SELECT
                        TId, Acct, Mrn,
                        ISNULL(Task,'') Task,
                        ISNULL(Tags,'') Tags,
                        ISNULL(Task_status,'') Task_status ,ISNULL(Task_method,'') Task_method,
                        ISNULL(Dispos,'') Dispos,ISNULL(Assigto,'') Assigto,ISNULL(Assigby,'') Assigby
                    ,ISNULL((FORMAT(Due_date, 'MM-dd-yyyy')),'') Due_date,ISNULL(Due_time,'') Due_time


                    FROM EncoutTask
                    Where TId = ? ORDER BY
                        TId ASC
                """

        cursor.execute(query, TId)

        columns = [column[0] for column in cursor.description]

        patcordinate = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return patcordinate

    finally:
        connection.close()
def add_comment(commentData,vst,mrn):
    connection = get_connection()
    cursor = connection.cursor()
    if commentData:

        sql2 = """
                                     INSERT INTO TaskCommnt
                                     (
                                         Acct ,
                                         Mrn ,
                                         Task_cmmnt,
                                         CreateBy,
                                         CreateDt
                                     )
                                     VALUES (?, ?, ?,  1, GETDATE())
                                 """

        for cmnt in commentData:
            cursor.execute(sql2, (
                vst,
                mrn,
                cmnt.get("cmntdt")


            ))
    connection.commit()
    cursor.close()
    connection.close()

def update_ETask(data,commentData):
    connection = get_connection()
    cursor = connection.cursor()
    tsk = ''
    try:
        if data.get("disposition") == "Unable to Assist":
            tsk = 'Unable to Assist Reason'
        elif data.get("disposition") == "Unable to Reach-No SMS":
            tsk = 'Unable to Reach'
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM dbo.EncoutTask WITH (UPDLOCK, HOLDLOCK)
            WHERE Acct = ? AND Task = ?
            """,
            data.get("vist"),
            tsk
        )

        count = cursor.fetchone()[0]

        if count == 0:

            insert_sql = """
                        INSERT INTO dbo.EncoutTask
                        (
                            Acct, Mrn, [Task],Task_method, 
                            [Task_status], CreateBy, CreateDt
                        )
                        VALUES (?, ?, ?, ?, ?, 1, GETDATE())
                    """

            cursor.execute(
                insert_sql,
                data.get("vist"),
                data.get("mrn"),
                tsk,
                "Other",
                data.get("Tstatus")
            )

        else:

            update_sql = """
                        UPDATE dbo.EncoutTask
                        SET
                            [Task_status] = ?,
                            Task_method = ?,
                            ModifyBy = 1,
                            ModifyDt = GETDATE()
                        WHERE Acct = ? AND Task = ?
                    """

            cursor.execute(
                update_sql,
                data.get("Tstatus"),
                data.get("method"),
                data.get("vist"),
                tsk
            )


        update_sql = """
               UPDATE dbo.EncoutTask
               SET
                   [Task_status] = ?,
                   Dispos = ?,
                   Assigto = ?,
                   Task_method = ?,
                   Due_date = ?,
                   Due_time = ?,
                   Assigby = 1,
                   ModifyBy = 1,
                   ModifyDt = GETDATE()
               WHERE TId = ?
           """

        cursor.execute(
            update_sql,
            data.get("Tstatus"),
            data.get("disposition"),
            data.get("assign"),
            data.get("method"),
            data.get("due_dt") or None,
            data.get("due_time") or None,
            data.get("TId")
        )
        if commentData:

            sql2 = """
                                         INSERT INTO TaskCommnt
                                         (
                                             Acct ,
                                             Mrn ,
                                             Task_cmmnt,
                                             CreateBy,
                                             CreateDt
                                         )
                                         VALUES (?, ?, ?,  1, GETDATE())
                                     """

            for cmnt in commentData:
                cursor.execute(sql2, (
                    data.get("vist"),
                    data.get("mrn"),
                    cmnt.get("cmntdt")

                ))
        connection.commit()

        query = """
               SELECT TId, Acct, Mrn, Task, Tags,
                      Task_status, Task_method, ISNULL(Dispos,'') Dispos,ISNULL((FORMAT(Due_date, 'MM-dd-yyyy')),'') Due_date,ISNULL(Due_time,'') Due_time
               FROM dbo.EncoutTask
               WHERE Acct = ? 
               ORDER BY
                        TId ASC
           """

        cursor.execute(query, data.get("vist"))

        columns = [column[0] for column in cursor.description]

        patcordinate = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return patcordinate

    except Exception:
        connection.rollback()
        # traceback.print_exc()
        raise

    finally:
        cursor.close()
        connection.close()
def Schedule_ETask(data,commentData):
    connection = get_connection()
    cursor = connection.cursor()
    current_time =''
    tsk = ''
    tgs=''
    try:
        if data.get("due_time") == '':
            current_time = datetime.now().strftime("%I:%M %p")
        else:
            current_time = data.get("due_time")
        if data.get("disposition") == "Scheduling Needed-PCP":
            tsk='Schedule Appointment-PCP'
            tgs='Task|Schedule PCP'
        elif data.get("disposition") == "Scheduling Needed-Specialist":
            tsk = 'Schedule Appointment-Specialist'
            tgs = 'Task|Schedule Specialist'
        elif data.get("disposition") == "Scheduling Needed-PCP & Specialist":
            tsk = 'Schedule Appointment-PCP & Specialist'
            tgs = 'Task|Schedule PCP & Specialist'
        elif data.get("disposition") == "Scheduling Needed-PCP & 2 Specialist":
            tsk = 'Schedule Appointment-PCP & 2 Specialist'
            tgs = 'Task|Schedule PCP & 2 Specialist'

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM dbo.EncoutTask WITH (UPDLOCK, HOLDLOCK)
            WHERE Acct = ? AND Task = ?
            """,
            data.get("vist"),
            tsk
        )

        count = cursor.fetchone()[0]

        if count == 0:



            insert_sql = """
               INSERT INTO dbo.EncoutTask
               (
                   Acct, Mrn, [Task], 
                   [Task_status],Tags,Assigto,
                  Due_date ,
                  Due_time, CreateBy, CreateDt
               )
               VALUES (?, ?, ?, 'Pending',?,?,?,?, 1, GETDATE()),
                      (?, ?, 'OakBend Medical Group SMS', 'Pending','',?,'','', 1, GETDATE())
           """

            cursor.execute(
                insert_sql,
                data.get("vist"),
                data.get("mrn"),
                tsk,
                tgs,
                data.get("assign"),
                data.get("due_dt") or None,
                current_time,
                data.get("vist"),
                data.get("mrn"),
                data.get("assign")
            )

        else:

            update_sql = """
                   UPDATE dbo.EncoutTask
                   SET
                       [Task_status] = ?,
                       Task_method = ?,
                       ModifyBy = 1,
                       ModifyDt = GETDATE()
                   WHERE Acct = ? AND Task = ?
               """

            cursor.execute(
                update_sql,
                data.get("Tstatus"),
                data.get("method"),
                data.get("vist"),
                tsk)

        update_sql = """
                          UPDATE dbo.EncoutTask
                          SET
                              [Task_status] = ?,
                              Dispos = ?,
                              Assigto = ?,
                              Task_method = ?,
                              Due_date = ?,
                              Due_time = ?,
                              Assigby = 1,
                              ModifyBy = 1,
                              ModifyDt = GETDATE()
                          WHERE TId = ?
                      """

        cursor.execute(
                update_sql,
                data.get("Tstatus"),
                data.get("disposition"),
                data.get("assign"),
                data.get("method"),
                data.get("due_dt") or None,
                data.get("due_time") or None,
                data.get("TId")
            )
        if commentData:

            sql2 = """
                                                INSERT INTO TaskCommnt
                                                (
                                                    Acct ,
                                                    Mrn ,
                                                    Task_cmmnt,
                                                    CreateBy,
                                                    CreateDt
                                                )
                                                VALUES (?, ?, ?,  1, GETDATE())
                                            """

            for cmnt in commentData:

                cursor.execute(sql2, (
                    data.get("vist"),
                    data.get("mrn"),
                    cmnt.get("cmntdt")

                ))
        connection.commit()

        query = """
                          SELECT TId, Acct, Mrn, Task, Tags,
                                 Task_status, Task_method, ISNULL(Dispos,'') Dispos,ISNULL((FORMAT(Due_date, 'MM-dd-yyyy')),'') Due_date,ISNULL(Due_time,'') Due_time
                          FROM dbo.EncoutTask
                          WHERE Acct = ? 
                          ORDER BY
                                   TId ASC
                      """

        cursor.execute(query, data.get("vist"))

        columns = [column[0] for column in cursor.description]

        patcordinate = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return patcordinate

    except Exception:
        connection.rollback()
        # traceback.print_exc()
        raise

    finally:
       cursor.close()
       connection.close()
def SchAppoimnt_ETask(data,commentData):
    connection = get_connection()
    cursor = connection.cursor()
    current_time = ''
    tsk = ''
    tskrm=''
    print(data.get("Tsk"))
    try:
        if data.get("due_time") == '':
            current_time = datetime.now().strftime("%I:%M %p")
        else:
            current_time = data.get("due_time")
        if (data.get("disposition") == "Appointment Scheduled"
                and data.get("Tsk") == "Schedule Appointment-PCP"):
            tsk='Confirm Appointment Attendance-PCP'
            tskrm = 'Appointment Reminder-PCP'
        elif (data.get("disposition") == "Appointment Scheduled"
              and data.get("Tsk") == "Schedule Appointment-Specialist") :
            tsk = 'Confirm Appointment Attendance-Specialist'
            tskrm = 'Appointment Reminder-Specialist'
        elif (data.get("disposition") == "Appointment Scheduled"
              and data.get("Tsk") == "Schedule Appointment-PCP & Specialist") :
            tsk = 'Confirm Appointment Attendance-PCP & Specialist'
            tskrm = 'Appointment Reminder-PCP & Specialist'
        elif (data.get("disposition") == "Appointment Scheduled"
              and data.get("Tsk") == "Schedule Appointment-PCP & 2 Specialist") :
            tsk = 'Confirm Appointment Attendance-PCP & 2 Specialist'
            tskrm = 'Appointment Reminder-PCP & 2 Specialist'

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM dbo.EncoutTask WITH (UPDLOCK, HOLDLOCK)
            WHERE Acct = ? AND Task = ?
            """,
            data.get("vist"),
            tsk
        )

        count = cursor.fetchone()[0]

        if count == 0:
            insert_sql = """
                           INSERT INTO dbo.EncoutTask
                           (
                               Acct, Mrn, [Task], 
                               [Task_status],Tags,Assigto,
                              Due_date ,
                              Due_time, CreateBy, CreateDt
                           )
                           VALUES (?, ?, ?, 'Pending','Task|Reminder',?,?,?, 1, GETDATE()),
                                  (?, ?, ?, 'Pending','Task|Confirm',?,?,?, 1, GETDATE())
                       """

            cursor.execute(
                insert_sql,
                data.get("vist"),
                data.get("mrn"),
                tskrm,
                data.get("assign"),
                data.get("due_dt") or None,
                current_time,
                data.get("vist"),
                data.get("mrn"),
                tsk,
                data.get("assign"),
               data.get("due_dt") or None,
               current_time,
            )

        else:

            update_sql = """
                               UPDATE dbo.EncoutTask
                               SET
                                   [Task_status] = ?,
                                   ModifyBy = 1,
                                   ModifyDt = GETDATE()
                               WHERE Acct = ? AND Task = ?
                           """

            cursor.execute(
                update_sql,
                data.get("Tstatus"),
                data.get("vist"),
                tsk)
        update_sql = """
                                  UPDATE dbo.EncoutTask
                                  SET
                                      [Task_status] = ?,
                                      Dispos = ?,
                                      Assigby = 1,
                                      ModifyBy = 1,
                                      ModifyDt = GETDATE()
                                  WHERE TId = ?
                              """

        cursor.execute(
            update_sql,
            data.get("Tstatus"),
            data.get("disposition"),
            data.get("TId")
        )
        if commentData:

            sql2 = """
                                                INSERT INTO TaskCommnt
                                                (
                                                    Acct ,
                                                    Mrn ,
                                                    Task_cmmnt,
                                                    CreateBy,
                                                    CreateDt
                                                )
                                                VALUES (?, ?, ?,  1, GETDATE())
                                            """

            for cmnt in commentData:
                cursor.execute(sql2, (
                    data.get("vist"),
                    data.get("mrn"),
                    cmnt.get("cmntdt")

                ))

        connection.commit()

        query = """
                                  SELECT TId, Acct, Mrn, Task, Tags,
                                         Task_status, Task_method, ISNULL(Dispos,'') Dispos,ISNULL((FORMAT(Due_date, 'MM-dd-yyyy')),'') Due_date,ISNULL(Due_time,'') Due_time
                                  FROM dbo.EncoutTask
                                  WHERE Acct = ? 
                                  ORDER BY
                                           TId ASC
                              """

        cursor.execute(query, data.get("vist"))

        columns = [column[0] for column in cursor.description]

        patcordinate = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return patcordinate

    except Exception:
        connection.rollback()
        # traceback.print_exc()
        raise

    finally:
        cursor.close()
        connection.close()
def ConfirmApoimnt_ETask(data,commentData):
    connection = get_connection()
    cursor = connection.cursor()
    current_time = ''
    tsk = ''
    try:
        update_sql = """
                                         UPDATE dbo.EncoutTask
                                         SET
                                             [Task_status] = 'Completed',
                                             Dispos = ?,
                                             Assigby = 1,
                                             ModifyBy = 1,
                                             ModifyDt = GETDATE()
                                         WHERE TId = ?
                                     """

        cursor.execute(
            update_sql,
            data.get("disposition"),
            data.get("TId")
        )
        if commentData:


            sql2 = """
                                                INSERT INTO TaskCommnt
                                                (
                                                    Acct ,
                                                    Mrn ,
                                                    Task_cmmnt,
                                                    CreateBy,
                                                    CreateDt
                                                )
                                                VALUES (?, ?, ?,  1, GETDATE())
                                            """

            for cmnt in commentData:
                cursor.execute(sql2, (
                    data.get("vist"),
                    data.get("mrn"),
                    cmnt.get("cmntdt")

                ))
        connection.commit()

        query = """
                                         SELECT TId, Acct, Mrn, Task, Tags,
                                                Task_status, Task_method , ISNULL(Dispos,'') Dispos,ISNULL((FORMAT(Due_date, 'MM-dd-yyyy')),'') Due_date,ISNULL(Due_time,'') Due_time
                                         FROM dbo.EncoutTask
                                         WHERE Acct = ? 
                                         ORDER BY
                                                  TId ASC
                                     """

        cursor.execute(query, data.get("vist"))

        columns = [column[0] for column in cursor.description]

        patcordinate = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return patcordinate

    except Exception:
        connection.rollback()
        # traceback.print_exc()
        raise

    finally:
        cursor.close()
        connection.close()
def get_Task_CmntList_Vistid(vist):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        sql = """
                    SELECT
                        Task_cmmnt,
                                                    CreateBy,
                                                    CreateDt
                    FROM dbo.TaskCommnt 
                    WHERE  Acct = ?
                """

        cursor.execute(sql, vist)

        columns = [column[0] for column in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    finally:
        conn.close()



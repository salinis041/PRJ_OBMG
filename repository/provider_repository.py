from database.connection import get_connection
from werkzeug.security import generate_password_hash

def insert_user(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        # values = _user_values(data)
        password_hash = generate_password_hash(data['user_pass'])
        # placeholders = ", ".join(
        #     ["?"] * len(values)
        # )
        sql = f"""
                                        INSERT INTO Umaster
                                        (
                                            Utype,
                                            Fname,
                                            Lname,
                                            Hphone,
                                            Mphone,
                                            Wphone,
                                            FaxNu,
                                            Email,
                                            DEmail,
                                            Uname,
                                            Upass,
                                            IsActive,
                                            IsEnroll,
                                            CreateBy,
                                            CreateDt

                                        )
                                        VALUES
                                        (
                                          ?,?,?,?,?,?,
                                          ?,?,?,?,?,
                                           'Y',
                                           'N',
                                           1,
                                           GETDATE()
                                        )
                                    """

        cursor.execute(sql,
                       data.get("user-type"),

                       data.get("first_name"),

                       data.get("last_name"),

                       data.get("phome"),

                       data.get("pmobile"),

                       data.get("pwork"),

                       data.get("pfax"),

                       data.get("email"),

                       data.get("direct_email"),

                       data.get("user_name"),

                       password_hash
                       )
        connection.commit()

        return True

    finally:

        connection.close()
def update_user(data):
    connection = get_connection()
    try:
        cursor = connection.cursor()

        sql = f"""
                                           UPDATE Umaster
                                           SET

                                               Utype = ?,
                                               Fname = ?,
                                               Lname = ?,
                                               Hphone = ?,
                                               Mphone = ?,
                                               Wphone = ?,
                                               FaxNu = ?,
                                               Email = ?,
                                               DEmail = ?,
                                               Uname = ?,
                                               ModifyBy=1,
                                               ModifyDt= GETDATE()

                                          Where Uid = ?
                                       """

        cursor.execute(sql,
                       data.get("user-type"), data.get("first_name"), data.get("last_name"),
                       data.get("phome"), data.get("pmobile"), data.get("pwork"),
                       data.get("pfax"), data.get("email"),
                       data.get("direct_email"), data.get("user_name"), data.get("usrid")
                       )


        connection.commit()

        return True

    finally:

        connection.close()
def _user_values(data):
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
        data.get("user-type"),

        data.get("first_name"),

        data.get("last_name"),

        data.get("phome"),

        data.get("pmobile"),

        data.get("pwork"),

        data.get("pfax"),

        data.get("email"),

        data.get("direct_email"),

        data.get("user_name"),

        data.get("user_pass")
    )


def get_Providerdetails( search=None):
    connection = get_connection()

    try:

        cursor = connection.cursor()
        search_condition = ""
        parameters = []

        if search:
            search_condition = """
                        AND (
                            u.Fname LIKE ?
                            OR u.Lname LIKE ?
                            OR p.NPI LIKE ?
                        )
                    """

            search_value = f"%{search}%"

            parameters.extend([
                search_value,
                search_value,
                search_value
            ])
            # ---------------------------------------
            # SECOND SEARCH
            # Account Number only
            # ---------------------------------------



        query = f"""
            SELECT u.Uid,

                 u.Fname + ' ' +u.Lname as ProviderName,

                u.Uname, ISNULL(p.NPI,'') NPI,u.CreateDt CreateDt, ISNULL(p.Spety,'') Spety 
               

            FROM Umaster u left join PractInfo p on p.Uid=u.Uid  where u.Utype='Provider'  
            {search_condition}

            ORDER BY
                u.CreateDt DESC

            

        """


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
def get_provider_by_id(user_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        sql = """
            SELECT
                Utype, Fname, Lname, ISNULL(Hphone,'') Hphone, ISNULL(Mphone,'') Mphone,
                ISNULL(Wphone,'') Wphone, ISNULL(FaxNu,'') FaxNu, ISNULL(Email,'') Email, ISNULL(DEmail,'') DEmail, 
                ISNULL(Uname,'') Uname,ISNULL(PrId,'') PrId,ISNULL(Spety,'') Spety,ISNULL(Deg,'') Deg,ISNULL(NPI,'') NPI,ISNULL(DEA,'') DEA,
                ISNULL(Lic,'') Lic,ISNULL(gender,'') gender,ISNULL(AccNPat,'') AccNPat  
            FROM dbo.Umaster left join PractInfo on PractInfo.Uid=Umaster.Uid
            WHERE Umaster.Uid = ?
        """

        cursor.execute(sql, (user_id,))



        columns = [column[0] for column in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    finally:
        conn.close()
def get_provider_AddList_id(user_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        sql = """
                SELECT
                    PAdId,pr_Loc,pr_Addres,
                                      pr_city,
                                      pr_state,
                                      pr_zip,
                                      pr_phone,
                                      pr_fax 
                FROM dbo.AddPract 
                WHERE IsActive='Y' and Uid = ?
            """

        cursor.execute(sql, (user_id,))

        columns = [column[0] for column in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    finally:
        conn.close()

def update_provider(data,addresses):
    connection = get_connection()
    try:
        cursor = connection.cursor()

        Prv_id = int(data.get("pid") or 0)


        if Prv_id==0:
            sql = f"""
                                INSERT INTO PractInfo
                                (
                                    Spety,
                                    Deg,
                                    NPI,
                                    DEA,
                                    Lic,
                                    gender,
                                    AccNPat,
                                    Uid,
                                    CreateBy,
                                   CreateDt

                                )
                                OUTPUT INSERTED.PrId
                                VALUES
                                (
                                  ?,?,?,?,?,
                                  ?,?,?,
                                   1,
                                   GETDATE()
                                )
                                 
                                
                            """

            cursor.execute(sql,(
                           data.get("specialty"), data.get("degree"), data.get("npi"),
                           data.get("dea"), data.get("licen"), data.get("gender"),
                           data.get("status"), data.get("uid")
            ))
            # Get newly inserted PrId
            row = cursor.fetchone()

            if row is None:
                raise Exception("Provider ID not generated")

            Prv_id = row[0]
            # INSERT Address Details
            if addresses:

                sql2 = """
                                  INSERT INTO AddPract
                                  (
                                      pr_Loc,
                                      pr_Addres,
                                      pr_city,
                                      pr_state,
                                      pr_zip,
                                      pr_phone,
                                      pr_fax,
                                      PrId,
                                      Uid,
                                      IsActive,
                                      CreateBy,
                                      CreateDt
                                  )
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Y', 1, GETDATE())
                              """

                for address in addresses:
                    cursor.execute(sql2, (
                        address.get("location"),
                        address.get("address"),
                        address.get("city"),
                        address.get("state"),
                        address.get("zip"),
                        address.get("aphone"),
                        address.get("afax"),
                        Prv_id,
                        data.get("uid")
                    ))


            connection.commit()
            return Prv_id

    except Exception as e:

        connection.rollback()
        raise

    finally:
        connection.close()


def update_provider_new(data, addresses):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        Prv_id = int(data.get("pid") or 0)
        if Prv_id != 0:
            sql = f"""
                                UPDATE PractInfo
                                SET
                                    Spety = ?,
                                    Deg = ?,
                                    NPI= ?,
                                    DEA= ?,
                                    Lic= ?,
                                    gender= ?,
                                    AccNPat= ?,
                                    Uid= ?,
                                    ModifyBy=1,
                                    ModifyDt= GETDATE()
                                WHERE PrId = ? 


                            """

            cursor.execute(sql, (
                data.get("specialty"), data.get("degree"), data.get("npi"),
                data.get("dea"), data.get("licen"), data.get("gender"),
                data.get("status"), data.get("uid"), data.get("pid")
            ))
            # Get newly inserted PrId
            # row = cursor.fetchone()
            #
            # if row is None:
            #     raise Exception("Provider ID not generated")
            #
            # Prv_id = row[0]

            print("STEP 5: New Provider ID:", Prv_id)
            # INSERT Address Details
            if addresses:

                sql2 = """
                                  INSERT INTO AddPract
                                  (
                                      pr_Loc,
                                      pr_Addres,
                                      pr_city,
                                      pr_state,
                                      pr_zip,
                                      pr_phone,
                                      pr_fax,
                                      PrId,
                                      Uid,
                                      IsActive,
                                      CreateBy,
                                      CreateDt
                                  )
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Y', 1, GETDATE())
                              """

                for address in addresses:
                    cursor.execute(sql2, (
                        address.get("location"),
                        address.get("address"),
                        address.get("city"),
                        address.get("state"),
                        address.get("zip"),
                        address.get("aphone"),
                        address.get("afax"),
                        Prv_id,
                        data.get("uid")
                    ))


            connection.commit()
            return Prv_id

    except Exception as e:

        connection.rollback()
        print("Provider Insert/Update Error:", str(e))
        raise

    finally:
        connection.close()
def Delete_PrAdd(address_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()

        sql = """
                UPDATE dbo.AddPract 
                   SET IsActive='N'
                   FROM dbo.AddPract 
                   WHERE  PAdId = ?
            """

        cursor.execute(sql, (address_id,))
        connection.commit()
        return True


    finally:
        connection.close()


from database.connection import get_connection


def list_providers():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Uid, Uname, Fname, Lname, Hphone, Mphone
            FROM dbo.Umaster
            WHERE Utype = 'Provider' AND ISNULL(IsActive, 'Y') = 'Y'
            ORDER BY Lname, Fname, Uname
        """)
        cols = [c[0] for c in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]
    finally:
        connection.close()


def list_appointments(acct=None, include_archived=False):
    # Appmnt has no archive column; return all rows until an archive field is added.
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT a.AId, a.Acct, a.Mrn, a.ReType, a.PrId, a.App_add,
                   a.App_date, a.App_time, a.App_status, a.App_instr,
                   a.Est_phOffice, a.Pron_inDisch, a.Prov_inNet,
                   a.Prov_RestIns, a.Prov_chpat, a.Prov_AssIns,
                   a.Prov_Aval, a.Prov_FarHosp, a.Prov_ChPcp, a.Pro_Slreasn,
                   u.Uname AS ProviderUsername,
                   LTRIM(RTRIM(CONCAT(ISNULL(u.Fname, ''), ' ', ISNULL(u.Lname, '')))) AS ProviderName,
                   u.Utype AS ProviderType, u.Hphone, u.Mphone
            FROM dbo.Appmnt a
            LEFT JOIN dbo.Umaster u ON u.Uid = a.PrId
            WHERE (? IS NULL OR a.Acct = ?)
            ORDER BY a.App_date DESC, a.AId DESC
        """, (acct, acct))
        cols = [c[0] for c in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]
    finally:
        connection.close()


def get_appointment(aid):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT AId, Acct, Mrn, ReType, PrId, App_add, App_date, App_time,
                   App_status, App_instr, Est_phOffice, Pron_inDisch,
                   Prov_inNet, Prov_RestIns, Prov_chpat, Prov_AssIns,
                   Prov_Aval, Prov_FarHosp, Prov_ChPcp, Pro_Slreasn
            FROM dbo.Appmnt WHERE AId = ?
        """, (aid,))
        row = cursor.fetchone()
        if not row:
            return None
        return dict(zip([c[0] for c in cursor.description], row))
    finally:
        connection.close()


def save_appointment(data, user_id=None, aid=None):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        values = (
            data['acct'], data['mrn'], data['record_type'], data['provider_id'],
            data['address'], data['date'], data['time'], data['status'],
            data['instructions'], data['established'], data['discharge'],
            data['in_network'], data['restricted_insurance'], data['chosen_patient'],
            data['assigned_insurance'], data['availability'], data['far_hospital'],
            data['chosen_pcp'], data['selection_notes']
        )
        if aid is None:
            cursor.execute("""
                INSERT INTO dbo.Appmnt (
                    Acct, Mrn, ReType, PrId, App_add, App_date, App_time,
                    App_status, App_instr, Est_phOffice, Pron_inDisch,
                    Prov_inNet, Prov_RestIns, Prov_chpat, Prov_AssIns,
                    Prov_Aval, Prov_FarHosp, Prov_ChPcp, Pro_Slreasn,
                    CreateBy, CreateDt
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, GETDATE()
                )
            """, values + (user_id,))
        else:
            cursor.execute("""
                UPDATE dbo.Appmnt SET
                    Acct=?, Mrn=?, ReType=?, PrId=?, App_add=?, App_date=?,
                    App_time=?, App_status=?, App_instr=?, Est_phOffice=?,
                    Pron_inDisch=?, Prov_inNet=?, Prov_RestIns=?, Prov_chpat=?,
                    Prov_AssIns=?, Prov_Aval=?, Prov_FarHosp=?, Prov_ChPcp=?,
                    Pro_Slreasn=?, ModifyBy=?, ModifyDt=GETDATE()
                WHERE AId=?
            """, values + (user_id, aid))
            if cursor.rowcount == 0:
                raise ValueError('Appointment not found.')
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

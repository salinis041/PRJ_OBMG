from database.connection import get_connection
from werkzeug.security import generate_password_hash


def list_users():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Uid, Uname, Fname, Lname, Utype, IsActive
            FROM dbo.Umaster ORDER BY Uname
        """)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        connection.close()


def get_user(uid):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Uid, Utype, Fname, Lname, Hphone, Mphone, Wphone, FaxNu,
                   Email, DEmail, Uname, NxtLgpawChg, IsActive
            FROM dbo.Umaster WHERE Uid = ?
        """, (uid,))
        row = cursor.fetchone()
        if not row:
            return None
        columns = [column[0] for column in cursor.description]
        user = dict(zip(columns, row))
        cursor.execute("SELECT PrUid FROM dbo.ProxyUsr WHERE Uid = ? AND IsActive = 'Y'", (uid,))
        user['proxy_uids'] = [int(r[0]) for r in cursor.fetchall()]
        return user
    finally:
        connection.close()


def create_user(data, created_by=0):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT TOP 1 Uid FROM dbo.Umaster WHERE Uname = ?", (data['username'],))
        if cursor.fetchone():
            raise ValueError("That username already exists.")
        password_hash = generate_password_hash(data['password'])
        cursor.execute("""
            INSERT INTO dbo.Umaster (
                Utype, Fname, Lname, Hphone, Mphone, Wphone, FaxNu,
                Email, DEmail, Uname, Upass, NxtLgpawChg, IsActive,
                IsEnroll, CreateBy, CreateDt
            )
            OUTPUT INSERTED.Uid
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Y', 'N', ?, GETDATE())
        """, (
            data['user_type'], data['first_name'], data['last_name'],
            data['home_phone'], data['mobile_phone'], data['work_phone'], data['fax'],
            data['email'], data['direct_email'], data['username'], password_hash,
            'Y' if data['change_password'] else 'N', created_by,
        ))
        row = cursor.fetchone()
        if not row:
            raise RuntimeError('The database did not return the new user ID.')
        new_uid = int(row[0])
        for proxy_uid in data['proxy_uids']:
            if proxy_uid != new_uid:
                cursor.execute("""
                    INSERT INTO dbo.ProxyUsr (Uid, PrUid, IsActive, CreateBy, CreateDt)
                    VALUES (?, ?, 'Y', ?, GETDATE())
                """, (new_uid, proxy_uid, created_by))
        connection.commit()
        return new_uid
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def update_user(uid, data, modified_by=0):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT TOP 1 Uid FROM dbo.Umaster WHERE Uname = ? AND Uid <> ?", (data['username'], uid))
        if cursor.fetchone():
            raise ValueError('That username is already used by another user.')
        fields = [
            data['user_type'], data['first_name'], data['last_name'], data['home_phone'],
            data['mobile_phone'], data['work_phone'], data['fax'], data['email'],
            data['direct_email'], data['username'], 'Y' if data['change_password'] else 'N',
        ]
        password_sql = ''
        if data['password']:
            password_sql = ', Upass = ?'
            fields.append(generate_password_hash(data['password']))
        fields.extend([modified_by, uid])
        cursor.execute(f"""
            UPDATE dbo.Umaster SET
                Utype = ?, Fname = ?, Lname = ?, Hphone = ?, Mphone = ?, Wphone = ?,
                FaxNu = ?, Email = ?, DEmail = ?, Uname = ?, NxtLgpawChg = ?
                {password_sql}, ModifyBy = ?, ModifyDt = GETDATE()
            WHERE Uid = ?
        """, tuple(fields))
        if cursor.rowcount == 0:
            raise ValueError('User not found.')
        # Replace active proxy mappings with the selections submitted on the form.
        cursor.execute("UPDATE dbo.ProxyUsr SET IsActive = 'N', ModifyBy = ?, ModifyDt = GETDATE() WHERE Uid = ? AND IsActive = 'Y'", (modified_by, uid))
        for proxy_uid in data['proxy_uids']:
            if proxy_uid != uid:
                cursor.execute("""
                    INSERT INTO dbo.ProxyUsr (Uid, PrUid, IsActive, CreateBy, CreateDt)
                    VALUES (?, ?, 'Y', ?, GETDATE())
                """, (uid, proxy_uid, modified_by))
        connection.commit()
        return uid
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

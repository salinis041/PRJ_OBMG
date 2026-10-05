from database.connection import get_remote_connection


PAGE_SIZE = 50


def get_available_details(page=1, search=None):

    offset = (page - 1) * PAGE_SIZE

    connection = get_remote_connection()

    try:

        cursor = connection.cursor()

        search_condition = ""
        parameters = []

        if search:

            search_condition = """
                AND (
                    pv.vst_ext_id LIKE ?
                    OR pv.med_rec_no LIKE ?
                    OR pat.fst_nm LIKE ?
                    OR pat.lst_nm LIKE ?
                )
            """

            search_value = f"%{search}%"

            parameters.extend([
                search_value,
                search_value,
                search_value,
                search_value
            ])

        query = f"""
            SELECT

                pv.vst_int_id AS [Visit ID],

                pv.vst_ext_id AS [Account Number],

                pv.med_rec_no AS [Med Rec Nbr],

                ISNULL(
                    dbo.fn_get_attend_dr_name(pv.vst_int_id),
                    ''
                ) AS [Phys Name Attending],

                ISNULL(
                    (
                        SELECT TOP 1
                            lic.car_gvr_lic_no
                        FROM TPM315_VISIT_CARE_GIVER vcg
                        INNER JOIN TPM114_CAR_GVR_FUNC func
                            ON func.func_aso_int_id = vcg.func_aso_int_id
                        INNER JOIN TSM180_MST_COD_DTL role
                            ON role.cod_dtl_int_id = func.func_int_id
                        INNER JOIN TPM100_CARE_GIVER cg
                            ON cg.car_gvr_int_id = func.car_gvr_int_id
                        LEFT JOIN TPM115_CAR_GVR_LIC lic
                            ON lic.car_gvr_int_id = cg.car_gvr_int_id
                        LEFT JOIN TSM180_MST_COD_DTL lcd
                            ON lcd.cod_dtl_int_id = lic.car_gvr_lic_id
                        WHERE vcg.vst_int_id = pv.vst_int_id
                        AND role.cod_dtl_ext_id = 'ATTND'
                        AND vcg.row_sta_cd = 'A'
                        AND lcd.cod_dtl_ext_id = 'NPI'
                    ),
                    ''
                ) AS [Phys NPI],

                ISNULL(
                    (
                        SELECT TOP 1
                            cg.car_gvr_ext_id
                        FROM TPM315_VISIT_CARE_GIVER vcg
                        INNER JOIN TPM114_CAR_GVR_FUNC func
                            ON func.func_aso_int_id = vcg.func_aso_int_id
                        INNER JOIN TSM180_MST_COD_DTL role
                            ON role.cod_dtl_int_id = func.func_int_id
                        INNER JOIN TPM100_CARE_GIVER cg
                            ON cg.car_gvr_int_id = func.car_gvr_int_id
                        WHERE vcg.vst_int_id = pv.vst_int_id
                        AND role.cod_dtl_ext_id = 'ATTND'
                        AND vcg.row_sta_cd = 'A'
                    ),
                    ''
                ) AS [Phys ID],

                pv.adm_ts AS [Admit Date],

                pv.dschrg_ts AS [Discharge Date],

                dbo.fn_get_cod_dtl_ext_id(
                    pv.pat_ty
                ) AS [Patient Type],

                dbo.fn_get_cod_dtl_ext_id(
                    pv.fin_cls_cd
                ) AS [Admit FC],

                dbo.fn_get_cod_ds(
                    pv.fin_cls_cd
                ) AS [Admit FC Name],

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        pv.cur_fin_cls_cd
                    ),
                    ''
                ) AS [Curr FC],

                ISNULL(
                    dbo.fn_get_cod_ds(
                        pv.cur_fin_cls_cd
                    ),
                    ''
                ) AS [Curr FC Nm],

                ISNULL(
                    pat.fst_nm,
                    ''
                ) AS [Pat First Nm],

                ISNULL(
                    pat.mid_nm,
                    ''
                ) AS [Pat Middle Nm],

                ISNULL(
                    pat.lst_nm,
                    ''
                ) AS [Pat Last Nm],

                ISNULL(
                    pat.nam_sfx_cd,
                    ''
                ) AS [Pat Name Suf],

                ISNULL(
                    pat.bth_ts,
                    ''
                ) AS [Pat DOB],

                DATEDIFF(
                    month,
                    pat.bth_ts,
                    pv.adm_ts
                ) / 12 AS Age,

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        pat.sex_cd
                    ),
                    ''
                ) AS [Pat Gender],

                ISNULL(
                    padr.adr_str_1,
                    ''
                ) AS [Pat Addr 1],

                ISNULL(
                    padr.adr_str_2,
                    ''
                ) AS [Pat Addr 2],

                ISNULL(
                    padr.cty_nm,
                    ''
                ) AS [Pat City],

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        padr.ste_cd
                    ),
                    ''
                ) AS [Pat State],

                ISNULL(
                    padr.zip_cd,
                    ''
                ) AS [Pat Zip],

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        padr.cty_cd
                    ),
                    ''
                ) AS [Pat Country],

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        padr.ste_cd
                    ),
                    ''
                ) AS [Pat Province],

                ISNULL(
                    org.org_nm,
                    ''
                ) AS [Facility],

                ISNULL(
                    dbo.fn_get_cod_ds(
                        pv.adm_src_cd
                    ),
                    ''
                ) AS [AdmitSource],

                ISNULL(
                    dbo.fn_get_cod_ds(
                        pv.dschg_sta_cd
                    ),
                    ''
                ) AS [DischStat],

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        pat.rac_cd
                    ),
                    ''
                ) AS Race,

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        pat.pri_lng_cd
                    ),
                    ''
                ) AS Language,

                ISNULL(
                    pdrg.drg_wgt_no,
                    ''
                ) AS [DRG Weight],

                DATEDIFF(
                    hour,
                    pv.adm_ts,
                    ISNULL(
                        pv.dschrg_ts,
                        GETDATE()
                    )
                ) AS LOSHours

            FROM TPM300_PAT_VISIT pv

            LEFT JOIN TSM040_PERSON_HDR pat
                ON pat.psn_int_id = pv.psn_int_id

            LEFT JOIN TSM021_ENT_ADR eadr
                ON eadr.psn_int_id = pat.psn_int_id
                AND eadr.pri_fg = 'Y'

            LEFT JOIN TSM020_ADDRESS padr
                ON padr.adr_int_id = eadr.adr_int_id

            LEFT JOIN TMR410_VISIT_DRG pdrg
                ON pdrg.vst_int_id = pv.vst_int_id

            LEFT JOIN TSM030_ORGANIZATION org
                ON org.org_int_id = pv.org_int_id

            WHERE pv.dschrg_ts IS NULL

            {search_condition}

            ORDER BY
                pv.adm_ts DESC,
                pv.vst_int_id DESC

            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        """

        parameters.extend([
            offset,
            PAGE_SIZE
        ])

        cursor.execute(
            query,
            parameters
        )

        columns = [
            column[0]
            for column in cursor.description
        ]

        details = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return details

    finally:

        connection.close()


def get_available_details_count(search=None):

    connection = get_remote_connection()

    try:

        cursor = connection.cursor()

        search_condition = ""
        parameters = []

        if search:

            search_condition = """
                AND (
                    pv.vst_ext_id LIKE ?
                    OR pv.med_rec_no LIKE ?
                    OR pat.fst_nm LIKE ?
                    OR pat.lst_nm LIKE ?
                )
            """

            search_value = f"%{search}%"

            parameters.extend([
                search_value,
                search_value,
                search_value,
                search_value
            ])

        query = f"""
            SELECT COUNT(*)

            FROM TPM300_PAT_VISIT pv

            LEFT JOIN TSM040_PERSON_HDR pat
                ON pat.psn_int_id = pv.psn_int_id

            WHERE pv.dschrg_ts IS NULL

            {search_condition}
        """

        cursor.execute(
            query,
            parameters
        )

        return cursor.fetchone()[0]

    finally:

        connection.close()


def get_remote_detail_by_visit_id(visit_id):

    connection = get_remote_connection()

    try:

        cursor = connection.cursor()

        query = """
            SELECT

                pv.vst_int_id AS [Visit ID],

                pv.vst_ext_id AS [Account Number],

                pv.med_rec_no AS [Med Rec Nbr],

                ISNULL(
                    pat.fst_nm,
                    ''
                ) AS [Pat First Nm],

                ISNULL(
                    pat.mid_nm,
                    ''
                ) AS [Pat Middle Nm],

                ISNULL(
                    pat.lst_nm,
                    ''
                ) AS [Pat Last Nm],

                ISNULL(
                    pat.bth_ts,
                    ''
                ) AS [Pat DOB],

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        pat.sex_cd
                    ),
                    ''
                ) AS [Pat Gender],

                ISNULL(
                    org.org_nm,
                    ''
                ) AS [Facility],

                ISNULL(
                    dbo.fn_get_attend_dr_name(
                        pv.vst_int_id
                    ),
                    ''
                ) AS [Phys Name Attending],

                pv.adm_ts AS [Admit Date],

                pv.dschrg_ts AS [Discharge Date],

                dbo.fn_get_cod_dtl_ext_id(
                    pv.pat_ty
                ) AS [Patient Type],

                dbo.fn_get_cod_dtl_ext_id(
                    pv.fin_cls_cd
                ) AS [Admit FC],

                dbo.fn_get_cod_ds(
                    pv.fin_cls_cd
                ) AS [Admit FC Name],

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        pv.cur_fin_cls_cd
                    ),
                    ''
                ) AS [Curr FC],

                ISNULL(
                    dbo.fn_get_cod_ds(
                        pv.cur_fin_cls_cd
                    ),
                    ''
                ) AS [Curr FC Nm],

                ISNULL(
                    padr.adr_str_1,
                    ''
                ) AS [Pat Addr 1],

                ISNULL(
                    padr.adr_str_2,
                    ''
                ) AS [Pat Addr 2],

                ISNULL(
                    padr.cty_nm,
                    ''
                ) AS [Pat City],

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        padr.ste_cd
                    ),
                    ''
                ) AS [Pat State],

                ISNULL(
                    padr.zip_cd,
                    ''
                ) AS [Pat Zip],

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        pat.rac_cd
                    ),
                    ''
                ) AS Race,

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        pat.pri_lng_cd
                    ),
                    ''
                ) AS Language

            FROM TPM300_PAT_VISIT pv

            LEFT JOIN TSM040_PERSON_HDR pat
                ON pat.psn_int_id = pv.psn_int_id

            LEFT JOIN TSM021_ENT_ADR eadr
                ON eadr.psn_int_id = pat.psn_int_id
                AND eadr.pri_fg = 'Y'

            LEFT JOIN TSM020_ADDRESS padr
                ON padr.adr_int_id = eadr.adr_int_id

            LEFT JOIN TSM030_ORGANIZATION org
                ON org.org_int_id = pv.org_int_id

            WHERE pv.vst_int_id = ?
        """

        cursor.execute(
            query,
            visit_id
        )

        row = cursor.fetchone()

        if not row:
            return None

        columns = [
            column[0]
            for column in cursor.description
        ]

        return dict(
            zip(columns, row)
        )

    finally:

        connection.close()
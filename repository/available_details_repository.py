from database.connection import get_remote_connection


PAGE_SIZE = 50


# ============================================================
# CURRENT CENSUS
# ============================================================

def get_available_details(
    page=1,
    search=""
):
    """
    Get the current census.

    Supports server-side progressive search.
    """

    offset = (page - 1) * PAGE_SIZE

    search = (search or "").strip()

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

                pat.bth_ts AS [Pat DOB],

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

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        pv.pat_ty
                    ),
                    ''
                ) AS [Patient Type]

            FROM TPM300_PAT_VISIT pv

            LEFT JOIN TSM040_PERSON_HDR pat
                ON pat.psn_int_id = pv.psn_int_id

            LEFT JOIN TSM030_ORGANIZATION org
                ON org.org_int_id = pv.org_int_id

            WHERE pv.dschrg_ts IS NULL
        """

        parameters = []

        # ----------------------------------------------------
        # Progressive search
        #
        # Searches Account #, MRN, first name,
        # middle name, last name and facility.
        # ----------------------------------------------------

        if search:

            query += """
                AND (
                    CAST(
                        pv.vst_ext_id
                        AS VARCHAR(50)
                    ) COLLATE SQL_Latin1_General_CP1_CI_AS LIKE ?

                    OR CAST(
                        pv.med_rec_no
                        AS VARCHAR(50)
                    ) COLLATE SQL_Latin1_General_CP1_CI_AS LIKE ?

                    OR ISNULL(
                        pat.fst_nm,
                        ''
                    ) COLLATE SQL_Latin1_General_CP1_CI_AS LIKE ?

                    OR ISNULL(
                        pat.mid_nm,
                        ''
                    ) COLLATE SQL_Latin1_General_CP1_CI_AS LIKE ?

                    OR ISNULL(
                        pat.lst_nm,
                        ''
                    ) COLLATE SQL_Latin1_General_CP1_CI_AS LIKE ?

                    OR ISNULL(
                        org.org_nm,
                        ''
                    ) COLLATE SQL_Latin1_General_CP1_CI_AS LIKE ?
                )
            """

            search_value = "%" + search + "%"

            parameters.extend(
                [
                    search_value,
                    search_value,
                    search_value,
                    search_value,
                    search_value,
                    search_value,
                ]
            )

        query += """
            ORDER BY
                pv.adm_ts DESC,
                pv.vst_int_id DESC

            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        """

        parameters.extend(
            [
                offset,
                PAGE_SIZE
            ]
        )

        cursor.execute(
            query,
            tuple(parameters)
        )

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


def get_available_details_count(
    search=""
):
    """
    Get the total number of current census records.

    Applies the same server-side search used by
    get_available_details().
    """

    search = (search or "").strip()

    connection = get_remote_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT COUNT(*)

            FROM TPM300_PAT_VISIT pv

            LEFT JOIN TSM040_PERSON_HDR pat
                ON pat.psn_int_id = pv.psn_int_id

            LEFT JOIN TSM030_ORGANIZATION org
                ON org.org_int_id = pv.org_int_id

            WHERE pv.dschrg_ts IS NULL
        """

        parameters = []

        if search:

            query += """
                AND (
                    CAST(
                        pv.vst_ext_id
                        AS VARCHAR(50)
                    ) COLLATE SQL_Latin1_General_CP1_CI_AS LIKE ?

                    OR CAST(
                        pv.med_rec_no
                        AS VARCHAR(50)
                    ) COLLATE SQL_Latin1_General_CP1_CI_AS LIKE ?

                    OR ISNULL(
                        pat.fst_nm,
                        ''
                    ) COLLATE SQL_Latin1_General_CP1_CI_AS LIKE ?

                    OR ISNULL(
                        pat.mid_nm,
                        ''
                    ) COLLATE SQL_Latin1_General_CP1_CI_AS LIKE ?

                    OR ISNULL(
                        pat.lst_nm,
                        ''
                    ) COLLATE SQL_Latin1_General_CP1_CI_AS LIKE ?

                    OR ISNULL(
                        org.org_nm,
                        ''
                    ) COLLATE SQL_Latin1_General_CP1_CI_AS LIKE ?
                )
            """

            search_value = "%" + search + "%"

            parameters.extend(
                [
                    search_value,
                    search_value,
                    search_value,
                    search_value,
                    search_value,
                    search_value,
                ]
            )

        cursor.execute(
            query,
            tuple(parameters)
        )

        return cursor.fetchone()[0]

    finally:
        connection.close()

def get_available_details_page(
    page=1,
    search=""
):
    """
    Return the complete pagination information
    required by Available Details.
    """

    total_records = get_available_details_count(
        search=search
    )

    total_pages = (
        (total_records + PAGE_SIZE - 1)
        // PAGE_SIZE
        if total_records
        else 0
    )

    if total_pages and page > total_pages:
        page = total_pages

    if page < 1:
        page = 1

    details = get_available_details(
        page=page,
        search=search
    )

    if details:

        start_record = (
            (page - 1) * PAGE_SIZE
        ) + 1

        end_record = min(
            page * PAGE_SIZE,
            total_records
        )

    else:

        start_record = 0
        end_record = 0

    # --------------------------------------------------------
    # Keep the pagination display compact.
    # --------------------------------------------------------

    page_numbers = []

    if total_pages:

        start_page = max(
            1,
            page - 2
        )

        end_page = min(
            total_pages,
            page + 2
        )

        page_numbers = list(
            range(
                start_page,
                end_page + 1
            )
        )

    return {
        "details": details,
        "total_records": total_records,
        "total_pages": total_pages,
        "start_record": start_record,
        "end_record": end_record,
        "page_numbers": page_numbers,
        "page": page,
        "search": search,
    }

# ============================================================
# SEARCH BY VISIT ID
# ============================================================

def get_remote_visit_for_display(visit_id):
    """
    Get the visit for Search by Visit ID.

    Visit ID is normally pv.vst_int_id.
    The comparison is converted to VARCHAR so that
    values entered from the UI are handled consistently.
    """

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

                pat.bth_ts AS [Pat DOB],

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

                ISNULL(
                    dbo.fn_get_cod_dtl_ext_id(
                        pv.pat_ty
                    ),
                    ''
                ) AS [Patient Type]

            FROM TPM300_PAT_VISIT pv

            LEFT JOIN TSM040_PERSON_HDR pat
                ON pat.psn_int_id = pv.psn_int_id

            LEFT JOIN TSM030_ORGANIZATION org
                ON org.org_int_id = pv.org_int_id
WHERE CAST(pv.vst_ext_id AS VARCHAR(50)) = ?
        """

        cursor.execute(
            query,
            (str(visit_id).strip(),)
        )

        columns = [
            column[0]
            for column in cursor.description
        ]

        rows = cursor.fetchall()

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    finally:
        connection.close()

def get_available_visit(visit_id):
    """
    Get the Available Details display record
    using the Account Number.
    """

    rows = get_remote_visit_for_display(
        visit_id
    )

    if not rows:
        return None

    return rows[0]
# ============================================================
# FULL VISIT FOR INSERT / UPDATE
# ============================================================

def get_full_remote_visit(visit_id):
    """
    Get the complete remote visit.

    This query is only executed after the user clicks
    the + button.

    The returned fields correspond to dbo.Visits.
    """

    query = """
        SELECT

            pv.vst_int_id AS [Visit ID],

            pv.vst_ext_id AS [Account Number],

            pv.med_rec_no AS [Med Rec Nbr],

            ISNULL(
                dbo.fn_get_attend_dr_name(
                    pv.vst_int_id
                ),
                ''
            ) AS [Phys Name Attending],

            ISNULL(
                (
                    SELECT TOP 1
                        lic.car_gvr_lic_no

                    FROM TPM315_VISIT_CARE_GIVER vcg

                    INNER JOIN TPM114_CAR_GVR_FUNC func
                        ON func.func_aso_int_id =
                           vcg.func_aso_int_id

                    INNER JOIN TSM180_MST_COD_DTL role
                        ON role.cod_dtl_int_id =
                           func.func_int_id

                    INNER JOIN TPM100_CARE_GIVER cg
                        ON cg.car_gvr_int_id =
                           func.car_gvr_int_id

                    LEFT JOIN TPM115_CAR_GVR_LIC lic
                        ON lic.car_gvr_int_id =
                           cg.car_gvr_int_id

                    LEFT JOIN TSM180_MST_COD_DTL lcd
                        ON lcd.cod_dtl_int_id =
                           lic.car_gvr_lic_id

                    WHERE vcg.vst_int_id =
                          pv.vst_int_id

                      AND role.cod_dtl_ext_id =
                          'ATTND'

                      AND vcg.row_sta_cd =
                          'A'

                      AND lcd.cod_dtl_ext_id =
                          'NPI'
                ),
                ''
            ) AS [Phys NPI],

            ISNULL(
                (
                    SELECT TOP 1
                        cg.car_gvr_ext_id

                    FROM TPM315_VISIT_CARE_GIVER vcg

                    INNER JOIN TPM114_CAR_GVR_FUNC func
                        ON func.func_aso_int_id =
                           vcg.func_aso_int_id

                    INNER JOIN TSM180_MST_COD_DTL role
                        ON role.cod_dtl_int_id =
                           func.func_int_id

                    INNER JOIN TPM100_CARE_GIVER cg
                        ON cg.car_gvr_int_id =
                           func.car_gvr_int_id

                    WHERE vcg.vst_int_id =
                          pv.vst_int_id

                      AND role.cod_dtl_ext_id =
                          'ATTND'

                      AND vcg.row_sta_cd =
                          'A'
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
                pat.lst_nm,
                ''
            ) AS [Pat Last Nm],

            ISNULL(
                pat.mid_nm,
                ''
            ) AS [Pat Middle Nm],

            ISNULL(
                pat.fst_nm,
                ''
            ) AS [Pat First Nm],

            ISNULL(
                pat.nam_sfx_cd,
                ''
            ) AS [Pat Name Suf],

            pat.bth_ts AS [Pat DOB],

            ISNULL(
                dbo.fn_get_cod_dtl_ext_id(
                    pat.sex_cd
                ),
                ''
            ) AS [Pat Gender],

            ISNULL(
                pat.soc_scu_no,
                ''
            ) AS [Pat SSN],

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
                (
                    SELECT TOP 1
                        ISNULL(
                            '(' +
                            RTRIM(pphn.phn_ara_cd) +
                            ') ',
                            ''
                        )
                        +
                        ISNULL(
                            RTRIM(pphn.phn_exc_no) +
                            '-',
                            ''
                        )
                        +
                        ISNULL(
                            RTRIM(pphn.phn_lcl_no),
                            ''
                        )

                    FROM TSM061_ENT_PHN ephn

                    LEFT JOIN TSM060_PHONE pphn
                        ON pphn.phn_int_id =
                           ephn.phn_int_id

                    WHERE ephn.psn_int_id =
                          pat.psn_int_id

                      AND dbo.fn_get_cod_dtl_ext_id(
                              ephn.phn_use_cd
                          ) IN ('HOME', 'MAIN')

                    ORDER BY
                        ephn.lst_mod_ts DESC
                ),
                ''
            ) AS [Pat Home Ph],

            ISNULL(
                (
                    SELECT TOP 1
                        ISNULL(
                            '(' +
                            RTRIM(pphn.phn_ara_cd) +
                            ') ',
                            ''
                        )
                        +
                        ISNULL(
                            RTRIM(pphn.phn_exc_no) +
                            '-',
                            ''
                        )
                        +
                        ISNULL(
                            RTRIM(pphn.phn_lcl_no),
                            ''
                        )

                    FROM TSM061_ENT_PHN ephn

                    LEFT JOIN TSM060_PHONE pphn
                        ON pphn.phn_int_id =
                           ephn.phn_int_id

                    WHERE ephn.psn_int_id =
                          pat.psn_int_id

                      AND dbo.fn_get_cod_dtl_ext_id(
                              ephn.phn_use_cd
                          ) = 'WORK'

                    ORDER BY
                        ephn.lst_mod_ts DESC
                ),
                ''
            ) AS [Pat Work Ph],

            ISNULL(
                (
                    SELECT TOP 1
                        ISNULL(
                            '(' +
                            RTRIM(pphn.phn_ara_cd) +
                            ') ',
                            ''
                        )
                        +
                        ISNULL(
                            RTRIM(pphn.phn_exc_no) +
                            '-',
                            ''
                        )
                        +
                        ISNULL(
                            RTRIM(pphn.phn_lcl_no),
                            ''
                        )

                    FROM TSM061_ENT_PHN ephn

                    LEFT JOIN TSM060_PHONE pphn
                        ON pphn.phn_int_id =
                           ephn.phn_int_id

                    WHERE ephn.psn_int_id =
                          pat.psn_int_id

                      AND dbo.fn_get_cod_dtl_ext_id(
                              ephn.phn_use_cd
                          ) IN ('CELL', 'MOBILE')

                    ORDER BY
                        ephn.lst_mod_ts DESC
                ),
                ''
            ) AS [Pat Cell Ph],

            ISNULL(
                (
                    SELECT TOP 1
                        org.org_nm

                    FROM THR101_EMP_HIST_HDR eml

                    LEFT JOIN TSM030_ORGANIZATION org
                        ON org.org_int_id =
                           eml.empr_int_id

                    WHERE eml.psn_int_id =
                          pv.psn_int_id

                    ORDER BY
                        eml.emp_seq_no DESC
                ),
                ''
            ) AS [Pat Empl Nm],

            ISNULL(
                (
                    SELECT TOP 1
                        dbo.fn_get_cod_ds(
                            vpyr.rel_cd
                        )

                    FROM TPM311_VISIT_PAYOR vpyr

                    WHERE vpyr.vst_int_id =
                          pv.vst_int_id

                      AND vpyr.pyr_seq_no =
                          4981
                ),
                ''
            ) AS [Guar Relation],

            ISNULL(
                (
                    SELECT TOP 1
                        vpyr.pol_hld_nm

                    FROM TPM311_VISIT_PAYOR vpyr

                    WHERE vpyr.vst_int_id =
                          pv.vst_int_id

                      AND vpyr.pyr_seq_no =
                          4981
                ),
                ''
            ) AS [Guar],

            ISNULL(
                guar.fst_nm,
                ''
            ) AS [Guar First Nm],

            ISNULL(
                guar.mid_nm,
                ''
            ) AS [Guar Middle Nm],

            ISNULL(
                guar.lst_nm,
                ''
            ) AS [Guar Last Nm],

            ISNULL(
                guar.nam_sfx_cd,
                ''
            ) AS [Guar Name Suf],

            guar.bth_ts AS [Guar DOB],

            ISNULL(
                guar.soc_scu_no,
                ''
            ) AS [Guar SSN],

            ISNULL(
                dbo.fn_get_cod_dtl_ext_id(
                    guar.sex_cd
                ),
                ''
            ) AS [Guar Gender],

            ISNULL(
                gadr.adr_str_1,
                ''
            ) AS [Guar Addr 1],

            ISNULL(
                gadr.adr_str_2,
                ''
            ) AS [Guar Addr 2],

            ISNULL(
                gadr.cty_nm,
                ''
            ) AS [Guar City],

            ISNULL(
                dbo.fn_get_cod_dtl_ext_id(
                    gadr.ste_cd
                ),
                ''
            ) AS [Guar State],

            ISNULL(
                gadr.zip_cd,
                ''
            ) AS [Guar Zipcode],

            ISNULL(
                dbo.fn_get_cod_dtl_ext_id(
                    gadr.cty_cd
                ),
                ''
            ) AS [Guar Country],

            ISNULL(
                dbo.fn_get_cod_dtl_ext_id(
                    gadr.ste_cd
                ),
                ''
            ) AS [Guar Province],

            ISNULL(
                (
                    SELECT TOP 1
                        ISNULL(
                            '(' +
                            RTRIM(pphn.phn_ara_cd) +
                            ') ',
                            ''
                        )
                        +
                        ISNULL(
                            RTRIM(pphn.phn_exc_no) +
                            '-',
                            ''
                        )
                        +
                        ISNULL(
                            RTRIM(pphn.phn_lcl_no),
                            ''
                        )

                    FROM TSM061_ENT_PHN ephn

                    LEFT JOIN TSM060_PHONE pphn
                        ON pphn.phn_int_id =
                           ephn.phn_int_id

                    WHERE ephn.psn_int_id =
                          guar.psn_int_id

                      AND dbo.fn_get_cod_dtl_ext_id(
                              ephn.phn_use_cd
                          ) IN ('HOME', 'MAIN')

                    ORDER BY
                        ephn.lst_mod_ts DESC
                ),
                ''
            ) AS [Guar Home Ph],

            ISNULL(
                (
                    SELECT TOP 1
                        ISNULL(
                            '(' +
                            RTRIM(pphn.phn_ara_cd) +
                            ') ',
                            ''
                        )
                        +
                        ISNULL(
                            RTRIM(pphn.phn_exc_no) +
                            '-',
                            ''
                        )
                        +
                        ISNULL(
                            RTRIM(pphn.phn_lcl_no),
                            ''
                        )

                    FROM TSM061_ENT_PHN ephn

                    LEFT JOIN TSM060_PHONE pphn
                        ON pphn.phn_int_id =
                           ephn.phn_int_id

                    WHERE ephn.psn_int_id =
                          guar.psn_int_id

                      AND dbo.fn_get_cod_dtl_ext_id(
                              ephn.phn_use_cd
                          ) = 'WORK'

                    ORDER BY
                        ephn.lst_mod_ts DESC
                ),
                ''
            ) AS [Guar Work Ph],

            ISNULL(
                (
                    SELECT TOP 1
                        ISNULL(
                            '(' +
                            RTRIM(pphn.phn_ara_cd) +
                            ') ',
                            ''
                        )
                        +
                        ISNULL(
                            RTRIM(pphn.phn_exc_no) +
                            '-',
                            ''
                        )
                        +
                        ISNULL(
                            RTRIM(pphn.phn_lcl_no),
                            ''
                        )

                    FROM TSM061_ENT_PHN ephn

                    LEFT JOIN TSM060_PHONE pphn
                        ON pphn.phn_int_id =
                           ephn.phn_int_id

                    WHERE ephn.psn_int_id =
                          guar.psn_int_id

                      AND dbo.fn_get_cod_dtl_ext_id(
                              ephn.phn_use_cd
                          ) IN ('CELL', 'MOBILE')

                    ORDER BY
                        ephn.lst_mod_ts DESC
                ),
                ''
            ) AS [Guar Cell Ph],

            ISNULL(
                (
                    SELECT TOP 1
                        dbo.fn_get_org_name(
                            vpyr.eml_int_id
                        )

                    FROM TPM311_VISIT_PAYOR vpyr

                    WHERE vpyr.vst_int_id =
                          pv.vst_int_id

                      AND vpyr.pyr_seq_no =
                          4981
                ),
                ''
            ) AS [Guar Empl],

            DATEDIFF(
                hour,
                pv.adm_ts,
                ISNULL(
                    pv.dschrg_ts,
                    GETDATE()
                )
            ) AS [LOSHours],

            ISNULL(
                pdrg.drg_wgt_no,
                ''
            ) AS [DRG Weight],

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
                (
                    SELECT TOP 1
                        plan_ds

                    FROM TPM311_VISIT_PAYOR vpyr

                    INNER JOIN TPM700_PAYOR_PLAN ppln
                        ON ppln.plan_int_id =
                           vpyr.plan_int_id

                       AND ppln.row_sta_cd =
                           'A'

                    WHERE vpyr.vst_int_id =
                          pv.vst_int_id

                      AND dbo.fn_get_cod_dtl_ext_id(
                              vpyr.pyr_seq_no
                          ) = '1'

                      AND vpyr.row_sta_cd =
                          'A'
                ),
                ''
            ) AS [primary I-Plan description],

            ISNULL(
                (
                    SELECT TOP 1
                        plan_ds

                    FROM TPM311_VISIT_PAYOR vpyr

                    INNER JOIN TPM700_PAYOR_PLAN ppln
                        ON ppln.plan_int_id =
                           vpyr.plan_int_id

                       AND ppln.row_sta_cd =
                           'A'

                    WHERE vpyr.vst_int_id =
                          pv.vst_int_id

                      AND dbo.fn_get_cod_dtl_ext_id(
                              vpyr.pyr_seq_no
                          ) = '2'

                      AND vpyr.row_sta_cd =
                          'A'
                ),
                ''
            ) AS [secondary I-Plan description],

            dbo.fn_get_cod_dtl_ext_id(
                pat.rac_cd
            ) AS [Race],

            dbo.fn_get_cod_dtl_ext_id(
                pat.pri_lng_cd
            ) AS [Language],

            ISNULL(
                (
                    SELECT
                        vpyr.certificate_no

                    FROM TPM311_VISIT_PAYOR vpyr

                    WHERE vpyr.vst_int_id =
                          pv.vst_int_id

                      AND vpyr.pyr_seq_no =
                          4981

                      AND vpyr.row_sta_cd =
                          'A'
                ),
                ''
            ) AS [Insurance1PolicyID]

        FROM TPM300_PAT_VISIT pv

        LEFT JOIN TSM040_PERSON_HDR pat
            ON pat.psn_int_id =
               pv.psn_int_id

        LEFT JOIN TSM021_ENT_ADR eadr
            ON eadr.psn_int_id =
               pat.psn_int_id

           AND eadr.pri_fg =
               'Y'

        LEFT JOIN TSM020_ADDRESS padr
            ON padr.adr_int_id =
               eadr.adr_int_id

        LEFT JOIN TMR410_VISIT_DRG pdrg
            ON pdrg.vst_int_id =
               pv.vst_int_id

        LEFT JOIN TSM913_DRG_REF drgver
            ON drgver.drg_int_id =
               pdrg.drg_int_id

        LEFT JOIN TPM350_VISIT_GUARANTOR vguar
            ON vguar.vst_int_id =
               pv.vst_int_id

           AND vguar.guar_seq_no =
               4981

        LEFT JOIN TSM040_PERSON_HDR guar
            ON guar.psn_int_id =
               vguar.guar_int_id

        LEFT JOIN TSM021_ENT_ADR geadr
            ON geadr.psn_int_id =
               guar.psn_int_id

           AND geadr.pri_fg =
               'Y'

        LEFT JOIN TSM020_ADDRESS gadr
            ON gadr.adr_int_id =
               geadr.adr_int_id

        WHERE CAST(pv.vst_ext_id AS VARCHAR(50)) = ?
    """

    connection = get_remote_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            query,
            (visit_id,)
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

from models import RollModel


def create_tables(app, db):
    """Trigger the table creation"""
    db.create_all()


def truncate_tables(app, db):
    """Remove existing data from tables"""

    # Delete everything in the table
    RollModel.query.delete()

    # Reset the autoincrement counter on id
    db.session.execute("ALTER SEQUENCE roll_id_seq RESTART WITH 1;")


def add_1d_rolls(app, db, sides_list):
    """Add rolls like 1dx"""

    for side_count in sides_list:
        for pip_total in range(1,side_count+1):
            base_prob = 1/side_count
            r1_prob = 1/(side_count-1) if pip_total >1 else 0.0
            r2_prob = 1/(side_count-2) if pip_total >2 else 0.0
            ro1_prob = 1/side_count + 1/(side_count)**2 if pip_total > 1 else 1/(side_count)**2
            ro2_prob = 1/side_count + 2/(side_count)**2 if pip_total > 2 else 2/(side_count)**2
            base_roll = RollModel(
                dice_total=1,
                side_count=side_count,
                roll_type='base',
                ndx_text='1d{}'.format(side_count),
                pip_total=pip_total,
                base_prob=base_prob,
                r1_prob=r1_prob,
                r2_prob=r2_prob,
                ro1_prob=ro1_prob,
                ro2_prob=ro2_prob
            )
            db.session.add(base_roll)
            db.session.commit()


def add_base_rolls(app, db, sides_list, max_dice_total):
    """Add rolls like ndx (iterate thorugh the combinations)"""

    for side_count in sides_list:
        for dice_next in range(1, max_dice_total+1):
            sql = f"""
                WITH multi_roll AS (
                    SELECT
                    r1.dice_total + r2.dice_total AS dice_total
                    , r1.side_count
                    , 'base' AS roll_type
                    , (r1.dice_total + r2.dice_total)::TEXT || 'd' || r1.side_count::TEXT AS ndx_text
                    , r1.pip_total + r2.pip_total AS pip_total
                    , sum(r1.base_prob * r2.base_prob) AS base_prob
                    FROM ROLL AS r1
                    JOIN ROLL AS r2 ON 1=1
                    WHERE
                    r1.side_count = {side_count} AND r1.dice_total = 1 AND r1.roll_type = 'base'
                    AND r2.side_count = {side_count} AND r2.dice_total = {dice_next} AND r2.roll_type = 'base'
                    GROUP BY 1,2,3,4,5
                    ORDER BY 1,2,3,4,5
                )
                INSERT INTO ROLL (dice_total, side_count, roll_type, ndx_text, pip_total, base_prob)
                (SELECT dice_total, side_count, roll_type, ndx_text, pip_total, base_prob from multi_roll)
                ;
            """
            db.session.execute(sql)
            db.session.commit()


def add_r_rolls(app, db, sides_list, max_dice_total):
    """Add rolls for ndxr< , (roll all again) 1s and 2s only"""

    for side_count in sides_list:
        for rval in [1,2]:
            for dice_next in range(1, max_dice_total+1):
                sql = f"""
                    WITH calc_roll AS (
                        SELECT
                        r1.dice_total + r2.dice_total AS dice_total
                        , r1.side_count
                        , r1.pip_total + r2.pip_total AS pip_total
                        , sum(r1.r{rval}_prob * r2.r{rval}_prob) AS r{rval}_prob
                        FROM ROLL AS r1
                        JOIN ROLL AS r2 ON 1=1
                        WHERE
                        r1.side_count = {side_count} AND r1.dice_total = 1 AND r1.roll_type = 'base'
                        AND r2.side_count = {side_count} AND r2.dice_total = {dice_next} AND r2.roll_type = 'base'
                        GROUP BY 1,2,3
                        ORDER BY 1,2,3
                    )
                    UPDATE ROLL
                    SET r{rval}_prob = calc_roll.r{rval}_prob
                    FROM calc_roll
                    WHERE ROLL.dice_total = calc_roll.dice_total
                    AND ROLL.side_count = calc_roll.side_count
                    AND ROLL.pip_total = calc_roll.pip_total
                    ;
                """
                db.session.execute(sql)
                db.session.commit()


def add_ro_rolls(app, db, sides_list, max_dice_total):
    """Add rolls for ndxro< (roll again once only), 1s and 2s only"""

    for side_count in sides_list:
            for rval in [1,2]:

                for dice_next in range(1, max_dice_total+1):
                    sql = f"""
                        WITH calc_roll AS (
                            SELECT
                            r1.dice_total + r2.dice_total AS dice_total
                            , r1.side_count
                            , r1.pip_total + r2.pip_total AS pip_total
                            , sum(r1.ro{rval}_prob * r2.ro{rval}_prob) AS ro{rval}_prob
                            FROM ROLL AS r1
                            JOIN ROLL AS r2 ON 1=1
                            WHERE
                            r1.side_count = {side_count} AND r1.dice_total = 1 AND r1.roll_type = 'base'
                            AND r2.side_count = {side_count} AND r2.dice_total = {dice_next} AND r2.roll_type = 'base'
                            GROUP BY 1,2,3
                            ORDER BY 1,2,3
                        )

                        UPDATE ROLL
                        SET ro{rval}_prob = calc_roll.ro{rval}_prob
                        FROM calc_roll
                        WHERE ROLL.dice_total = calc_roll.dice_total
                        AND ROLL.side_count = calc_roll.side_count
                        AND ROLL.pip_total = calc_roll.pip_total
                        ;
                    """
                    db.session.execute(sql)
                    db.session.commit()


def add_kh_dl_rolls(app, db, sides_list):
    """Add rolls like ndxkh or ndxdl etc, 2 dice only. Also special case for 4d6 dl"""

    for side_count in sides_list:
        for kh_mod in ['kh', 'dl', 'kl', 'dh']:
            sql = f"""
                WITH calc_roll AS (
                    SELECT
                    2 AS dice_total
                    , r1.side_count
                    , '{kh_mod}' AS roll_type
                    , '2d' || r1.side_count::TEXT || '{kh_mod}' AS ndx_text
                    , CASE
                        WHEN '{kh_mod}' in ('kh', 'dl') THEN GREATEST(r1.pip_total, r2.pip_total)
                        WHEN '{kh_mod}' in ('kl', 'dh') THEN LEAST(r1.pip_total, r2.pip_total)
                    END AS pip_total
                    , sum(r1.base_prob * r2.base_prob) AS base_prob
                    FROM ROLL AS r1
                    JOIN ROLL AS r2 ON 1=1
                    WHERE
                    r1.side_count = {side_count} AND r1.dice_total = 1 AND r1.ndx_text = '1d{side_count}'
                    AND r2.side_count = {side_count} AND r2.dice_total = 1 AND r2.ndx_text = '1d{side_count}'
                    GROUP BY 1,2,3,4,5
                    ORDER BY 1,2,3,4,5
                )
                INSERT INTO ROLL (dice_total, side_count, roll_type, ndx_text, pip_total, base_prob)
                (SELECT dice_total, side_count, roll_type, ndx_text, pip_total, base_prob from calc_roll)
                ;
            """
            db.session.execute(sql)
            db.session.commit()


def add_4d6dl_roll(app, db):
    """Add specific entry for: 4d6 dl (5e starting stats rolls)"""

    sql = f"""
        WITH calc_roll AS (
            SELECT
            4 AS dice_total
            , 6 AS side_count
            , 'dl' AS roll_type
            , '4d6dl' AS ndx_text
            , r1.pip_total + r2.pip_total + r3.pip_total + r4.pip_total - LEAST(r1.pip_total, r2.pip_total) AS pip_total
            , sum(r1.base_prob * r2.base_prob * r3.base_prob * r4.base_prob) AS base_prob
            FROM ROLL AS r1
            JOIN ROLL AS r2 ON 1=1
            JOIN ROLL AS r3 ON 1=1
            JOIN ROLL AS r4 ON 1=1
            WHERE
            r1.side_count = 6 AND r1.dice_total = 1 AND r1.ndx_text = '1d6'
            AND r2.side_count = 6 AND r2.dice_total = 1 AND r2.ndx_text = '1d6'
            AND r3.side_count = 6 AND r3.dice_total = 1 AND r3.ndx_text = '1d6'
            AND r4.side_count = 6 AND r4.dice_total = 1 AND r4.ndx_text = '1d6'
            GROUP BY 1,2,3,4,5
            ORDER BY 1,2,3,4,5
        )
        INSERT INTO ROLL (dice_total, side_count, roll_type, ndx_text, pip_total, base_prob)
        (SELECT dice_total, side_count, roll_type, ndx_text, pip_total, base_prob from calc_roll)
        ;
    """
    db.session.execute(sql)
    db.session.commit()


def repopulate_roll_table(app, db, sides_list, max_dice_total):
    """Truncate tables and repopulate with data"""

    with app.app_context():

        truncate_tables(app, db)

        add_1d_rolls(app, db, sides_list)
        add_base_rolls(app, db, sides_list, max_dice_total)
        add_r_rolls(app, db, sides_list, max_dice_total)
        add_ro_rolls(app, db, sides_list, max_dice_total)
        add_kh_dl_rolls(app, db, sides_list)
        add_4d6dl_roll(app, db)

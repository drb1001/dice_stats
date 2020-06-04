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


def add_base_rolls(app, db, sides_list, max_dice_total):
    """Add rolls like ndx"""

    for side_count in sides_list:

        # Add for 1dx (initial set)
        for pip_total in range(1,side_count+1):
            base_roll = RollModel(
                dice_total=1,
                side_count=side_count,
                roll_type='base',
                ndx_text='1d{}'.format(side_count),
                pip_total=pip_total,
                probability=1/side_count
            )
            db.session.add(base_roll)
            db.session.commit()

        # Add for ndx (iterate thorugh the combinations)
        for dice_next in range(1, max_dice_total+1):
            sql1 = f"""
                WITH multi_roll AS (
                    SELECT
                    r1.dice_total + r2.dice_total AS dice_total
                    , r1.side_count
                    , 'base' AS roll_type
                    , (r1.dice_total + r2.dice_total)::TEXT || 'd' || r1.side_count::TEXT AS ndx_text
                    , r1.pip_total + r2.pip_total AS pip_total
                    , sum(r1.probability * r2.probability) AS probability
                    FROM ROLL AS r1
                    JOIN ROLL AS r2 ON 1=1
                    WHERE
                    r1.side_count = {side_count} AND r1.dice_total = 1 AND r1.roll_type = 'base'
                    AND r2.side_count = {side_count} AND r2.dice_total = {dice_next} AND r2.roll_type = 'base'
                    GROUP BY 1,2,3,4,5
                    ORDER BY 1,2,3,4,5
                )
                INSERT INTO ROLL (dice_total, side_count, roll_type, ndx_text, pip_total, probability)
                (SELECT dice_total, side_count, roll_type, ndx_text, pip_total, probability from multi_roll)
                ;
            """
            db.session.execute(sql1)
            db.session.commit()


def add_kh_dl_rolls(app, db, sides_list):
    """Add rolls like ndxkh or ndxdl etc, 2 dice only. Also special case for 4d6 dl"""

    for side_count in sides_list:
        for kh_mod in ['kh', 'dl', 'kl', 'dh']:
            sql1 = f"""
                WITH roll_2 AS (
                    SELECT
                    2 AS dice_total
                    , r1.side_count
                    , '{kh_mod}' AS roll_type
                    , '2d' || r1.side_count::TEXT || '{kh_mod}' AS ndx_text
                    , CASE
                        WHEN '{kh_mod}' in ('kh', 'dl') THEN GREATEST(r1.pip_total, r2.pip_total)
                        WHEN '{kh_mod}' in ('kl', 'dh') THEN LEAST(r1.pip_total, r2.pip_total)
                    END AS pip_total
                    , sum(r1.probability * r2.probability) AS probability
                    FROM ROLL AS r1
                    JOIN ROLL AS r2 ON 1=1
                    WHERE
                    r1.side_count = {side_count} AND r1.dice_total = 1 AND r1.roll_type = 'base'
                    AND r2.side_count = {side_count} AND r2.dice_total = 1 AND r2.roll_type = 'base'
                    GROUP BY 1,2,3,4,5
                    ORDER BY 1,2,3,4,5
                )
                INSERT INTO ROLL (dice_total, side_count, roll_type, ndx_text, pip_total, probability)
                (SELECT dice_total, side_count, roll_type, ndx_text, pip_total, probability from roll_2)
                ;
            """
            db.session.execute(sql1)
            db.session.commit()


def add_4d6dl_roll(app, db):
    """Add specific entry for: 4d6 dl (5e starting stats rolls)"""

    sql1 = f"""
        WITH roll_2 AS (
            SELECT
            4 AS dice_total
            , 6 AS side_count
            , 'dl' AS roll_type
            , '4d6dl' AS ndx_text
            , r1.pip_total + r2.pip_total + r3.pip_total + r4.pip_total - LEAST(r1.pip_total, r2.pip_total) AS pip_total
            , sum(r1.probability * r2.probability * r3.probability * r4.probability) AS probability
            FROM ROLL AS r1
            JOIN ROLL AS r2 ON 1=1
            JOIN ROLL AS r3 ON 1=1
            JOIN ROLL AS r4 ON 1=1
            WHERE
            r1.side_count = 6 AND r1.dice_total = 1 AND r1.roll_type = 'base'
            AND r2.side_count = 6 AND r2.dice_total = 1 AND r2.roll_type = 'base'
            AND r3.side_count = 6 AND r3.dice_total = 1 AND r3.roll_type = 'base'
            AND r4.side_count = 6 AND r4.dice_total = 1 AND r4.roll_type = 'base'
            GROUP BY 1,2,3,4,5
            ORDER BY 1,2,3,4,5
        )
        INSERT INTO ROLL (dice_total, side_count, roll_type, ndx_text, pip_total, probability)
        (SELECT dice_total, side_count, roll_type, ndx_text, pip_total, probability from roll_2)
        ;
    """
    db.session.execute(sql1)
    db.session.commit()


def add_r_rolls(app, db, sides_list, max_dice_total):
    """Add rolls for ndxr< , (roll all again) 1s and 2s only"""

    for side_count in sides_list:
        for rval in [1,2]:

            # Add for 1dxr< (initial set)
            for pip_total in range(rval+1, side_count+1):
                base_roll = RollModel(
                    dice_total=1,
                    side_count=side_count,
                    roll_type='r<{}'.format(rval),
                    ndx_text='1d{}r<{}'.format(side_count, rval),
                    pip_total=pip_total,
                    probability=1/(side_count-rval)
                )
                db.session.add(base_roll)
                db.session.commit()

            # Add for ndx (iterate thorugh the combinations)
            for dice_next in range(1, max_dice_total+1):
                sql1 = f"""
                    WITH multi_roll AS (
                        SELECT
                        r1.dice_total + r2.dice_total AS dice_total
                        , r1.side_count
                        , 'r<{rval}' AS roll_type
                        , (r1.dice_total + r2.dice_total)::TEXT || 'd' || r1.side_count::TEXT || 'r<{rval}' AS ndx_text
                        , r1.pip_total + r2.pip_total AS pip_total
                        , sum(r1.probability * r2.probability) AS probability
                        FROM ROLL AS r1
                        JOIN ROLL AS r2 ON 1=1
                        WHERE
                        r1.side_count = {side_count} AND r1.dice_total = 1 AND r1.roll_type = 'r<{rval}'
                        AND r2.side_count = {side_count} AND r2.dice_total = {dice_next} AND r2.roll_type = 'r<{rval}'
                        GROUP BY 1,2,3,4,5
                        ORDER BY 1,2,3,4,5
                    )
                    INSERT INTO ROLL (dice_total, side_count, roll_type, ndx_text, pip_total, probability)
                    (SELECT dice_total, side_count, roll_type, ndx_text, pip_total, probability from multi_roll)
                    ;
                """
                db.session.execute(sql1)
                db.session.commit()


def add_ro_rolls(app, db, sides_list, max_dice_total):
    """Add rolls for ndxro< (roll again once only), 1s and 2s only"""

    for side_count in sides_list:
            for rval in [1,2]:

                # Add for 1dxro< (initial set)
                sql1 = f"""
                    WITH multi_roll AS (
                        SELECT
                        1 AS dice_total
                        , r1.side_count
                        , 'ro<{rval}' AS roll_type
                        , '1d' || r1.side_count::TEXT || 'ro<{rval}' AS ndx_text
                        , CASE WHEN r1.pip_total <= {rval} THEN r2.pip_total ELSE r1.pip_total END AS pip_total
                        , sum(r1.probability * r2.probability) AS probability
                        FROM ROLL AS r1
                        JOIN ROLL AS r2 ON 1=1
                        WHERE
                        r1.side_count = {side_count} AND r1.dice_total = 1 AND r1.roll_type = 'base'
                        AND r2.side_count = {side_count} AND r2.dice_total = 1 AND r2.roll_type = 'base'
                        GROUP BY 1,2,3,4,5
                        ORDER BY 1,2,3,4,5
                    )
                    INSERT INTO ROLL (dice_total, side_count, roll_type, ndx_text, pip_total, probability)
                    (SELECT dice_total, side_count, roll_type, ndx_text, pip_total, probability from multi_roll)
                    ;
                """
                db.session.execute(sql1)
                db.session.commit()

                # Add for ndx (iterate thorugh the combinations)
                for dice_next in range(1, max_dice_total+1):
                    sql2 = f"""
                        WITH multi_roll AS (
                            SELECT
                            r1.dice_total + r2.dice_total AS dice_total
                            , r1.side_count
                            , 'ro<{rval}' AS roll_type
                            , (r1.dice_total + r2.dice_total)::TEXT || 'd' || r1.side_count::TEXT || 'ro<{rval}' AS ndx_text
                            , r1.pip_total + r2.pip_total AS pip_total
                            , sum(r1.probability * r2.probability) AS probability
                            FROM ROLL AS r1
                            JOIN ROLL AS r2 ON 1=1
                            WHERE
                            r1.side_count = {side_count} AND r1.dice_total = 1 and r1.roll_type = 'ro<{rval}'
                            AND r2.side_count = {side_count} AND r2.dice_total = {dice_next} and r2.roll_type = 'ro<{rval}'
                            GROUP BY 1,2,3,4,5
                            ORDER BY 1,2,3,4,5
                        )
                        INSERT INTO ROLL (dice_total, side_count, roll_type, ndx_text, pip_total, probability)
                        (SELECT dice_total, side_count, roll_type, ndx_text, pip_total, probability from multi_roll)
                        ;
                    """
                    db.session.execute(sql2)
                    db.session.commit()


def repopulate_roll_table(app, db, sides_list=[4,6,8,20], max_dice_total=10):
    """Truncate tables and repopulate with data"""

    with app.app_context():

        truncate_tables(app, db)

        add_base_rolls(app, db, sides_list, max_dice_total)
        add_kh_dl_rolls(app, db, sides_list)
        add_4d6dl_roll(app, db)
        add_r_rolls(app, db, sides_list, max_dice_total)
        add_ro_rolls(app, db, sides_list, max_dice_total)

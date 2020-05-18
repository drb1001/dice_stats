from models import RollModel, RollDetailModel


def create_tables(app, db):
    """ """
    db.create_all()


def repopulate_roll_table(app, db, max_dice_total=10):
    """ """

    with app.app_context():

        # Delete everything in the table
        RollModel.query.delete()

        # Reset the autoincrement counter on id
        db.session.execute("ALTER SEQUENCE roll_id_seq RESTART WITH 1;")

        for side_count in [2,3,4,6,8,10,12,20]:

            # Add for 1dx (initial set)
            for pip_total in range(1,side_count+1):
                base_roll = RollModel(
                    dice_total=1,
                    side_count=side_count,
                    ndx_text='1d{}'.format(side_count),
                    pip_total=pip_total,
                    probability=1/side_count
                )
                db.session.add(base_roll)
                db.session.commit()


            # Add for ndx (iterate thorugh the combinations)
            for dice_next in range(1, max_dice_total):
                sql1 = """
                    WITH multi_roll AS (
                        SELECT
                            r1.dice_total + r2.dice_total AS dice_total
                            , r1.side_count
                            , (r1.dice_total + r2.dice_total)::TEXT || 'd' || r1.side_count::TEXT AS ndx_text
                            , r1.pip_total + r2.pip_total AS pip_total
                            , sum(r1.probability * r2.probability) AS probability
                        FROM ROLL AS r1
                        JOIN ROLL AS r2 ON 1=1
                        WHERE
                            r1.side_count = {side_count} AND r1.dice_total = 1
                            AND r2.side_count = {side_count} AND r2.dice_total = {dice_next}
                        GROUP BY 1,2,3,4
                        ORDER BY 1,2,3,4
                    )
                    INSERT INTO ROLL (dice_total, side_count, ndx_text, pip_total, probability)
                    (SELECT dice_total, side_count, ndx_text, pip_total, probability from multi_roll)
                    ;
                """
                db.session.execute(sql1.format(**{'side_count':side_count, 'dice_next': dice_next}))
                db.session.commit()

            # Add kh/dl dice rolls (2 dice only)
            for kh_mod in ['kh', 'dl', 'kl', 'dh']:
                sql2 = """
                    WITH roll_2 AS (
                        SELECT
                            2 AS dice_total
                            , r1.side_count
                            , '2d' || r1.side_count::TEXT || '{kh_mod}' AS ndx_text
                            , CASE
                                WHEN '{kh_mod}' in ('kh', 'dl') THEN GREATEST(r1.pip_total, r2.pip_total)
                                WHEN '{kh_mod}' in ('kl', 'dh') THEN LEAST(r1.pip_total, r2.pip_total)
                            END AS pip_total
                            , sum(r1.probability * r2.probability) AS probability
                        FROM ROLL AS r1
                        JOIN ROLL AS r2 ON 1=1
                        WHERE
                            r1.side_count = {side_count} AND r1.dice_total = 1
                            AND r2.side_count = {side_count} AND r2.dice_total = 1
                        GROUP BY 1,2,3,4
                        ORDER BY 1,2,3,4
                    )
                    INSERT INTO ROLL (dice_total, side_count, ndx_text, pip_total, probability)
                    (SELECT dice_total, side_count, ndx_text, pip_total, probability from roll_2)
                    ;
                """
                db.session.execute(sql2.format(**{'side_count':side_count, 'kh_mod': kh_mod}))
                db.session.commit()

            # Add specific entry for: 4d6 dl (starting stats rolls)
            sql3 = """
                WITH roll_2 AS (
                    SELECT
                        4 AS dice_total
                        , 6 AS side_count
                        , '4d6dl' AS ndx_text
                        , r1.pip_total + r2.pip_total + r3.pip_total + r4.pip_total - LEAST(r1.pip_total, r2.pip_total) AS pip_total
                        , sum(r1.probability * r2.probability * r3.probability * r4.probability) AS probability
                    FROM ROLL AS r1
                    JOIN ROLL AS r2 ON 1=1
                    JOIN ROLL AS r3 ON 1=1
                    JOIN ROLL AS r4 ON 1=1
                    WHERE
                        r1.side_count = 6 AND r1.dice_total = 1
                        AND r2.side_count = 6 AND r2.dice_total = 1
                        AND r3.side_count = 6 AND r3.dice_total = 1
                        AND r4.side_count = 6 AND r4.dice_total = 1
                    GROUP BY 1,2,3,4
                    ORDER BY 1,2,3,4
                )
                INSERT INTO ROLL (dice_total, side_count, ndx_text, pip_total, probability)
                (SELECT dice_total, side_count, ndx_text, pip_total, probability from roll_2)
                ;
            """
            db.session.execute(sql3.format(**{'side_count':side_count, 'kh_mod': kh_mod}))
            db.session.commit()

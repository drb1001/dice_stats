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


        for side_count in [2,3,4,5,6,8,10,12,20]:

            # create initial set
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

            # iterate thorugh the combinations
            sql = """
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
            for dice_next in range(1, max_dice_total):
                db.session.execute(sql.format(**{'side_count':side_count, 'dice_next': dice_next}))
                db.session.commit()





def repopulate_roll_details_table(max_n):
    """"""
    pass

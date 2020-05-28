from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class RollModel(db.Model):
    __tablename__ = 'roll'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dice_total = db.Column(db.Integer, nullable=False)
    side_count = db.Column(db.Integer, nullable=False)
    roll_type = db.Column(db.String())
    ndx_text = db.Column(db.String())
    pip_total = db.Column(db.Integer)
    probability = db.Column(db.Numeric(12,10))

    def __init__(self, dice_total, side_count, roll_type, ndx_text, pip_total, probability):
        self.dice_total = dice_total
        self.side_count = side_count
        self.roll_type = roll_type
        self.ndx_text = ndx_text
        self.pip_total = pip_total
        self.probability = probability

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'dice_total': self.dice_total,
            'side_count': self.side_count,
            'roll_type': self.roll_type,
            'ndx_text': self.ndx_text,
            'pip_total': self.pip_total,
            'probability': self.probability
        }


# class RollDetailModel(db.Model):
#     __tablename__ = 'roll_detail'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     dice_total = db.Column(db.Integer, nullable=False)
#     side_count = db.Column(db.Integer, nullable=False)
#     ndx_text = db.Column(db.String())
#     pip_total = db.Column(db.Integer)
#     rolls = db.Column(db.String())
#     probability = db.Column(db.Numeric(12,10))
#
#     def __init__(self, dice_total, side_count, ndx_text, pip_total, combo_count):
#         self.dice_total = dice_total
#         self.side_count = side_count
#         self.ndx_text = ndx_text
#         self.pip_total = pip_total
#         self.rolls = rolls
#         self.combo_count = combo_count
#
#     def __repr__(self):
#         return '<id {}>'.format(self.id)
#
#     def serialize(self):
#         return {
#             'id': self.id,
#             'dice_total': self.dice_total,
#             'side_count': self.side_count,
#             'ndx_text': self.ndx_text,
#             'pip_total': self.pip_total,
#             'rolls': self.rolls,
#             'combo_count': self.combo_count
#         }

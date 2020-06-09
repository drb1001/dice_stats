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
    base_prob = db.Column(db.Numeric(12,10))
    r1_prob = db.Column(db.Numeric(12,10))
    r2_prob = db.Column(db.Numeric(12,10))
    ro1_prob = db.Column(db.Numeric(12,10))
    ro2_prob = db.Column(db.Numeric(12,10))

    def __init__(self, dice_total, side_count, roll_type, ndx_text, pip_total,
            base_prob, r1_prob, r2_prob, ro1_prob, ro2_prob):
        self.dice_total = dice_total
        self.side_count = side_count
        self.roll_type = roll_type
        self.ndx_text = ndx_text
        self.pip_total = pip_total
        self.base_prob = base_prob
        self.r1_prob = r1_prob
        self.r2_prob = r2_prob
        self.ro1_prob = ro1_prob
        self.ro2_prob = ro2_prob

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
            'base_prob': self.base_prob,
            'r1_prob': self.r1_prob,
            'r2_prob': self.r2_prob,
            'ro1_prob': self.ro1_prob,
            'ro2_prob': self.ro2_prob,
        }

    def get_r_data(self, r_mod, r_val):
        if r_mod == 'r<':
            if r_val == 1: return self.r1_prob
            elif r_val == 2: return self.r2_prob
        elif r_mod == 'ro<':
            if r_val == 1: return self.ro1_prob
            elif r_val == 2: return self.ro2_prob

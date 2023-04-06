from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from server.model.BaseTimeEntity import BaseTimeEntity

db = SQLAlchemy()


class FootPrintOcr(db.Model, BaseTimeEntity):
    __tablename__ = 'foot_print_ocr'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fat = db.Column(db.String(255))
    muscle = db.Column(db.String(255))
    weight = db.Column(db.String(255))

    # Getter 기능 구현
    def to_dict(self):
        return {
            'id': self.id,
            'fat': self.fat,
            'muscle': self.muscle,
            'weight': self.weight,
            'insert_time': self.insert_time,
            'update_time': self.update_time
        }
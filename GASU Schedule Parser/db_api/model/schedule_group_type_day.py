from typing import List
import sqlalchemy as sa
from gino import Gino

db = Gino()

class ScheduleGroupTypeDay(db.Model):
    __tablename__ = 'schedule_group_type_day'
    group_name_with_type_and_day = db.Column(db.String(40), primary_key=True)
    academic_degree = db.Column(db.String(30))
    faculty = db.Column(db.String(100))
    year = db.Column(db.Integer())
    group_name = db.Column(db.String(25))
    week_type = db.Column(db.String(15))
    day_of_week = db.Column(db.String(15))
    first_lecture_time = db.Column(db.String(15))
    first_lecture = db.Column(db.String(255))
    second_lecture_time = db.Column(db.String(15))
    second_lecture = db.Column(db.String(255))
    third_lecture_time = db.Column(db.String(15))
    third_lecture = db.Column(db.String(255))
    fourth_lecture_time = db.Column(db.String(15))
    fourth_lecture = db.Column(db.String(255))
    fifth_lecture_time = db.Column(db.String(15))
    fifth_lecture = db.Column(db.String(255))
    sixth_lecture_time = db.Column(db.String(15))
    sixth_lecture = db.Column(db.String(255))
    seventh_lecture_time = db.Column(db.String(15))
    seventh_lecture = db.Column(db.String(255))

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"
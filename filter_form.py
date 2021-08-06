from flask_wtf import FlaskForm
from wtforms import SelectField


class ThesisFilter(FlaskForm):
    levels = SelectField('levels', choices=[])
    supervisor = SelectField('supervisor', choices=[])
    department = SelectField('department', choices=[])
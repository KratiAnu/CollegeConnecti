from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

# ...

class EditProfileForm(FlaskForm):
    first_name = StringField('Username', validators=[DataRequired()])
    about = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
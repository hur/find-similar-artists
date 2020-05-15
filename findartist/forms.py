from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, URL, InputRequired


class ArtistForm(FlaskForm):
    artist = StringField('artist', validators=[InputRequired()],
                         render_kw={'placeholder': 'Enter artist name',
                                    'onfocus': 'this.placeholder = ""',
                                    'onblur': 'this.placeholder = "Enter artist name"'})

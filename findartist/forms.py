from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, URL, InputRequired


class ArtistForm(FlaskForm):
    """ A form to submit an artist name """
    artist = StringField('artist', validators=[InputRequired()],
                         render_kw={'placeholder': 'Enter artist name',
                                    'onfocus': 'this.placeholder = ""',
                                    'onblur': 'this.placeholder = "Enter artist name"'})
    use_musicmap = BooleanField('use_musicmap', render_kw={'value': False})

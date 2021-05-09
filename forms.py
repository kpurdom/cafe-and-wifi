from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, URL


SEAT_OPTIONS = ["0-10", "10-20", "20-30", "30-40", "40-50", "50+"]


##WTForm
class CreateCafeForm(FlaskForm):
    name = StringField("Cafe Name:", validators=[DataRequired()])
    location = StringField("Location:", validators=[DataRequired()])
    img_url = StringField("Cafe Image URL:", validators=[DataRequired(), URL()])
    map_url = StringField("Google Map URL:", validators=[DataRequired(), URL()])
    seats = SelectField("No. Seats:", choices=SEAT_OPTIONS, validators=[DataRequired()])
    coffee_price = FloatField("Coffee Price (e.g. enter '2.80' for '£2.80'):", validators=[DataRequired()])
    has_sockets = BooleanField("Access to sockets")
    has_toilet = BooleanField("Toilets")
    has_wifi = BooleanField("WiFi access")
    can_take_calls = BooleanField("Can take calls")
    submit = SubmitField("Submit New Cafe")

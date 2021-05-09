from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import CreateCafeForm
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
POSITION_STACK_API = os.environ.get("POSITION_STACK_API")
POSITION_STACK_URL = 'http://api.positionstack.com/v1/forward'
Bootstrap(app)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///cafes.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class CafesList(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean)
    has_toilet = db.Column(db.Boolean)
    has_wifi = db.Column(db.Boolean)
    can_take_calls = db.Column(db.Boolean)
    seats = db.Column(db.String(100), nullable=False)
    coffee_price = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float(10), nullable=False)
    longitude = db.Column(db.Float(10), nullable=False)


db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/cafes')
def show_cafes():
    cafes_list = CafesList.query.all()
    return render_template("cafes.html", all_cafes=cafes_list)


@app.route("/cafes/<int:cafe_id>", methods=["GET", "POST"])
def show_cafe_detail(cafe_id):
    requested_cafe = CafesList.query.get(cafe_id)
    return render_template("cafe_detail.html", cafe=requested_cafe)


@app.route("/new-cafe", methods=["GET", "POST"])
def add_new_cafe():
    form = CreateCafeForm()
    if form.validate_on_submit():
        parameters = {'access_key': POSITION_STACK_API,
                      'query': f'{form.name.data} {form.location.data}',
                      }
        response = requests.get(url=POSITION_STACK_URL, params=parameters)

        try:
            response.raise_for_status()
            data = response.json()['data'][0]
            print(data)
            latitude = data['latitude']
            longitude = data['longitude']
        except (IndexError, TypeError):
            latitude = 0
            longitude = 0

        new_cafe = CafesList(
            name=form.name.data,
            location=form.location.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=f"£{format(form.coffee_price.data,'.2f')}",
            latitude=latitude,
            longitude=longitude,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("show_cafes"))

    return render_template("add-cafe.html", form=form)


@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = CafesList.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('show_cafes'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)



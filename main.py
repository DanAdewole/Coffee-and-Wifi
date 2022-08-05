from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(
        'Cafe name',
        validators=[
            DataRequired(),
        ]
    )
    location_url = URLField(
        'Cafe Location on Google Maps(URL)',
        validators=[
            DataRequired(),
            URL(require_tld=True, message="Invalid URL")
        ]
    )
    open_time = StringField(
        'Opening Time e.g. 8AM',
        validators=[
            DataRequired(),
        ]
    )
    closing_time = StringField(
        'Closing Time e.g. 4PM',
        validators=[
            DataRequired(),
        ]
    )
    coffee_rating = SelectField(
        'Coffee Rating',
        choices=['☕️','☕️☕️','☕️☕️☕️','☕️☕️☕️☕️','☕️☕️☕️☕️☕️'],
        coerce=str,
        validators=[DataRequired()],
    )
    wifi_strength = SelectField(
        'WiFi Strength Rating',
        choices=['✘','💪','💪💪','💪💪💪','💪💪💪💪','💪💪💪💪💪'],
        coerce=str,
        validators=[DataRequired()],
    )
    power_socket = SelectField(
        'Power Socket Availability',
        choices=['✘','🔌','🔌🔌','🔌🔌🔌','🔌🔌🔌🔌','🔌🔌🔌🔌🔌'],
        coerce=str,
        validators=[DataRequired()],
    )
    submit = SubmitField(label='Submit')



@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_name = form.cafe.data
        location = form.location_url.data
        open_time = form.open_time.data
        close_time = form.closing_time.data
        coffee_rating = form.coffee_rating.data
        wifi_strength = form.wifi_strength.data
        power_socket = form.power_socket.data
        info_list = [cafe_name, location, open_time, close_time, coffee_rating, wifi_strength, power_socket]
        with open('cafe-data.csv', 'a', newline='',encoding='utf8') as csv_file:
            csv_data = csv.writer(csv_file)
            csv_data.writerow(info_list)
        return redirect('cafes')
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)

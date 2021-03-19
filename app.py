from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, RadioField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class Config():
    SECRET_KEY = 'n983U#!*TPiu'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bets.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
endtime = datetime(2021, 3, 26, 23)


@app.route('/', methods=['GET', 'POST'])
def root():
    form = BetForm()
    if form.validate_on_submit() and datetime.now() < endtime:
        bet = Bet(name=form.name.data, choice=form.choice.data, bet=form.bet.data)
        db.session.add(bet)
        db.session.commit()
        return redirect(url_for('root'))
    rows = Bet.query.all()
    return render_template('root.html', form=form, rows=rows, endtime=endtime)


class BetForm(FlaskForm):
    name = StringField('Naam', validators=[DataRequired()])
    choice = RadioField('Keuze', validators=[DataRequired()], choices=[
        ('Ayla', 'Ayla'), ('Joyce', 'Joyce')])
    bet = DecimalField('Inzet', validators=[DataRequired()])
    submit = SubmitField('Bevestig')


class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    choice = db.Column(db.String, nullable=False)
    bet = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now().replace(microsecond=0))


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')

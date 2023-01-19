from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired

from game_of_life import GameOfLife

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key-for-forms'


class InitWorldForm(FlaskForm):
    width = IntegerField(('Введите ширину'), validators=[DataRequired()])
    height = IntegerField(('Введите высоту'), validators=[DataRequired()])
    submit = SubmitField(('Создать жизнь'))


@app.route('/', methods=['GET', 'POST'])
def index():
    init_form = InitWorldForm()
    if init_form.validate_on_submit() and init_form.submit.data:
        GameOfLife(int(init_form.width.data), int(init_form.height.data))
        return redirect(url_for('live'))
    return render_template("index.html", form=init_form)


@app.route('/live')
def live():
    current_game = GameOfLife()
    if current_game.counter > 0:
        current_game.form_new_generation()
    current_game.counter += 1
    return render_template("live.html", current_game=current_game)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

import os

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Email


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                u"Error in the %s field - %s"
                % (getattr(form, field).label.text, error),
                "error",
            )


class WishForm(FlaskForm):
    name = StringField("name")
    email = StringField("email", validators=[DataRequired(), Email()])
    message = TextAreaField("message", validators=[DataRequired()])


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def home():
    form = WishForm()
    if request.method == "POST":

        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            message = form.message.data

            flash("Posted message:")
            flash(name)
            flash(email)
            flash(message)
            return redirect(url_for("home", _external=True, _scheme='https'))
        else:
            flash_errors(form)
            return redirect(url_for("home", _external=True, _scheme='https'))
    return render_template("home.html", form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008, debug=True, ssl_context='adhoc')

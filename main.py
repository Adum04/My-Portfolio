from flask import Flask, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Regexp
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os


app = Flask("__name__")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app)
app.secret_key = os.getenv("SECRET_KEY")

load_dotenv()


class MyForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    phone = StringField(
        "Phone",
        validators=[
            DataRequired(),
            Regexp(r"^\+?1?\d{9,15}$", message="Enter a valid phone number."),
        ],
    )
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send me an Owl")


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/aboutMe")
def aboutme():
    return render_template("aboutme.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    name = None
    email = None
    phone = None
    message = None
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data

        try:
            send_email_to_user(email, name)
            send_email_to_yourself(name, email, phone, message)

        except Exception as e:
            return "Nothing"

        form.name.data = ""
        form.email.data = ""
        form.phone.data = ""
        form.message.data = ""
        return render_template(
            "contactme.html",
            name=name,
            email=email,
            phone=phone,
            message=message,
            form=form,
        )
    return render_template("contactme.html", form=form)


def send_email_to_user(user_email, user_name):
    msg = Message(
        "Thank You for Contacting Us",
        sender="adum0407@gmail.com",
        recipients=[user_email],
    )  # User's email address
    msg.body = f"Hello {user_name},\nThank you for reaching out! We have received your message and will get back to you shortly."
    mail.send(msg)


def send_email_to_yourself(name, email, phone, message):
    msg = Message(
        "New Contact Form Submission",
        sender="adum0407@gmail.com",
        recipients=["adum0407@gmail.com"],
    )  # Your email address
    msg.body = (
        f"New message from {name}:\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    )
    mail.send(msg)


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/skills")
def skills():
    return render_template("skills.html")


@app.route("/certifications")
def certifications():
    return render_template("certifications.html")


if __name__ == "__main__":
    app.run()

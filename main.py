from flask import Flask, render_template, request, redirect, url_for, flash
from forms import ContactForm
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from projects import PROJECTS
from resume import RESUME_DATA
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from threading import Thread
import smtplib
import os

load_dotenv()
EMAIL=os.environ.get("email")
PASSWORD=os.environ.get("password")
current_year = datetime.now().year


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["secret_key"]
Bootstrap5(app)

# SendGrid credentials
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_TO = os.getenv("MAIL_TO")

# Async SendGrid email sender
def send_async_email(app, message):
    with app.app_context():
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            print(f"Email sent! Status code: {response.status_code}")
        except Exception as e:
            print(f"SendGrid email error: {e}")


# Home page
@app.route("/")
def home():
    return render_template("index.html", year=current_year)

# Contact page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        phone=form.mobile.data
        msg=form.msg.data

        try:
            message = Mail(
                from_email=MAIL_FROM,
                to_emails=MAIL_TO,
                subject=f"New Message from {name}",
                plain_text_content=f"From: {name}\nEmail: {email}\n\nMessage:\n{msg}"
            )

            Thread(target=send_async_email, args=(app, message)).start()

            flash("Message sent successfully! ✅", "success")
            return redirect(url_for("contact"))

        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for("contact"))

    return render_template("contact.html", form=form, year=current_year)

# Project page
@app.route("/projects")
def projects():
    return render_template("projects.html", projects=PROJECTS, year=current_year)

# Resume page
@app.route("/resume")
def resume():
    return render_template("resume.html", resume=RESUME_DATA, year=current_year)

if __name__ == "__main__":
    app.run(debug=True)
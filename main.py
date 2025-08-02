from flask import Flask, render_template, request, redirect, url_for, flash
from forms import ContactForm
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from projects import PROJECTS
from resume import RESUME_DATA
from datetime import datetime
import smtplib
import os

load_dotenv()
EMAIL=os.environ.get("email")
PASSWORD=os.environ.get("password")
current_year = datetime.now().year


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["secret_key"]
Bootstrap5(app)


@app.route("/")
def home():
    return render_template("index.html", year=current_year)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        phone=form.mobile.data
        msg=form.msg.data
        with smtplib.SMTP_SSL("smtp.gmail.com", port=465) as connection:
            connection.login(EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL,
                                to_addrs=EMAIL,
                                msg=f"Subject: New message from {name}\n\nFrom: {name}\nEmail: {email}\nPhone_no: {phone}\nMessage:{msg}")
            flash("Message sent successfully!")
            return redirect(url_for('contact'))
    return render_template("contact.html", form=form, year=current_year)


@app.route("/projects")
def projects():
    return render_template("projects.html", projects=PROJECTS, year=current_year)

@app.route("/resume")
def resume():
    return render_template("resume.html", resume=RESUME_DATA, year=current_year)

if __name__ == "__main__":
    app.run(debug=False)
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import smtplib
import os
from dotenv import load_dotenv

load_dotenv(".env")
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap(app)

my_email = os.getenv("CONTACT_EMAIL")
password = os.getenv("CONTACT_EMAIL_PASSWORD")  # Note that this is the app password for the gmail account
send_address = my_email


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/contact', methods=["GET"])
def contact():
    if request.method == 'GET':
        submit_success = None
        return render_template('contact.html', submit_success=submit_success)


def send_message_via_email(form_data: dict) -> bool:
    try:
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=send_address,
                                msg=f"Subject:New Blog Site Message\n\nName: {form_data['name']}"
                                    f"\nEmail: {form_data['email']}"
                                    f"\nPhone Number: {form_data['phone']}"
                                    f"\nMessage:\n\t{form_data['message']}")
        return True
    except smtplib.SMTPException:
        return False


def is_valid_message(form_data):
    if len(form_data['name']) > 0 and len(form_data['email']) > 0 \
            and len(form_data['message']) > 0:
        return True
    return False


@app.route('/contact', methods=["POST"])
def send_message():
    if request.method == 'POST':
        form_data = {
            "name": request.form['name'],
            "email": request.form['email'],
            "phone": request.form['phone'],
            "message": request.form['message'],
        }
        if is_valid_message(form_data):
            submit_success = send_message_via_email(form_data)
            return render_template('contact.html', submit_success=submit_success)
        return render_template('contact.html', submit_success=False)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

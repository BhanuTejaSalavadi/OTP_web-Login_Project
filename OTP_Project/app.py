from flask import Flask, render_template, request
import random
import smtplib
import time

app = Flask(__name__)

# Store OTP + timestamp
otp_store = {}

# 📩 Send Email Function (Gmail SMTP)
def send_email(to_email, otp):
    sender_email = "23wj1a6276@gniindia.org"       # 🔁 replace with your Gmail
    app_password = "ynzu chcx dvjv riox" # 🔁 replace with App Password

    subject = "OTP Login"
    body = f"Your OTP is {otp}. It is valid for 60 seconds."

    message = f"Subject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, to_email, message)
        server.quit()
        print("✅ Email sent successfully to", to_email)
    except Exception as e:
        print("❌ Error sending email:", e)


# 🏠 Home Page
@app.route('/')
def home():
    return render_template("email.html")


# 🔐 Generate OTP (for ANY email)
@app.route('/send_otp', methods=['POST'])
def send_otp():
    email = request.form['email']

    otp = str(random.randint(100000, 999999))

    # Store OTP + time
    otp_store[email] = {
        "otp": otp,
        "time": time.time()
    }

    print("Email:", email)
    print("Generated OTP:", otp)

    send_email(email, otp)

    return render_template("verify.html", email=email)


# ✅ Verify OTP
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    email = request.form['email']
    user_otp = request.form['otp']

    data = otp_store.get(email)

    if data:
        # ⏱ Expiry check (60 seconds)
        if time.time() - data["time"] > 60:
            return "OTP Expired ❌"

        if data["otp"] == user_otp:
            return "Login Successful ✅"

    return "Invalid OTP ❌"


# 🚀 Run App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
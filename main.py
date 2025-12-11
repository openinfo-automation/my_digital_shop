from flask import Flask, render_template, send_file, redirect, url_for, request
import stripe
import os

app = Flask(**name**)

# Stripe setup

stripe.api_key = os.environ.get(“STRIPE_SECRET_KEY”)

@app.route(”/”)
def index():
return render_template(“index.html”)

@app.route(”/create-checkout-session”, methods=[“POST”])
def create_checkout_session():
try:
session = stripe.checkout.Session.create(
payment_method_types=[“card”],
line_items=[{
“price_data”: {
“currency”: “usd”,
“product_data”: {
“name”: “AI Monster Brains - 30 Unique Designs”,
“description”: “Instant PDF download with 30 high-resolution monster brain illustrations”,
},
“unit_amount”: 500,  # $5.00 in cents
},
“quantity”: 1,
}],
mode=“payment”,
success_url=url_for(“success”, _external=True),
cancel_url=url_for(“index”, _external=True),
)
return redirect(session.url, code=303)
except Exception as e:
return str(e), 500

@app.route(”/success”)
def success():
return render_template(“success.html”)

@app.route(”/download”)
def download():
return send_file(
“static/AI_Monster_Brains.pdf”,
as_attachment=True,
download_name=“AI_Monster_Brains.pdf”,
mimetype=“application/pdf”
)

if **name** == “**main**”:
app.run(host=“0.0.0.0”, port=5000)

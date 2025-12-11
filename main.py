from flask import Flask, render_template, send_file, redirect, url_for
import stripe
import os

app = Flask(__name__)

# Stripe setup
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")  # Set this in Render Environment

# Landing page
@app.route("/")
def index():
    return render_template("index.html")  # Your main page with product info and Buy button

# Stripe checkout session
@app.route("/buy")
def buy():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "AI Monster Brains PDF",
                },
                "unit_amount": 500,  # $5.00 in cents
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=url_for("success", _external=True),
        cancel_url=url_for("index", _external=True),
    )
    return redirect(session.url, code=303)

# Success page
@app.route("/success")
def success():
    return render_template("success.html")  # Thank you page with download link

# Download PDF
@app.route("/download")
def download():
    return send_file(
        "static/AI_Monster_Brains.pdf",
        as_attachment=True,
        download_name="AI_Monster_Brains.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)

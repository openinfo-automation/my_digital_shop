import os
import stripe
from flask import Flask, render_template, redirect, send_from_directory, url_for

app = Flask(__name__)

# Stripe secret key from environment variable
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "AI Productivity Cheat Sheet"},
                "unit_amount": 500,  # $5 in cents
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="https://my-digital-shop.onrender.com/success",
        cancel_url="https://my-digital-shop.onrender.com/",
    )
    return redirect(session.url, code=303)

@app.route("/success")
def success():
    # Show thank-you page and trigger PDF download automatically
    return render_template("success.html")

@app.route("/download")
def download():
    # Serve the PDF file for download
    return send_from_directory('static', 'product.pdf', as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

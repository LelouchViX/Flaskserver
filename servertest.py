from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import stripe

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Serve static index.html
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Stripe keys (replace with your own)
stripe.api_key = "sk_test_51QUN2JJCvP46CUpY2VuiPJJv5nwR85aSPlD1Xspdw7Ad393I5lQfEbdzuHDGVVFIZ8puHzyxru586tzt4f3ZY0ig00nZWieNbp"  # Replace with your secret key

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Test Product',
                    },
                    'unit_amount': 2000,  # Amount in cents ($20.00)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:5000/success?session_id={CHECKOUT_SESSION_ID}',  # Replace with your URL
            cancel_url='http://127.0.0.1:5000/cancel',  # Replace with your URL
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/success')
def success():
    session_id = request.args.get('session_id')
    if not session_id:
        return "<h1>Missing session ID</h1>", 400

    try:
        # Retrieve the session from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == "paid":
            # Trigger your ESP32 motor logic here
            print("Payment successful! You can now run your ESP32 motor.")
            return "<h1>Payment Successful! ESP32 logic triggered.</h1>"
        else:
            return "<h1>Payment not successful.</h1>", 400
    except Exception as e:
        return f"<h1>Error: {e}</h1>", 500

@app.route('/cancel')
def cancel():
    return "<h1>Payment Cancelled</h1>"

if __name__ == '__main__':
    app.run(port=5000)

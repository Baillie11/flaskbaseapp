# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from flask import Blueprint, redirect, render_template, request, url_for, current_app
from flask_login import current_user, login_required
import stripe
from app import db

main_blueprint = Blueprint('main', __name__, template_folder='templates')

# Public home page
@main_blueprint.route('/')
def home_page():
    return render_template('main/home_page.html')

# Member-only page
@main_blueprint.route('/member')
@login_required
def member_page():
    return render_template('main/user_page.html')

# Subscription route (Stripe)
@main_blueprint.route('/subscribe')
@login_required
def subscribe():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Premium Membership',
                },
                'unit_amount': 1000,  # $10.00 USD
                'recurring': {'interval': 'month'},
            },
            'quantity': 1,
        }],
        success_url=url_for('main.subscription_success', _external=True),
        cancel_url=url_for('main.subscription_cancelled', _external=True),
    )

    return redirect(session.url, code=303)

@main_blueprint.route('/subscription-success')
@login_required
def subscription_success():
    return render_template('main/subscription_success.html')

@main_blueprint.route('/subscription-cancelled')
@login_required
def subscription_cancelled():
    return render_template('main/subscription_cancelled.html')
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template, request, url_for, current_app

from flask_user import current_user, login_required, roles_required
import stripe



from app import db
from app.models.user_models import UserProfileForm

main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return render_template('main/home_page.html')


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('main/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('main/admin_page.html')


@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form)
    
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




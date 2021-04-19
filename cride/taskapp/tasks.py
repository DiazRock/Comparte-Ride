""" Celery task """

# Django 
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


# Models
from cride.users.models import User
from cride.rides.models import Ride


# Utilities
import jwt
from datetime import timedelta

# Serializers
from cride.users.serializers.profile import ProfileModelSerializer

# Celery
from celery.decorators import task, periodic_task

def gen_verification_token(user):
    """ Create JWT token that the user can use to verify its account """
    exp_date = timezone.now() + timedelta(days= 3)
    payload = {
        'user': user.username,
        'exp': int (exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm= 'HS256')
    return token


@task(name= 'send_confirmation_email', max_retries = 3)
def send_confirmation_email(user_pk):
    """ Send account verification link to given user """
    user = User.objects.get(pk= user_pk)
    verifiaction_token = gen_verification_token(user)
    print("Sending email")
    subject = 'Wellcome @{}! Verfiy your account to start using Comparte Ride'.format(user.username)
    from_email = 'Comparte Ride <noreply@comparteride.com>'
    text_content = render_to_string('emails/users/account_verification.html',
                                    {'token': verifiaction_token, 
                                        'user': user})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
    msg.attach_alternative(text_content, 'text/html')
    msg.send()
    

@periodic_task(name='disable_finished_rides', run_every=timedelta(minutes=20))
def disable_finished_rides():
    """Disable finished rides."""
    now = timezone.now()
    offset = now + timedelta(minutes=20)

    # Update rides that have already finished
    rides = Ride.objects.filter(
        arrival_date__gte=now,
        arrival_date__lte=offset,
        is_active=True
    )
    rides.update(is_active=False)    
    
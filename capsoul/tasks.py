import logging
 
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from capsoul.celery import app
 
@app.task
def send_welcome_email(username):
    User = get_user_model()
    user = User.objects.filter(username=username).values('email')
    logging.warning("got user '%s'" % username)
    send_mail(
        'Welcome to CapSoul!',
        'Welcome to CapSoul!',
        'eric.marcondes@wallawalla.edu',
        [user]
    )
    logging.warning("sent email to '%s'" % username)
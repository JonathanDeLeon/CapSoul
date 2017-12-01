import logging
 
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from capsoul.celery import app
 
@app.task
def send_welcome_email(uname):
    User = get_user_model()
    try:
        user = User.objects.all()
        for u in user:
            logging.warning("INFO: '%s'" % u.email + '%s' % u.username)
            
        send_mail(
            'Welcome to CapSoul!',
            'Welcome to CapSoul!',
            'eric.marcondes@wallawalla.edu',
            [user.email]
        )
        logging.warning("sent email to '%s'" % uname)
    except User.DoesNotExist:
        user = None
    logging.warning("got user: '%s'" % user)

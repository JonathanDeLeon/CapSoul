import logging
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from capsoul.celery import app

@app.task
def send_welcome_email(email):
    logging.info("User Email: %s" % email)
    send_mail(
        'Welcome to CapSoul!',
        'Welcome to CapSoul!',
        'wwu.capsoul@gmail.com',
        [email]
        )
    logging.info("Welcome email sent to: '%s'" % email)

@app.task
def send_capsule_created_email(email):
    send_mail(
        'A Capsule has been created!',
        'Login to your CapSoul account and checkout the recently created capsule!',
        'wwu.capsoul@gmail.com',
        [email]
    )
    print("New capsule email sent to: '%s' " % email)

@app.task
def send_capsule_unlocked_email(email):
    send_mail(
        'Your Capsule has unlocked!',
        'Login to your CapSoul account and checkout the recently unlocked capsule!',
        'wwu.capsoul@gmail.com',
        [email]
    )
    print("Unlocked capsule email sent to: '%s' " % email)

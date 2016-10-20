#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.core.mail import EmailMessage
from django.utils.translation import ugettext as _
from django.core.management import call_command

# from celery import shared_task
from project.celery import app


@app.task
def send_initial_password_mail(user, password):
    """
    task sending out email with new passwword via mandrill
    """

    msg = EmailMessage(
        subject=_('Welcome to Das Aktienregister - Your new password'),
        from_email="no-reply@das-aktienregister.ch",
        to=[user.email]
    )
    msg.template_name = "DARG_WELCOME_PASSWORD"
    msg.template_content = {}
    msg.global_merge_vars = {
        'NEW_PASSWORD': password,
    }
    msg.merge_vars = {}
    msg.send()


@app.task
def backup_app_db():
    """
    calls django-dbbackup's management commands to backup app's database
    """
    call_command('dbbackup', **{'encrypt': True})

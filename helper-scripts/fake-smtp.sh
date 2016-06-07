#!/bin/bash
# From: http://docs.djangoproject.com/en/dev/topics/email/
# The easiest way to test your project's use of e-mail is to use a "dumb"
# e-mail server that receives the e-mails locally and displays them to the
# terminal, but does not actually send anything. Python has a built-in way to
# accomplish this with a single command:

python -m smtpd -n -c DebuggingServer localhost:1025

# This command will start a simple SMTP server listening on port 1025 of
# localhost. This server simply prints to standard output all email headers
# and the email body. You then only need to set the EMAIL_HOST and EMAIL_PORT
# accordingly, and you are set.

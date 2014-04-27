from flask import Flask, render_template, request, abort, redirect
from flask.ext.mail import Message, Mail
from forms import ContactForm
from wsgi import ReverseProxied
from ConfigParser import RawConfigParser
import os
import re

CONFIG_ENV = 'CONTACT_POTION_CONFIG'

config_filename = os.getenv(CONFIG_ENV, 'sample.config')
config = RawConfigParser()
config.read(config_filename)

app = Flask(__name__)
app.secret_key = config.get('GLOBAL', 'secret_key')
app.config['MAIL_SERVER'] = config.get('GLOBAL', 'mailserver')
app.config['MAIL_PORT'] = config.getint('GLOBAL', 'mailport')
app.config['MAIL_USE_SSL'] = config.getboolean('GLOBAL', 'mailusessl')

mail = Mail()
mail.init_app(app)

app.wsgi_app = ReverseProxied(app.wsgi_app)

@app.route('/', methods=['GET', 'POST'])
def contact():
    request_config = get_request_config()
    form = ContactForm()
    form.category.choices = ((choice, choice)
                             for choice in request_config['categories'])
    if request.method == 'POST':
        if form.validate():
            send_message(form, request_config)
            return redirect(request_config['success_url'])
    return render_template('contact.html',
                           skin=request_config['skin'],
                           form=form)


def send_message(form, request_config):
    subject = "[{0}] {1}".format(form.category.data, form.subject.data)
    subject = re.sub(r'\s+', ' ', subject)
    message = Message(subject,
                      sender=request_config['sender'],
                      recipients=request_config['recipients'])
    message.body = """
    Website contact message from {0} ({1}):

    {2}""".format(form.name.data, form.email.data, form.message.data)
    mail.send(message)


def get_request_config():
    required_options = ['categories', 'recipients', 'sender', 'success_url']
    host = re.sub(r':', '_', request.headers['Host'])
    if not config.has_option('HOSTS', host): abort(404)
    config_section = config.get('HOSTS', host)

    if not all(config.has_option(config_section, option)
            for option in required_options):
        abort(404)

    request_config = {key: config.get(config_section, key)
                      for key in required_options}
    request_config['skin'] = 'skin_{0}.html'.format(config_section)
    request_config['categories'] = re.split(r';\s*',
                                            request_config['categories'])
    request_config['recipients'] = re.split(r',\s*',
                                            request_config['recipients'])
    return request_config


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

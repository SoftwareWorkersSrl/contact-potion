from flask import Flask, render_template, request
from flask.ext.mail import Message, Mail
from forms import ContactForm
from ConfigParser import RawConfigParser

import os

MAGIC_HEADER = 'X-Contact-Potion-Config'
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

@app.route('/', methods=['GET', 'POST'])
def contact():
    config_section = 'default'
    skin = 'skin_development.html'
    form = ContactForm()
    form.category.choices = [('1', 'one'), (2, 'two')]
    print(form.category.choices)
    if request.method == 'POST':
        if form.validate():
            send_message(form)
            return 'Message sent'
    return render_template('contact.html', skin=skin, form=form)


def send_message(form, app):
    message = Message(form.subject.data,
                      sender=app.config['MAIL_SENDER'],
                      recipients=['mike@bloy.org'])
    message.body = """
    Website contact message from {0} ({1}):

    {2}""".format(form.name.data, form.email.data, form.message.data)
    mail.send(message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

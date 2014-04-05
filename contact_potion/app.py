from flask import Flask, render_template, request
from flask.ext.mail import Message, Mail
from forms import ContactForm


app = Flask(__name__)
app.secret_key = "Development Secret Key"
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_RECIPIENT'] = 'test@example.com'
app.config['MAIL_SENDER'] = 'webmaster@example.com'

mail = Mail()
mail.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def contact():
    skin = 'skin_development.html'
    form = ContactForm()
    form.category.choices = [('1', 'one'), (2, 'two')]
    print(form.category.choices)
    if request.method == 'POST':
        if form.validate():
            send_message(form)
            return 'Message sent'
    return render_template('contact.html', skin=skin, form=form)


def send_message(form):
    message = Message(form.subject.data,
                      sender=app.config['MAIL_SENDER'],
                      recipients=['mike@bloy.org'])
    message.body = """
    Website contact message from {0} ({1}):

    {2}""".format(form.name.data, form.email.data, form.message.data)
    mail.send(message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

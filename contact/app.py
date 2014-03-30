from flask import Flask, render_template, request
from forms import ContactForm


app = Flask(__name__)
app.secret_key = "Development Secret Key"


@app.route('/', methods=['GET', 'POST'])
def contact():
    skin = 'skin_development.html'
    form = ContactForm()
    if request.method == 'POST':
        if form.validate():
            return "valid Form posted"
    return render_template('contact.html', skin=skin, form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

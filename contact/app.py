from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "Development Secret Key"


@app.route('/')
def hello_world():
    skin = 'skin_development.html'
    return render_template('contact.html', skin=skin)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

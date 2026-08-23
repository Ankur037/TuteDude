from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello, World!</h1><p>This is my Flask application.</p>'

@app.route('/api/<name>')
def name(name):
    length = len(name)

    if length > 5:

        return 'Name is too long!'

    else:
        return f'Hello, {name}! Your name has {length} characters.'


if __name__ == '__main__':

    app.run(debug=True)
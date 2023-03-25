from flask import Flask

app = Flask(__name__)



@app.route('/members')
def get_members():
    return {'members': ['John', 'Paul', 'George', 'Ringo']}
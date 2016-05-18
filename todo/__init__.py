from flask import Flask

app = Flask(__name__)

app.secret_key="wtf"

from todo import view
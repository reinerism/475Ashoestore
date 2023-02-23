from flask import Flask
import os
from db import get



#creatin an instance of flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_songs():
    return get()

if __name__ == '__main__':
    app.run()

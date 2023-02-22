from flask import Flask
import os
from db import get



#creatin an instance of flask
app = Flask(__name__)

db_user = os.environ.get('CLOUD_SQL_USERNAME'),
db_password = os.environ.get('CLOUD_SQL_PASSWORD'),
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME'),
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME'),


@app.route('/', methods=['GET'])
def get_songs():
    return get()

if __name__ == '__main__':
    app.run()

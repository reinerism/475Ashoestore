# db.py
from flask import jsonify
import mysql.connector
import os

db_user = os.environ.get('CLOUD_SQL_USERNAME'),
db_password = os.environ.get('CLOUD_SQL_PASSWORD'),
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME'),
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = mysql.connector.connect(user=db_user,
                                   password=db_password,
                                   unix_socket=unix_socket,
                                   db=db_name,
                                   cursorclass=mysql.connector.cursors.DictCursor
                                   )
    except mysql.connector.MySQLError as e:
        return e
    return conn

def get():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM SHOE;')
        songs = cursor.fetchall()
        if result > 0:
            got_shoes = jsonify(songs)
        else:
            got_shoes = 'No shoes in DB'
        return got_shoes

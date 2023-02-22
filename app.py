from flask import Flask
import mysql.connector
import os



#creatin an instance of flask
app = Flask(__name__)

db_user = os.environ.get('CLOUD_SQL_USERNAME'),
db_password = os.environ.get('CLOUD_SQL_PASSWORD'),
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME'),
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME'),


#define route displays query 
@app.route('/')
def index():
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = mysql.connector.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM SHOE;')
        result = cursor.fetchall()
        current_msg = result[0][0]
    cnx.close()

    return str(current_msg)


if __name__ == "__main__":
        app.run(host='127.0.0.1', port=8080, debug=True)

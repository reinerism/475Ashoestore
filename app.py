# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python39_cloudsql_mysql]
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python39_cloudsql_mysql]
import os

from flask import Flask, request, render_template, jsonify
import pymysql
import sqlalchemy

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)


def get_db():
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        return pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        return pymysql.connect(user='mastershoe', password='shoe',
                              host='127.0.0.1', db='shoestore')


def get(cnx, query):
    with cnx.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    cnx.close()
    
    # Return query result as string
    return (result)


@app.route('/', methods=['GET'])
def main():
    # Connect to Cloud SQL instance using Cloud SQL Proxy
    """if request.method =='GET':
        cnx = get_db()
        query = request.form
        result = get(cnx, query)
        cnx.close()
        return result
    else :
        return render_template('home.html')"""
    # Return query result as string
   
    cnx = get_db()
    result = get(cnx, query)
    query = 'SELECT * FROM SHOE;'
    cnx.close()
    return render_template(result[0])
    #return 'Welcome to the test page for Team Pineapple Shoe Store Database'

# [END gae_python37_cloudsql_mysql]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

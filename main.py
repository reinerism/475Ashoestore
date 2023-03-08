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

from flask import Flask, request, render_template, redirect, url_for, flash
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
        host = '127.0.0.1'
        return pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

"""def get(cnx, query):
    with cnx.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        curr_msg = result[0][0]
    return curr_msg"""

def get(cnx, query):
    with cnx.cursor() as cursor:
        cursor.execute(query)
        # the result is a list of tuples
        # col name fix: need to get the description attribute
        # from the first entry in the table
        col_names = [col[0] for col in cursor.description]
        result = cursor.fetchall()
    return col_names, result

@app.route('/', methods = ['GET', 'POST'])
def main():
    cnx = get_db()
    if request.method == 'POST':
        query_user = request.form.get('query_user')

        # may want to test request.form.get
        # current implementation raises a "KeyError"
        # if the query field is missing
        # request.form.get returns 'None' 
        if query_user == 'customer':
            customer_query = request.form.get('customer_query')
            query = f"SELECT SHOES.shoe_id, SHOES.shoe_brand, SHOES.shoe_type, SHOES.shoe_color, SHOE_STORE.store_id, SHOE_STORE.store_name, SHOE_STORE.store_location \
              FROM SHOES \
              INNER JOIN INVENTORY ON SHOES.shoe_id = INVENTORY.shoe_id \
              INNER JOIN SHOE_STORE ON INVENTORY.store_id = SHOE_STORE.store_id \
              WHERE SHOES.shoe_style LIKE '%{customer_query}%' \
              OR SHOES.shoe_brand LIKE '%{customer_query}%' \
              OR SHOES.shoe_type LIKE '%{customer_query}%' \
              OR SHOES.shoe_color LIKE '%{customer_query}%' \
              OR SHOE_STORE.store_name LIKE '%{customer_query}%' \
              OR SHOE_STORE.store_location LIKE '%{customer_query}%'"
        elif query_user == 'store':
            query = request.form.get('store_query')
        # this block is used to avoid an blank submission to database
        # avoid internal service error
        else:
            cnx.close()
            return render_template('home.html', error="Invalid query user")
        if not query:
            cnx.close()
            return redirect(url_for('main'))
        try:
            col_names, result = get(cnx, query)
            # need this info to merge the table in the HTML
            # num_col = len(col_names)
    # Return query result as string
            cnx.close()
            return render_template('home.html', result=result, col_names = col_names)
        except Exception as e:
            cnx.close()
            return render_template('home.html', error=str(e))
    else:
        cnx.close()
        return render_template('home.html')



# [END gae_python37_cloudsql_mysql]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

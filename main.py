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
            shoe_name = request.form.get('shoe_name')
            style = request.form.get('style')
            brand = request.form.get('brand')
            size = request.form.get('size')
            gender = request.form.get('gender')
            max_price = request.form.get('shoe_price') 
          
             # Construct the SQL query using the selected values
             #uses 
            query = "SELECT SHOES.Shoe_id, SHOES.Name, SHOES.Brand, SHOES.Size, SHOES.Style, SHOES.Color, SHOES.Price, SHOES.Gender, SHOE_STORE.Store_name \
              FROM SHOES \
              INNER JOIN INVENTORY ON SHOES.Shoe_id = INVENTORY.Shoe_id \
              INNER JOIN SHOE_STORE ON INVENTORY.Store_id = SHOE_STORE.Store_id \
              WHERE 1=1"
            if shoe_name:
                query += f" AND SHOES.Name LIKE '%{shoe_name}%'"
            else:
                query += " AND 1=1"
            if style:
                query += f" AND SHOES.Style = '{style}'"
            # query if the input is not entered we take everything
            else:
                query += " AND 1=1"
            if brand:
                query += f" AND SHOES.Brand = '{brand}'"
            else:
                query += " AND SHOES.Brand LIKE '%'"
            if size:
                query += f" AND SHOES.Size = '{size}'"
            else:
                query += " AND SHOES.Size LIKE '%'"
            if gender:
                query += f" AND SHOES.Gender = '{gender}'"
            else:
                query += " AND SHOES.Gender LIKE '%'"
            if max_price:
                query += f" AND SHOES.Price <= {max_price}"
            else:
                query += " AND SHOES.Price <= '1000000'" 
        # if the store query is used demonstrating more functionality   
        elif query_user == 'store':
            #grabbing input from HTML
            store_name = request.form.get('store_name')
            ship_state = request.form.get('state')
            order_status =request.form.get('order_status')
            from_date = request.form.get('from_date')
            to_date = request.form.get('to_date')
            # creating the interesting query
            query = "SELECT COUNT(*) AS 'number of orders', SUM(Total_cost) AS 'total $$' \
                FROM ORDERS \
                INNER JOIN SHOE_STORE ON ORDERS.Store_id = SHOE_STORE.Store_id \
                WHERE 1 = 1 "
            if store_name:
                query += f" AND SHOE_STORE.Store_name = '{store_name}'"
            else:
                query += " AND 1=1"

            if order_status:
                query += f" AND ORDER.Order_status = '{order_status}'"
            else:
                query += " AND 1=1"
            """if ship_state:
                query += f" AND SHOE_STORE.Shipping_info LIKE '%{ship_state}%'"
            else:
                query += " AND 1=1"""
            if from_date:
                query += f" AND ORDERS.Order_date >= '{from_date}'"
            else:
                query += " AND 1=1"
            if to_date:
                query += f" AND ORDERS.Order_date <= '{to_date}"
            else:
                query += " AND 1=1"
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

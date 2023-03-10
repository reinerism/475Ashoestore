#Author: Reiner Opitz
#Date: 03/13/2023
#This is the web application for the shoe store database

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
            query = "SELECT SHOES.Shoe_id, SHOES.Name, SHOES.Brand, SHOES.Size, SHOES.Style, SHOES.Color, SHOES.Price, SHOES.Gender, SHOE_STORE.Store_name, INVENTORY.Quantity  \
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
                query += " ORDER BY SHOES.price DESC"
            else:
                query += " AND SHOES.Price <= '1000000'" 
                query += " ORDER BY SHOES.price DESC"
        # if the store query is used demonstrating more functionality   
        elif query_user == 'store':
            #grabbing input from HTML
            store_name = request.form.get('store_name')
            ship_state = request.form.get('state')
            order_status =request.form.get('order_status')
            from_date = request.form.get('from_date')
            to_date = request.form.get('to_date')
            # creating the interesting query
            query = "SELECT CUSTOMER.Customer_id, CUSTOMER.Last_name, CUST_ADDR.Cust_addr_state, ORDERS.Order_status,SUM(ORDERS.Total_cost) AS 'total amount of order', ORDERS.Order_date \
                FROM ORDERS \
                INNER JOIN SHOE_STORE ON ORDERS.Store_id = SHOE_STORE.Store_id \
                INNER JOIN CUSTOMER ON ORDERS.Customer_id = CUSTOMER.Customer_id \
                INNER JOIN CUST_ADDR ON CUSTOMER.Customer_id = CUST_ADDR.Customer_id \
                WHERE 1 = 1 "
            if store_name:
                query += f" AND SHOE_STORE.Store_name = '{store_name}'"
            else:
                query += " AND 1=1"
            if order_status:
                query += f" AND ORDERS.Order_status = '{order_status}'"
            else:
                query += " AND 1=1"
            if ship_state:
                query += f" AND CUST_ADDR.Cust_addr_state LIKE '%{ship_state}%'"
            else:
                query += " AND 1=1"
            if from_date:
                query += f" AND ORDERS.Order_date >= '{from_date}'"
            else:
                query += " AND 1=1"
            if to_date:
                query += f" AND ORDERS.Order_date <= '{to_date}'"
            else:
                query += " AND 1=1"
            query += " GROUP BY CUSTOMER.Customer_id, CUSTOMER.Last_name, CUST_ADDR.Cust_addr_state, ORDERS.Order_status, ORDERS.Order_date;"
        # this block is used to avoid an blank submission to database
        # avoid internal service error
        elif query_user == 'admin':
            query = request.form.get('admin_query')
            #error handling to avoid users from creating,dropping, or altering tables!
            if 'create' in query.lower() or 'drop' in query.lower() or 'alter' in query.lower():
                return 'You been put in a time out for trying to do bad things to my database!<br>If you Promise to be nice just hit the "backarrow" in your browser =)<br>And please NO funny business or you will get sent back here >:('
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

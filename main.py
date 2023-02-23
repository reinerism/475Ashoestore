from flask import Flask, render_template, request
import os
import mysql.connector

# Get database connection details from environment variables
db_user = os.environ['MYSQL_USER']
db_password = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
cloud_sql_connection_name = os.environ['CLOUD_SQL_CONNECTION_NAME']

# Create a connection object to the Cloud SQL database
cnx = mysql.connector.connect(user=db_user, password=db_password,
                              database=db_name, unix_socket="/cloudsql/{}".format(cloud_sql_connection_name))

# Create a Flask app object
app = Flask(__name__)

# Define a route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for executing SQL queries
@app.route('/query', methods=['POST'])
def query():
    # Get the query string from the form submission
    query_string = request.form['query']
    # Create a cursor object for executing SQL queries
    cursor = cnx.cursor()
    # Execute the query
    cursor.execute(query_string)
    # Fetch the results
    results = cursor.fetchall()
    # Get the column names
    column_names = [i[0] for i in cursor.description]
    # Close the cursor
    cursor.close()
    # Render the results template with the query results and column names
    return render_template('results.html', results=results, column_names=column_names)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
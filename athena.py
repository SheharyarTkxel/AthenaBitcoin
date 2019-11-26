# Library Imports
import pyodbc
import sys


# Creates a Database titled "UserDB" along with a table "UsersTable"
# Returns a "pyodbc" connection object which connects to the SQL Server instance in the Docker container that is hosted on the local machine
def get_db_connection():
    server = '<YourHostIP>'
    database = 'UserDB'
    username = 'SA'
    password = '<YourSQLServerUserPassword>'
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';PORT=1433;UID=' + username + ';PWD=' + password, autocommit=True)
    cursor = connection.cursor()
    try:
        cursor.execute('USE ' + database)
    except:
      cursor.execute('CREATE Database ' + database)
      cursor.execute('USE ' + database)
      cursor.execute('CREATE TABLE UsersTable (UserId int NOT NULL IDENTITY PRIMARY KEY, Name varchar(100));')

    return connection


# Creates a user with the name given and returns a success message
def create_user(name):
  connection = get_db_connection()
  cursor = connection.cursor()
  cursor.execute('INSERT INTO UsersTable VALUES(\'' + name + '\')')
  connection.commit()
  success_message = 'Record successfully added.'
  print(success_message)
  return success_message

# Nose Testing function for create_user
def create_user_nose_test():
  assert create_user('Sheharyar') == 'Record successfully added.'


# Returns the record of a previously added user
def get_user(user_id):
  connection = get_db_connection()
  cursor = connection.cursor()
  result = ''
  try:
    cursor.execute('SELECT * FROM UsersTable WHERE UserId=' + str(user_id))
    result = cursor.fetchone()
  except:
    result = 'Record not found.'
  print(result)
  return result

# Nose Testing function for get_user
def get_user_nose_test():
  assert get_user(1) != 'Record not found.'


# Return a list of all users in the database
def get_all_users():
  connection = get_db_connection()
  cursor = connection.cursor()
  cursor.execute('SELECT * FROM UsersTable')
  for row in cursor:
    print(row)

# Runs a malformed query. Returns a Failure message if the query is correct, otherwise generates a relevant exception which we interpret as a success.
def malformed_query(query):
  connection = get_db_connection()
  cursor = connection.cursor()
  result = ''
  try:
    cursor.execute(query)
    result = 'Test failed because the query was correct and no exception was generated. This test will succeed only when an exception generates.'
    print(result)
    return result
  except Exception as ex:
    result = 'Exception:' + str(ex)
    print(result)
    return result

# Nose Testing function for malformed_query
def malformed_query_nose_test():
  assert str(malformed_query('SELECT * FROM NonExistentTable')) != 'Test failed because the query was correct and no exception was generated. This test will succeed only when an exception generates.'


if __name__ == '__main__':
    try:
      if sys.argv[1]=='create_user':
        create_user(sys.argv[2])
      elif sys.argv[1]=='get_user':
        get_user(sys.argv[2])
      elif sys.argv[1] == 'get_all_users':
        get_all_users()
      elif sys.argv[1]=='malformed_query':
        malformed_query(sys.argv[2])
    except:
      print('Wrong no. of parameters or spelling errors.')

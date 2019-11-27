# Athena Bitcoin
Setup guide for Athena's POC


### What does this POC do?
- ***get_db_connection()*** function returns a good connection with the SQL Server instance that is running in a Docker container. It also creates a Database with a simple User(UserId, Name) table if it doesn't exists already.
- ***create_user(name)*** function takes in a name parameter and creates a record against it.
- ***get_user(user_id)*** function returns the user record against the specified id.
- ***malformed_query(query)*** takes in an SQL query and generates an exception in case of malformed query, otherwise fails the test if the query is legit.
- ***create_user_nose_test()*** nose tests the ***create_user(name)*** function.
- ***get_user_nose_test()*** nose tests the ***get_user(user_id)*** function.
- ***malformed_query_nose_test()*** nose tests the ***malformed_query(query)*** function.


### Testing Environment
- Ubuntu 18.04


### Pre-requisites
- Docker
- pyodbc
- Nose Testing package
- SQL Server instance in Docker (**MUST USE 2017 IMAGE ONLY AS 2019 RUNS INTO ERRORS**). Steps:
  1. Pull SQL 2017 Image:   sudo docker pull mcr.microsoft.com/mssql/server:2017-latest
  2. Configure/Run SQL Container:   sudo docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=<YourStrong@Passw0rd>" -p 1433:1433 --name sql_container -d mcr.microsoft.com/mssql/server:2017-latest
  3. Start Interactive Bash Shell:   sudo docker exec -it sql_container "bash"
  4. Connect Locally with SQLCMD: /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "<YourNewStrong@Passw0rd>"


### How to run the POC?
1. Make sure the Pre-requisites are fulfilled and an SQL Server instance is in the running state in a Docker container as instructed above.
2. On Ubuntu, the athena.py file can be run with the below commands:
    - *python3 athena.py create_user SomeUserName*
    - *python3 athena.py get_user AValidUserID*
    - *python3 athena.py malformed_query 'SELECT * FROM UsersTable'*
3. On Ubuntu, **Nose Testing** can be performed on the athena.py file by runing this command:
    - *nosetests athena.py*

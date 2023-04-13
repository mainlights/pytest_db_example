The task:
1. Write a python script that creates a SQLite database according to the specified scheme.
2. Create a script that will randomly fill in the values in the created database.
3. Create a session-scope fixture that gets the current state of the database and creates a temporary
new database where the values are randomized
4. Create autotests that compare data from the original database with the randomized one


Use ```./run_tests.sh``` or run the following commands from project root:
1. Run ```python3 ./create_database.py```
2. Run tests ```pytest```
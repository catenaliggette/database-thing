import mysql.connector
from mysql.connector.plugins import caching_sha2_password

applications_db = mysql.connector.connect(host="localhost", user="a", password="12345", database="schema_requests")

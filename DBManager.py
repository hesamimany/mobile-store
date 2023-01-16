import json

import mysql.connector
import os
import time
import re
from mysql.connector import Error, MySQLConnection
from mysql.connector.cursor_cext import CMySQLCursor

with open('users.json') as reader:
    users = json.load(reader)


def start():
    os.system("cls")
    print("Welcome to database manager\nAvailable options:\n1.Login\n2.Create user")
    op = input(">>> ")
    while not re.match("[1-2]", op):
        print("Invalid input")
        op = input(">>> ")
    if op == "1":
        print("Enter exit to get back")
        username = input("Enter your username: ")
        if username == "exit":
            start()
        if not users.get(username):
            username = input("User not found, enter your username again: ")
            if username == "exit":
                start()
            while not users.get(username):
                username = input("User not found, enter your username again: ")
                if username == "exit":
                    start()
        print("Enter exit to get back")
        password = input("Enter your password: ")
        if password == "exit":
            start()
        if users.get(username) != password:
            password = input("Wrong password, enter your password again: ")
            if password == "exit":
                start()
            while users.get(username) != password:
                password = input("Wrong password, enter your password again: ")
                if password == "exit":
                    start()
        login(username, password)
    if op == "2":
        print("Available users are: ")
        for i in users:
            print(i)
        username = input("Enter your username: ")
        while users.get(username):
            username = input("Username already exist enter your username again: ")
        password = input("Enter your password: ")
        users[username] = password
        createUser(username, password)


def createUser(username, password):
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                             database='mobilestore',
                                             user='root',
                                             password=users.get('root'))
        cursor = connection.cursor()
        cursor.execute(f"CREATE USER IF NOT EXISTS '{username}'@'127.0.0.1' IDENTIFIED BY '{password}'")
        cursor.execute(f"GRANT SELECT ON *.* TO '{username}'@'127.0.0.1'")
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        print("User created successfully")
        with open('users.json', 'w') as writer:
            writer.write(json.dumps(users))
        time.sleep(2.5)
        start()


def login(username, password):
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                             database='mobilestore',
                                             user=username,
                                             password=password)
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        if connection.is_connected():
            startUI(connection)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        print("Going back to login page")
        time.sleep(2.5)
        os.system("cls")
        start()


def startUI(connection: MySQLConnection):
    print("Available options: \n1.Execute your queries\n2.Use Prepared queries\n9.Logout")
    op = input(">>> ")
    if op == '1':
        queryExec(connection)
    elif op == '2':
        ourQueries(connection)
    elif op == '9':
        logout(connection)


def queryExec(connection: MySQLConnection):
    print("Enter exit to get back")
    query = input(">>> ")
    cursor = connection.cursor()
    while query != "exit":
        cursor.execute(query)
        result = cursor.fetchall()
        print(cursor.column_names)
        print(result)
        query = input(">>> ")


def ourQueries(connection: MySQLConnection):
    hell = 1


def logout(connection: MySQLConnection):
    connection.close()
    os.system("cls")
    print("Logging out")
    time.sleep(2.5)
    os.system("cls")
    start()


if __name__ == "__main__":
    start()

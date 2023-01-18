import json

import mysql.connector
import os
import time
import re
from mysql.connector import Error, MySQLConnection
from mysql.connector.cursor_cext import CMySQLCursor

with open('users.json') as reader:
    users = json.load(reader)

ourQueries = ["SELECT Name FROM Product ORDER BY Name ASC",
              "SELECT First_name, Last_name FROM Customer ORDER BY Last_name ASC",
              "SELECT distinct ccp.Product_ID FROM Cart_contains_Product ccp,Cart c WHERE c.Customer_ID=3 and c.ID = ccp.Cart_ID",
              "SELECT c.First_name, c.Last_name FROM Bill b, Customer c WHERE b.Date between '2021-03-24' and '2021-03-31' and c.ID = b.Cart_Customer_ID GROUP BY b.Cart_Customer_ID ORDER BY sum(Total_price) DESC LIMIT 3",
              "SELECT c.First_name, c.Last_name FROM Bill b, Customer c WHERE b.Date between '2021-03-01' and '2021-03-31' and c.ID = b.Cart_Customer_ID GROUP BY b.Cart_Customer_ID ORDER BY sum(Total_price) DESC LIMIT 3",
              "SELECT p.Name FROM Cart c, Product p, Bill b, Cart_contains_Product ccp WHERE ccp.Product_ID = p.ID and b.Cart_ID = c.ID and b.Date between '2021-03-24' and '2021-03-31' GROUP BY ccp.Product_ID ORDER BY count(ccp.Product_ID) DESC LIMIT 3",
              "SELECT p.Name FROM Cart c, Product p, Bill b, Cart_contains_Product ccp WHERE ccp.Product_ID = p.ID and b.Cart_ID = c.ID and b.Date between '2021-03-01' and '2021-03-31' GROUP BY ccp.Product_ID ORDER BY count(ccp.Product_ID) DESC LIMIT 3",
              "SELECT * FROM Product WHERE Discount > 15",
              "SELECT pr.Name, pr.ID, pt.Name FROM Product pt, Provider pr, Product_has_Provider php WHERE pt.ID = php.Product_ID and pr.ID = php.Provider_ID and pt.ID = 3",
              "SELECT pr.Name, pr.ID, pt.Name, MIN(Price) FROM Product pt, Provider pr, Product_has_Provider php WHERE pt.ID = php.Product_ID and pr.ID = php.Provider_ID and pt.ID = 3",
              "SELECT p.Name, b.Cart_Customer_ID FROM Product p, Bill b, Cart_contains_Product ccp WHERE p.ID = ccp.Product_ID and ccp.Cart_ID = b.Cart_ID and b.Cart_Customer_ID = 2 ORDER BY b.Date DESC LIMIT 2",
              "SELECT distinct p1.Name, p1.ID, p2.Name, p2.ID FROM Provider p1, Provider p2 WHERE p1.City = p2.City",
              "SELECT DISTINCT c1.First_name, c1.Last_name FROM Customer c1, Customer c2 WHERE c1.City = c2.City and not (c1.First_name = c2.First_name)"
              ]


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
        create_user(username, password)


def create_user(username, password):
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
            start_ui(connection)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        print("Going back to login page")
        time.sleep(2.5)
        os.system("cls")
        start()


def start_ui(connection: MySQLConnection):
    print("Available options: \n1.Execute your queries\n2.Use Prepared queries\n9.Logout")
    op = input(">>> ")
    if op == '1':
        query_exec(connection)
    elif op == '2':
        our_queries(connection)
    elif op == '9':
        logout(connection)


def query_exec(connection: MySQLConnection):
    print("Enter exit to get back")
    query = input(">>> ")
    cursor = connection.cursor()
    while query != "exit":
        cursor.execute(query)
        if ("INSERT".lower() or "UPDATE".lower()) in query.lower():
            connection.commit()
        if "SELECT".lower() in query.lower():
            result = cursor.fetchall()
            print(cursor.column_names)
            for i in result:
                print(i)
        query = input(">>> ")


def our_queries(connection: MySQLConnection):
    options = ['Products', 'Users', 'Orders', 'Three best users of week', 'Three best users of month',
               'Best seller items of week', 'Best seller items of month', 'Special Offers', 'Seller of an item',
               'Cheapest seller',
               'Two last order of user', 'Sellers of a city', 'Customers of a city', 'Product sell amount in month']
    counter = 1
    print("Available options:")
    for i in options:
        print(f"{counter}.{i}")
        counter += 1

    print("Enter exit to get back")
    op = input(">>> ")
    cursor = connection.cursor()
    while op != "exit":
        cursor.execute(ourQueries[int(op) - 1])
        result = cursor.fetchall()
        for i in result:
            print(i)
        op = input(">>> ")


def logout(connection: MySQLConnection):
    connection.close()
    os.system("cls")
    print("Logging out")
    time.sleep(2.5)
    os.system("cls")
    start()


if __name__ == "__main__":
    start()

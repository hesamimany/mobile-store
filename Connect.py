import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                         database='mobilestore',
                                         user='root',
                                         password='1234')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()


        cursor.execute("INSERT INTO Product(Discount, Weight, Brand, Price, Color, Name) VALUES(10, 200, 'Apple', 2000, 'Gold', 'Iphone 13');")
        cursor.execute("INSERT INTO Product(Discount, Weight, Brand, Price, Color, Name) "
                       "VALUES(11, 200, 'Apple', 2000, 'Gold', 'Iphone 14');")
        connection.commit()
        cursor.execute("select * from product")
        record = cursor.fetchall()
        test = cursor.column_names
        print(test)
        print("You're connected to database: ",record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
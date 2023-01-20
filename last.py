import sys
import json
import mysql.connector
from PyQt5 import QtWidgets
from mysql.connector import Error, MySQLConnection
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush, QFont
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QGridLayout, QPlainTextEdit, QLineEdit, QLabel)

with open('users.json') as reader:
    users = json.load(reader)

gradient = QLinearGradient(0, 0, 0, 400)
gradient.setColorAt(0.8, QColor("#73C8A9"))
gradient.setColorAt(1.0, QColor("#474d59"))
p = QPalette()
p.setBrush(QPalette.Window, QBrush(gradient))
my_font = QFont('Bahnschrift Light', 15)
style_sheet_buttons = "QPushButton { background-color:#00b894;color:white;border-color:white;} " \
                      "QPushButton::hover { background-color:#00cec9;} QPushButton::pressed { background-color:#0984e3;}"
style_sheet_button = "QPushButton {background-color:#b2bec3;} QPushButton::hover { background-color:#636e72;} QPushButton::pressed { background-color:#2d3436;}"
style_sheet_plain_text = "QPlainTextEdit {background-color:#636e72;color:white}"
buttons_text = ['Products', 'Users', 'Orders', 'Three best users of week', 'Three best users of month',
                'Best seller items of week', 'Best seller items of month', 'Special Offers', 'Seller of an item', 'Cheapest seller',
                'Two last order of user', 'Sellers of a city', 'Customers of a city', 'Product sell amount in month']
default_queries_text = ["SELECT Name FROM Product ORDER BY Name ASC",
                        "SELECT First_name, Last_name FROM Customer ORDER BY Last_name ASC",
                        "SELECT distinct ccp.Product_ID FROM Cart_contains_Product ccp,Cart c WHERE c.Customer_ID=# and c.ID = ccp.Cart_ID",
                        "SELECT c.First_name, c.Last_name FROM Bill b, Customer c WHERE b.Date between '2021-03-24' and '2021-03-31' and c.ID = b.Cart_Customer_ID GROUP BY b.Cart_Customer_ID ORDER BY sum(Total_price) DESC LIMIT 3",
                        "SELECT c.First_name, c.Last_name FROM Bill b, Customer c WHERE b.Date between '2021-03-01' and '2021-03-31' and c.ID = b.Cart_Customer_ID GROUP BY b.Cart_Customer_ID ORDER BY sum(Total_price) DESC LIMIT 3",
                        "SELECT p.Name FROM Cart c, Product p, Bill b, Cart_contains_Product ccp WHERE ccp.Product_ID = p.ID and b.Cart_ID = c.ID and b.Date between '2021-03-24' and '2021-03-31' GROUP BY ccp.Product_ID ORDER BY count(ccp.Product_ID) DESC LIMIT 3",
                        "SELECT p.Name FROM Cart c, Product p, Bill b, Cart_contains_Product ccp WHERE ccp.Product_ID = p.ID and b.Cart_ID = c.ID and b.Date between '2021-03-01' and '2021-03-31' GROUP BY ccp.Product_ID ORDER BY count(ccp.Product_ID) DESC LIMIT 3",
                        "SELECT * FROM Product WHERE Discount > 15",
                        "SELECT pr.Name, pr.ID, pt.Name FROM Product pt, Provider pr, Product_has_Provider php WHERE pt.ID = php.Product_ID and pr.ID = php.Provider_ID and pt.ID = #",
                        "SELECT pr.Name, pr.ID, pt.Name, MIN(Price) FROM Product pt, Provider pr, Product_has_Provider php WHERE pt.ID = php.Product_ID and pr.ID = php.Provider_ID and pt.ID = #",
                        "SELECT p.Name, b.Cart_Customer_ID FROM Product p, Bill b, Cart_contains_Product ccp WHERE p.ID = ccp.Product_ID and ccp.Cart_ID = b.Cart_ID and b.Cart_Customer_ID = # ORDER BY b.Date DESC LIMIT 2",
                        "SELECT DISTINCT p1.Name, p1.ID, p1.City FROM Provider p1, Provider p2 WHERE p1.City = p2.City and not (p1.ID = p2.ID) ORDER BY p1.City",
                        "SELECT DISTINCT c1.First_name, c1.Last_name FROM Customer c1, Customer c2 WHERE c1.City = c2.City and not (c1.First_name = c2.First_name)",
                        "SELECT p.ID, p.Name, SUM(p.Price) total FROM Product p, Cart c, Cart_contains_Product ccp WHERE p.ID = ccp.Product_ID and c.ID = ccp.Cart_ID and p.ID = 8"
                        ]


class loginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Queries')
        self.setPalette(p)

        # -----------------------------                                  LOGIN PAGE                               --------------------------- #
        self.login_sign_up_layout = QGridLayout()

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.sign_up_button = QPushButton("Sign Up")
        self.sign_up_button.clicked.connect(self.sign_up)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")

        self.login_sign_up_label = QLabel("")

        self.login_sign_up_user_list = QPlainTextEdit()
        self.login_sign_up_user_list.setReadOnly(True)
        self.login_sign_up_user_list.setPlaceholderText('Users')
        # ----------------------------------------------------------------------------------------------------------------------------------- #

        # -----------------------------                             STYLING LOGIN PAGE                           ---------------------------- #
        self.login_sign_up_layout.setVerticalSpacing(20)

        self.login_button.setFont(my_font)
        self.login_button.setMinimumHeight(35)
        self.login_button.setStyleSheet(style_sheet_buttons)
        self.login_sign_up_layout.addWidget(self.login_button, 0, 0)

        self.sign_up_button.setFont(my_font)
        self.sign_up_button.setMinimumHeight(35)
        self.sign_up_button.setStyleSheet(style_sheet_buttons)
        self.login_sign_up_layout.addWidget(self.sign_up_button, 1, 0)

        self.username.setFont(my_font)
        self.username.setStyleSheet(style_sheet_plain_text)
        self.login_sign_up_layout.addWidget(self.username, 2, 0)

        self.password.setFont(my_font)
        self.password.setStyleSheet(style_sheet_plain_text)
        self.login_sign_up_layout.addWidget(self.password, 3, 0)

        self.login_sign_up_label.setFont(my_font)
        self.login_sign_up_label.setStyleSheet(style_sheet_plain_text)
        self.login_sign_up_layout.addWidget(self.login_sign_up_label, 4, 0)

        self.login_sign_up_user_list.setFont(my_font)
        self.login_sign_up_user_list.setStyleSheet(style_sheet_plain_text)
        self.login_sign_up_layout.addWidget(self.login_sign_up_user_list, 5, 0)
        # ----------------------------------------------------------------------------------------------------------------------------------- #

        self.setLayout(self.login_sign_up_layout)

    # -----------------------------                                   BUTTON FUNCTIONS                             -------------------------- #
    def login(self):
        global connection
        global widget
        username = self.username.text()
        password = self.password.text()
        if not users.get(username):
            self.login_sign_up_label.setText("User not found!")
        if users.get(username) != password:
            self.login_sign_up_label.setText("Wrong password!")
        else:
            try:
                connection = mysql.connector.connect(host='127.0.0.1', database='mobilestore', user=username, password=password)
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                if connection.is_connected():
                    self.username.clear()
                    self.password.clear()
                    widget.setCurrentIndex(1)
            except Error as e:
                print("Error while connecting to MySQL", e)
                self.login_sign_up_label.setText("Error while connecting to MySQL")

    def sign_up(self):
        global connection
        for user in users:
            self.login_sign_up_user_list.appendPlainText(user + "\n")
        username = self.username.text()
        password = self.password.text()
        if users.get(username):
            self.login_sign_up_label.setText("Username already exist!")
        else:
            users[username] = password
            try:
                connection = mysql.connector.connect(host='127.0.0.1', database='mobilestore', user='root', password=users.get('root'))
                cursor = connection.cursor()
                cursor.execute(f"CREATE USER IF NOT EXISTS '{username}'@'127.0.0.1' IDENTIFIED BY '{password}'")
                cursor.execute(f"GRANT SELECT ON *.* TO '{username}'@'127.0.0.1'")
                connection.commit()
                cursor.close()
                connection.close()
                self.username.clear()
                self.password.clear()
                with open('users.json', 'w') as writer:
                    writer.write(json.dumps(users))
                self.login_sign_up_label.setText("User created successfully")
            except Error as e:
                print("Error while connecting to MySQL", e)
                self.login_sign_up_label.setText("Error while connecting to MySQL")


class queryPage(QWidget):
    def __init__(self):
        super().__init__()
        # -----------------------------                                      QUERY PAGE                             ------------------------- #
        self.layout = QGridLayout()
        self.buttons = []
        for i in range(14):
            self.buttons.append(QPushButton(buttons_text[i]))
            self.buttons[i].clicked.connect(lambda state, x=i: self.default_queries(x))

        self.user_id = QLineEdit()
        self.user_id.setPlaceholderText("User ID")

        self.product_id = QLineEdit()
        self.product_id.setPlaceholderText("Product ID")

        logout_button = QPushButton("logout")
        logout_button.clicked.connect(self.logout)

        self.result_box = QPlainTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setPlaceholderText('Result')

        self.query_box = QPlainTextEdit()
        self.query_box.setPlaceholderText('Enter your query')

        query_button = QPushButton("Send Query")
        query_button.clicked.connect(self.query_send)

        # -----------------------------                              STYLING QUERY PAGE                             ------------------------- #
        self.layout.setHorizontalSpacing(50)
        self.layout.setVerticalSpacing(20)
        self.layout.setColumnMinimumWidth(0, int(self.width() * 0.3))
        self.layout.setColumnMinimumWidth(1, int(self.width() * 0.7))

        for i in range(14):
            self.buttons[i].setFont(my_font)
            self.buttons[i].setMinimumHeight(35)
            self.layout.addWidget(self.buttons[i], i, 0)
            self.buttons[i].setStyleSheet(style_sheet_buttons)

        self.user_id.setFont(my_font)
        self.layout.addWidget(self.user_id, 14, 0)
        self.user_id.setStyleSheet(style_sheet_plain_text)

        self.product_id.setFont(my_font)
        self.layout.addWidget(self.product_id, 15, 0)
        self.product_id.setStyleSheet(style_sheet_plain_text)

        logout_button.setFont(my_font)
        logout_button.setMinimumHeight(35)
        self.layout.addWidget(logout_button, 16, 0)
        logout_button.setStyleSheet(style_sheet_buttons)

        self.result_box.setFont(my_font)
        self.layout.addWidget(self.result_box, 0, 1, 8, 2)
        self.result_box.setStyleSheet(style_sheet_plain_text)

        self.query_box.setFont(my_font)
        self.layout.addWidget(self.query_box, 8, 1, 11, 2)
        self.query_box.setStyleSheet(style_sheet_plain_text)

        query_button.setFont(my_font)
        query_button.setMinimumHeight(35)
        self.layout.addWidget(query_button, 14, 1, 15, 2)
        query_button.setStyleSheet(style_sheet_button)

        # ----------------------------------------------------------------------------------------------------------------------------------- #

        self.setLayout(self.layout)

    # -----------------------------                                   BUTTON FUNCTIONS                             -------------------------- #
    def logout(self):
        global connection
        global widget
        self.user_id.clear()
        self.product_id.clear()
        self.result_box.clear()
        self.query_box.clear()
        connection.close()
        widget.setCurrentIndex(0)

    def query_send(self):
        global connection
        try:
            query = self.query_box.toPlainText()
            cursor = connection.cursor()
            cursor.execute(query)
            if ("INSERT".lower() or "UPDATE".lower()) in query.lower():
                connection.commit()
            if "SELECT".lower() in query.lower():
                result = cursor.fetchall()
                self.result_box.setPlainText(cursor.column_names + "\n")
                for i in result:
                    self.result_box.appendPlainText(i + "\n")
        except Error as e:
            self.result_box.setPlainText("Problem")
            print("Error: ", e)

    def default_queries(self, index):
        global connection
        try:
            cursor = connection.cursor()
            print(cursor)
            query = default_queries_text[index]
            print(query)
            if index == 2 and self.user_id.text() != "":
                query.replace('#', self.user_id.text())

            elif (index == 8 or index == 9 or index == 10) and self.product_id.text() != "":
                query.replace('#', self.product_id.text())

            elif index == 2 or index == 9 or index == 9 or index == 11:
                self.result_box.setPlainText("Enter needed user or product id")
            else:
                cursor.execute(query)
                result = cursor.fetchall()
                print(result)
                self.result_box.setPlainText(f"{cursor.column_names}\n")
                print(1)
                count = 0
                for i in result:
                    print(type(i))
                    print(count)
                    count+=1
                    self.result_box.appendPlainText(f"{i}\n")
        except Error as e:
            self.result_box.setPlainText("Problem")
            print("Error: ", e)


connection: MySQLConnection
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
loginPage = loginPage()
queryPage = queryPage()
widget.addWidget(loginPage)
widget.addWidget(queryPage)
widget.setFixedHeight(1000)
widget.setFixedWidth(900)
widget.show()
sys.exit(app.exec_())
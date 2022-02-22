import sqlite3


class DataBase:
    def __init__(self, name):
        self.connection = self.create_db(name)

    def create_db(self, name):
        return sqlite3.connect(name)

    def get_cursor(self):
        return self.connection.cursor()

    def select_client(self):
        cursor = self.get_cursor()
        cursor.execute("""
            SELECT 
                   Clients.user_name AS 'Клиент',
                   SUM(Products.price) AS 'Общая сумма покупок'
            FROM
                (Orders
                JOIN Clients ON Orders.id_users=Clients.id_users
                JOIN Products ON Products.id_product=Orders.id_product)
                GROUP BY Clients.user_name
        """)
        return cursor.fetchall()

    def select_pay_phone(self):
        cursor = self.get_cursor()
        cursor.execute("""
        SELECT Clients.user_name AS 'Клиент'
        FROM
            Orders
            JOIN Clients ON Orders.id_users=Clients.id_users
            JOIN Products ON Products.id_product=Orders.id_product
            WHERE Orders.id_product=5
        """)
        return cursor.fetchall()

    def select_count_pay(self):
        cursor = self.get_cursor()
        cursor.execute("""
                SELECT
                       Products.product_name AS 'Товар',
                       count (*) AS 'Количество заказов'
                FROM
                    (Orders
                    JOIN Products ON Products.id_product=Orders.id_product)
                    GROUP BY Orders.id_product
                """)
        return cursor.fetchall()


if __name__ == "__main__":
    db = DataBase("db.sqlite3")
    one = db.select_client()
    two = db.select_count_pay()
    three = db.select_pay_phone()
    print(one, two, three, sep='\n')

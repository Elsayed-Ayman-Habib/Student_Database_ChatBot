import sqlite3

class Database:
    def __init__(self, db_name='student.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255),
                age INTEGER,
                grade VARCHAR(50),
                email TEXT UNIQUE
            )
        ''')
        self.conn.commit()

    def insert_user(self, name, age, grade, email):
        self.cursor.execute('''
            INSERT INTO users (name, age, grade, email)
            VALUES (?, ?, ?, ?)
        ''', (name, age, grade, email))
        self.conn.commit()

    def insert_many_users(self, users):
        self.cursor.executemany('''
            INSERT INTO users (name, age, grade, email)
            VALUES (?, ?, ?, ?)
        ''', users)
        self.conn.commit()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def get_user_by_name(self, name):
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        return self.cursor.fetchone()

    def get_user_by_grade(self, grade):
        self.cursor.execute("SELECT * FROM users WHERE grade = ?", (grade,))
        return self.cursor.fetchone()

    def update_user_age(self, name, new_age):
        self.cursor.execute("UPDATE users SET age = ? WHERE name = ?", (new_age, name))
        self.conn.commit()
    
    def update_user_grade(self, name, new_grade):
        self.cursor.execute("UPDATE users SET grade = ? WHERE name = ?", (new_grade, name))
        self.conn.commit()

    def delete_user_by_name(self, name):
        self.cursor.execute("DELETE FROM users WHERE name = ?", (name,))
        self.conn.commit()

    def delete_all_users(self):
        self.cursor.execute("DELETE FROM users")
        self.conn.commit()

    def drop_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS users")
        self.conn.commit()

    def close(self):
        self.conn.close()

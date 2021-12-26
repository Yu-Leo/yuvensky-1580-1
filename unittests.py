import os
import unittest

from database import Database


class TestDatabase(unittest.TestCase):
    """
    Class for testing database module
    """
    DB_PATH = "test_db.db"
    database = None

    @classmethod
    def del_db_file(cls):
        if os.path.isfile(cls.DB_PATH):
            os.remove(cls.DB_PATH)

    @classmethod
    def setUpClass(cls) -> None:
        cls.del_db_file()
        cls.database = Database(path=cls.DB_PATH)
        cls.database.cursor.executescript(
            """
            BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "accounts" (
    "account_id"	INTEGER,
    "login"	TEXT NOT NULL UNIQUE,
    "first_name"	TEXT,
    "last_name"	TEXT,
    "email"	TEXT NOT NULL UNIQUE,
    "password"	TEXT NOT NULL,
    "total_rating"	INTEGER,
    "registration_date"	TEXT NOT NULL,
    "birthday"	TEXT,
    PRIMARY KEY("account_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "active_courses" (
    "active_course_id"	INTEGER,
    "account_id"	INTEGER NOT NULL,
    "course_id"	INTEGER NOT NULL,
    "percentage_of_passing"	INTEGER NOT NULL,
    "mark"	REAL NOT NULL,
    FOREIGN KEY("account_id") REFERENCES "accounts"("account_id"),
    FOREIGN KEY("course_id") REFERENCES "courses"("course_id"),
    PRIMARY KEY("active_course_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "courses" (
    "course_id"	INTEGER,
    "name"	TEXT NOT NULL UNIQUE,
    "lessons_number"	INTEGER NOT NULL,
    "description"	TEXT,
    "rating"	INTEGER,
    "passage_time"	INTEGER,
    PRIMARY KEY("course_id" AUTOINCREMENT)
);
COMMIT;
INSERT INTO "accounts" VALUES (1,'leo','Lev','Yu','l@test.ru','12345',100,'2021-11-21','2004-12-11');
INSERT INTO "accounts" VALUES (2,'max','Max','Ivanov','m@test.ru','qwerty',50,'2020-11-20','2005-01-01');
INSERT INTO "accounts" VALUES (3,'misha','Misha','Mikhailov','misha@test.ru','qwerty123',80,'2021-08-20','2003-01-01');
INSERT INTO "accounts" VALUES (4,'masha','Masha','Petrova','masha@test.ru','3333',91,'2021-10-21','2003-11-27');
INSERT INTO "accounts" VALUES (5,'nick','Nikolay','Ivanov','nick@gmail.com','dfsdfsidmfi3434',50,'2021-11-27','2000-11-27');
INSERT INTO "active_courses" VALUES (1,1,1,100,100.0);
INSERT INTO "active_courses" VALUES (2,2,1,50,80.0);
INSERT INTO "active_courses" VALUES (3,2,2,70,90.0);
INSERT INTO "active_courses" VALUES (4,3,3,70,80.0);
INSERT INTO "active_courses" VALUES (5,1,3,70,70.0);
INSERT INTO "courses" VALUES (1,'Linux',10,'Краткий курс по основам ОС Linux',10,10);
INSERT INTO "courses" VALUES (2,'Windows',3,'Краткий курс по основам ОС Windows',3,8);
INSERT INTO "courses" VALUES (3,'Python',20,'Краткий курс по основам Python',8,20);
        """)
        cls.database.connection.commit()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.database.close()
        cls.del_db_file()

    def test_get_users_id_list(self):
        result = self.database.get_users_id_list()
        self.assertEqual(result, ['1', '2', '4', '3', '5'])

    def test_get_all_courses(self):
        result = self.database.get_all_courses()
        self.assertEqual(len(result), 3)
        self.assertEqual(len(result[0]), 3)
        self.assertTrue(result[0][2] > result[1][2] > result[2][2])

    def test_get_user_courses(self):
        test_user_id = 1
        result = self.database.get_user_courses(test_user_id)
        self.assertEqual(result, [('Linux', 100, 100.0), ('Python', 70, 70.0)])

        test_user_id = 2
        result = self.database.get_user_courses(test_user_id)
        self.assertEqual(result, [('Linux', 50, 80.0), ('Windows', 70, 90.0)])

    def test_get_top_of_users(self):
        result = self.database.get_top_of_users()
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][1], 100)
        self.assertTrue(result[0][1] > result[1][1] > result[2][1])

    def test_get_user_info(self):
        test_user_id = 1
        result = self.database.get_user_info(test_user_id)
        self.assertEqual(result, ('leo', 'Lev', 'Yu', 100, '2021-11-21'))

        test_user_id = 5
        result = self.database.get_user_info(test_user_id)
        self.assertEqual(result, ('nick', 'Nikolay', 'Ivanov', 50, '2021-11-27'))

    def test_get_users_whose_birthday_is_today(self):
        self.database.cursor.execute("SELECT (substr(date('now'), 6));")
        current_date = self.database.cursor.fetchall()[0][0]

        self.database.cursor.execute("SELECT substr(birthday, 6) FROM accounts")
        birthdays_dates = [i[0] for i in self.database.cursor.fetchall()]

        k = 0
        for date in birthdays_dates:
            if date == current_date:
                k += 1
        result = self.database.get_users_whose_birthday_is_today()
        self.assertEqual(len(result), k)


if __name__ == "__main__":
    unittest.main(failfast=False)

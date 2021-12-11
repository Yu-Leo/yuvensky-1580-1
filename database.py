import sqlite3


class Database:
    """
    Class for working with database
    """

    def __init__(self, path: str):
        self.__connection = sqlite3.connect(path)  # Database object
        self.__cursor = self.__connection.cursor()

    @property
    def connection(self):
        return self.__connection

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self.__cursor

    def close(self):
        self.__connection.close()

    def get_users_id_list(self):
        request = "SELECT account_id FROM accounts"
        result = self.__cursor.execute(request)
        id_list = result.fetchall()
        return [str(i[0]) for i in id_list]

    def get_all_courses(self):
        request = "SELECT name, description, rating FROM courses ORDER BY rating DESC;"
        result = self.__cursor.execute(request)
        return result.fetchall()

    def get_user_courses(self, user_id: int):
        request = "SELECT (SELECT courses.name FROM courses WHERE courses.course_id == active_courses.course_id) AS \
        course_name, percentage_of_passing, mark FROM active_courses WHERE account_id == :user_id;"
        result = self.__cursor.execute(request, {"user_id": str(user_id)})
        return result.fetchall()

    def get_top_of_users(self):
        request = "SELECT login, total_rating FROM accounts ORDER BY total_rating DESC LIMIT 3;"
        result = self.__cursor.execute(request)
        return result.fetchall()

    def get_user_info(self, user_id: int):
        request = "SELECT login, first_name, last_name, total_rating, registration_date FROM accounts \
        WHERE account_id = :user_id;"
        result = self.__cursor.execute(request, {"user_id": str(user_id)})
        return result.fetchall()[0]

    def get_users_whose_birthday_is_today(self):
        request = "SELECT account_id FROM accounts WHERE substr(birthday, 6) == (substr(date('now'), 6));"
        result = self.__cursor.execute(request)
        return result.fetchall()

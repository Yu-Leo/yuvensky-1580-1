from old_database import Database


class Phrases:
    """
    Class with phrases for the interface in Russian
    """

    list_of_requests = """Список запросов:
1) Получение списка всех курсов (название + описание + рейтинг), отсортированного по невозрастанию их рейтинга

2) Получение списка изучаемых курсов и информации об их прохождении (название курса + процент прохождения + оценка) для\
 одного пользователя по его id

3) Получение информации (логин + рейтинг) о трёх пользователях с наивысшими рейтингами:

4) Получение информации о пользователе (логин + имя + фамилия + рейтинг + когда зарегистрировался) по его id

5) Получение списка id-шников пользователей, у которых сегодня (в день, когда выполняется запрос) д. р. 
"""

    invitation = "Введите номер запроса (от 1 до 5) или q для выхода: "

    finish_work_with_database = "Работа с базой данных завершена"

    courses_list = "Список курсов: "

    invitation_for_user_id = "Введите id пользователя (возможные id: "

    courses_for_user = "Список курсов, изучаемых пользователем с id="

    invalid_id = "Пользователя с таким id не существует"

    top_3_users = "Топ 3 пользователя по рейтингу"

    info_for_user = "Информация о пользователе с id="

    birthday = "Список id пользователей, у которых сегодня (в день, когда выполняется запрос) день рождения"

    invalid_request_number = "Запроса с таким номером не существует"


def main_loop():
    database = Database("database.db")
    acceptable_user_id = database.get_users_id_list()
    print()
    print(Phrases.list_of_requests)
    while True:
        input_data = input(Phrases.invitation)
        if input_data == "q":
            print(Phrases.finish_work_with_database)
            database.close()
            return
        elif len(input_data) == 1 and input_data.isdigit():
            req_num = int(input_data)
            print()
            if req_num == 1:
                print(Phrases.courses_list)
                result = database.get_all_courses()
                for line in result:
                    print(line)

            elif req_num == 2:
                ask_id = Phrases.invitation_for_user_id + f"{acceptable_user_id}): "
                user_id_str = input(ask_id)
                print()
                if user_id_str in acceptable_user_id:
                    user_id = int(user_id_str)
                    print(Phrases.courses_for_user + f"{user_id}:")
                    result = database.get_user_courses(user_id)
                    for line in result:
                        print(line)
                else:
                    print(Phrases.invalid_id)

            elif req_num == 3:
                print(Phrases.top_3_users)
                result = database.get_top_of_users()
                for line in result:
                    print(line)

            elif req_num == 4:
                ask_id = Phrases.invitation_for_user_id + f"{acceptable_user_id}): "
                user_id_str = input(ask_id)
                print()
                if user_id_str in acceptable_user_id:
                    user_id = int(user_id_str)
                    print(Phrases.info_for_user + f"{user_id}:")
                    result = database.get_user_info(user_id)
                    print(result)
                else:
                    print(Phrases.invalid_id)

            elif req_num == 5:
                print(Phrases.birthday)
                result = database.get_users_whose_birthday_is_today()
                print(result)

            else:
                print(Phrases.invalid_request_number)

            print()


main_loop()

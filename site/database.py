from main import database, Courses


def create_database_structure():
    database.create_all()


def add_courses():
    course_python_basics = Courses(link="python_basics",
                                   logo_file_name="python_logo.jpg",
                                   name="Python. Основы",
                                   price=0,
                                   description="Супер курс по основам Python",
                                   lessons_number=5,
                                   rating=100,
                                   passage_time=15)

    course_python_pro = Courses(link="python_pro",
                                logo_file_name="python_logo.jpg",
                                name="Python. Pro",
                                price=5000,
                                description="Супер курс с профессиональными фишками Python ",
                                lessons_number=5,
                                rating=200,
                                passage_time=30)

    course_cpp_basics = Courses(link="cpp_basics",
                                logo_file_name="cpp_logo.png",
                                name="C++. Основы",
                                price=0,
                                description="Супер курс по основам C++",
                                lessons_number=5,
                                rating=200,
                                passage_time=30)

    course_cpp_pro = Courses(link="cpp_pro",
                             logo_file_name="cpp_logo.png",
                             name="C++. Pro",
                             price=5000,
                             description="Супер курс с профессиональными фишками C++",
                             lessons_number=5,
                             rating=200,
                             passage_time=30)

    database.session.add(course_python_basics)
    database.session.add(course_python_pro)
    database.session.add(course_cpp_basics)
    database.session.add(course_cpp_pro)
    database.session.commit()


if __name__ == '__main__':
    create_database_structure()
    add_courses()

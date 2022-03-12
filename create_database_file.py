from app.models import *

if __name__ == "__main__":
    create_database_structure()
    add_courses()
    add_reviews()
    add_accounts()
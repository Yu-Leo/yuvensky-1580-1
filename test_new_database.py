import create_database_structure as new_db
import datetime

acc1 = new_db.Accounts(login="leo", email="leo@gmail.com", password="123", total_rating=100,
                       registration_date=datetime.datetime.now())
acc2 = new_db.Accounts(login="max", email="max@gmail.com", password="123121212", total_rating=10,
                       registration_date=datetime.datetime.now())
acc3 = new_db.Accounts(login="ivan", email="ivan@gmail.com", password="000000", total_rating=50,
                       registration_date=datetime.datetime.now())

new_db.database.session.add(acc1)
new_db.database.session.add(acc2)
new_db.database.session.add(acc3)
new_db.database.session.commit()

print(new_db.Accounts.query.all())

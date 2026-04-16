from faker import Faker
import random
from app import app 
from extensions import db
from models import Expense, Person

fake=Faker()

with app.app_context():

    person_ids = [p.id for p in Person.query.all()]
    
    if not person_ids:
        print("No users found! Please create some users first.")

    
    for _ in range(100):
        new_expense = Expense(
            title=fake.word(),
            amount=round(random.uniform(1000.0, 5000.0), 2),
            description=fake.sentence(nb_words=3),
            person_id=random.choice(person_ids)
        )
        db.session.add(new_expense)

    db.session.commit()
    print("Successfully seeded 100 expenses!")
from extensions import db, bcrypt

class Person(db.Model):
    __tablename__='persons'

    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100), unique=True, nullable=False)
    password=db.Column(db.String(150), nullable=False)

    expenses=db.relationship('Expense', back_populates='person', cascade='delete, delete-orphan')

    def hash_password(self, password):
        """hash passowrd using bycrypt"""
        self.password=bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """check if password is same as one saved in db"""
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f'Person(name={self.email}, password={self.password})'


class Expense(db.Model):
    __tablename__="expenses"

    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    amount=db.Column(db.Numeric(10,2), nullable=False)
    description=db.Column(db.Text)

    person_id=db.Column(db.Integer, db.ForeignKey('persons.id'))

    person=db.relationship('Person', back_populates='expenses')

    def __repr__(self):
        return f'Expense(title={self.title}, amount={self.amount})'



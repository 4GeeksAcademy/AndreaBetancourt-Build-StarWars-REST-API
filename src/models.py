from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 1. Definir clase y campos
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    # favorites = db.relationship('Favorites')

    def __repr__(self):
        return '<Users %r>' % self.email

    def serialize(self):
        # favorites = [fav.serialize() for fav in self.favorites] 
        return {
            "id": self.id,
            "email": self.email,
            # "favorites": favorites
            # do not serialize the password, its a security breach
        }


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    # users = db.relationship("Users", back_populates="favorites")

    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    planets = db.relationship("Planets", back_populates="favorites")

    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    people = db.relationship("People", back_populates="favorites")

    def serialize(self):
        return {
            "id" : self.id,
            # "user_id" : self.user_id,
            "planet_id" : self.planet_id,
            "people_id" : self.people_id,
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    url = db.Column(db.String(400), unique=False, nullable=False)
    favorites = db.relationship('Favorites', back_populates='planets')


    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
        }    
    

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    url = db.Column(db.String(400), unique=False, nullable=False)
    favorites = db.relationship('Favorites', back_populates='people')

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
        } 



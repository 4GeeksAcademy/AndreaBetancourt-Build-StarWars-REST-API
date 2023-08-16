"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, People, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_user():
    users = Users.query.all()

    if not users:
        return jsonify({"message": "There are no registered users"}), 404

    user_list = [user.serialize() for user in users]
    return jsonify(user_list), 200


@app.route('/users/<int:user_id>/', methods=['GET'])
def user_id(user_id):
    user = Users.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_serialized = user.serialize()
    return jsonify(user_serialized), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    # Se hace un for para recorrer lo que me devuelve la API, el cual se puede hacer mediante una lista comprimida.
    planets_list = [planet.serialize() for planet in planets]
    return jsonify(planets_list), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    # Busca en el modelo de datos Planets y obtén un solo elemento
    planet = Planets.query.get(planet_id)
    
    if not planet:
        return jsonify({"message": "Planet not found"}), 404

    planet_serialized = planet.serialize()
    return jsonify(planet_serialized), 200


@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    
    if not people:
        return jsonify({"message": "People not found"}), 404
    
    people_list = [person.serialize() for person in people]
    return jsonify(people_list), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person_id(person_id):
    person = People.query.get(person_id)

    if not person:
        return jsonify({"message": "Person not found"}), 404

    return jsonify(person.serealize()), 200


# @app.route('/users/<int:user_id>/favorites', methods=['GET'])
# def get_favorites(user_id):

#     favorites = Favorites.query.get(user_id)
    
#     if not user_id:
#         return jsonify({"message": "Favorites not found"}), 404

#     favorites_serialized = favorites.serealize()
#     return jsonify(favorites_serialized), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

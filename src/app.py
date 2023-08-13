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
from models import db, User, Planets
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


# RUTAS 

#GET Users
@app.route('/user', methods=['GET'])
def handle_user():
    allusers = User.query.all()
    results = list(map(lambda item: item.serialize(),allusers))

    return jsonify(results), 200

#GET Single User
@app.route('/user/<int:user_id>', methods=['GET'])
def single_user(user_id):
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user.serialize()), 200


# POST user




# DELETE user
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    thatuser = User.query.get(user_id)
    if thatuser is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(thatuser)
    db.session.commit()

    return jsonify("User deleted"), 200


#PLANETAS 

#GET Planetas (TODOS-ALL)
@app.route('/planets', methods=['GET'])
def handle_planets():
    allplanets = Planets.query.all()
    planetsList = list(map(lambda p: p.serialize(),allplanets))

    return jsonify(planetsList), 200

#GET un solo planeta
@app.route('/planets/<int:planets_id>', methods=['GET'])
def single_planet(planets_id):
    
    planet = Planets.query.filter_by(id=planets_id).first()
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    return jsonify(planet.serialize()), 200


#POST Planeta
@app.route('/planets', methods=['POST'])
def create_planet():

    request_body_planet = request.get_json()

    newPlanet = Planets(
        name=request_body_planet["name"],
        url=request_body_planet["url"],
        diameter=request_body_planet["diameter"],
        population=request_body_planet["population"],
        climate=request_body_planet["climate"],
        terrain=request_body_planet["terrain"],
        surfaceWater=request_body_planet["surfaceWater"],
        rotationPeriod=request_body_planet["rotationPeriod"],
        orbitalPeriod=request_body_planet["orbitalPeriod"],
        gravity=request_body_planet["gravity"],
        films=request_body_planet["films"],
        created=request_body_planet["created"],
        edited=request_body_planet["edited"]
        )
    db.session.add(newPlanet)
    db.session.commit()

    return jsonify("New planet added successfully"), 200



#DELETE PLANETA
@app.route('/planets/<int:planets_id>', methods=['DELETE'])
def delete_planet(planets_id):
    thatPlanet = Planets.query.get(planets_id)
    if thatPlanet is None:
        raise APIException('Planet not found', status_code=404)
    db.session.delete(thatPlanet)
    db.session.commit()

    return jsonify("Planet deleted"), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

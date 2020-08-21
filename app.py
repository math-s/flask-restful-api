from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['JWT_SECRET_KEY'] = 'key@evolux'

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


# COMMANDS FOR DATABASE
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('DB created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    new_number = DidNumber(value="+55 84 91234-4321",
                           monthyPrice=0.03,
                           setupPrice=3.40,
                           currency="U$")
    new_user = User(name="Math",
                    email="naotem@naotem.com",
                    password="1234")
    db.session.add(new_number)
    db.session.add(new_user)
    db.session.commit()
    print('DB seeded!')
    
# END COMMANDS FOR DATABASE


# ROUTES FOR API
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'), 404


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough!")
    
    
@app.route('/did_number', methods=['GET'])
def did_number_list_all():
    did_number_list = DidNumber.query.all()
    result = dids_number_schema.dump(did_number_list)
    return jsonify(result)
    
    
@app.route('/did_number_detail/<int:did_number_id>', methods=['GET'])
def did_number_detail_by_id(did_number_id: int):
    did_number_search = DidNumber.query.filter_by(id=did_number_id).first()
    if did_number_search:
        result = did_number_schema.dump(did_number_search)
        return jsonify(result)
    else:
        return jsonify(message='This number was not found!'), 404
    

@app.route('/add_number', methods=['POST'])
@jwt_required
def add_number():
    if request.is_json:
        value = request.json['value']
        monthyPrice = request.json['monthyPrice']
        setupPrice = request.json['setupPrice']
        currency = request.json['currency']
    else:
        value = request.form['value']
        monthyPrice = float(request.form['monthyPrice'])
        setupPrice = float(request.form['setupPrice'])
        currency = request.form['currency']
    test = DidNumber.query.filter_by(value=value).first()
    if test:
        return jsonify(message='This number is already registered!'), 409
    else:
        new_did_number = DidNumber(value=value,
                                   monthyPrice=monthyPrice,
                                   setupPrice=setupPrice,
                                   currency=currency)
        db.session.add(new_did_number)
        db.session.commit()
        return jsonify(message='New number added!')
    

@app.route('/update_number', methods=['PUT', 'POST'])
@jwt_required
def update_number():
    number_id = int(request.form['id'])
    did_number = DidNumber.query.filter_by(id=number_id).first()
    test = DidNumber.query.filter_by(value=request.form['value'])

    if did_number:
        did_number.value = request.form['value']
        did_number.monthyPrice = float(request.form['monthyPrice'])
        did_number.setupPrice = float(request.form['setupPrice'])
        did_number.currency = request.form['currency']
        db.session.commit()
        return jsonify(message='You updated the number'), 202
    else:
        return jsonify(message='The number does not exist!'), 404


@app.route('/delete/<int:did_number_id>', methods=['DELETE'])
@jwt_required
def delete_number(did_number_id: int):
    did_number = DidNumber.query.filter_by(id=did_number_id)
    if did_number:
        db.session.delete(did_number)
        db.session.commit()
        return jsonify(message='You deleted the number!')
    else:
        return jsonify(message='That number does not exist!'), 404
    
    
@app.route('/register', methods=['POST'])
def register():
    if request.is_json:
        email = request.json['email']
        name = request.json['name']
        password = request.json['password']
    else:
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
    
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='This email is already registered!'), 409
    else:
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message='User created!')
    

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']
    
    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Logged in!', access_token=access_token)
    else:
        return jsonify(message='That didnt work'), 401
    
# END ROUTES FOR API


# MODELS with SQLAlchemy
class DidNumber(db.Model):
    __tablename__ = 'did'
    id = Column(Integer, primary_key=True)
    value = Column(String, unique=True)
    monthyPrice = Column(Float)
    setupPrice = Column(Float)
    currency = Column(String)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    
# END MODELS


# SCHEMA with marshmallow
class DidNumberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'value', 'monthyPrice', 'setupPrice', 'currency')

# END SCHEMA


did_number_schema = DidNumberSchema()
dids_number_schema = DidNumberSchema(many=True)


if __name__ == '__main__':
    app.run(port=5000, debug=True)

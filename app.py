from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
db = SQLAlchemy(app)


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
    db.session.add(new_number)
    db.session.commit()
    print('DB seeded!')
    
# END COMMANDS FOR DATABASE


# ROUTES FOR API
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the Planetary API.'), 200


@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'), 404


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough!")


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry " + name + ", you are not old enough."), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enough!")
    
# END ROUTES FOR API


# MODELS
class DidNumber(db.Model):
    __tablename__ = 'did'
    id = Column(Integer, primary_key=True)
    value = Column(String, unique=True)
    monthyPrice = Column(Float)
    setupPrice = Column(Float)
    currency = Column(String)
    
# END MODELS


if __name__ == '__main__':
    app.run(port=5000, debug=True)

import os
import datetime
import flask
import flask_sqlalchemy
import flask_restless
from hashlib import md5

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = flask_sqlalchemy.SQLAlchemy(app)

# Create the Flask-Restless API manager.
api_manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Define Flask-SQLALchemy models.
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True)
    password = db.Column(db.Unicode)
    firstname = db.Column(db.Unicode)
    lastname = db.Column(db.Unicode)
    email = db.Column(db.Unicode, unique=True)
    phone = db.Column(db.Unicode)
    order = db.relationship('Order', backref='customer', uselist=False)


class Deliveryperson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True)
    password = db.Column(db.Unicode)
    firstname = db.Column(db.Unicode)
    lastname = db.Column(db.Unicode)
    email = db.Column(db.Unicode, unique=True)
    phone = db.Column(db.Unicode)
    on_duty = db.Column(db.Boolean, default=False)
    assigned_order = db.relationship('Order', lazy='dynamic')


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu = db.relationship('Restaurant', backref='menu', uselist=False)
    menu_items = db.relationship('Menuitem', backref="menu", lazy='dynamic')


class Menuitem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    name = db.Column(db.Unicode)
    price = db.Column(db.Float)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    delivery_address = db.Column(db.Unicode)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    deliveryperson_id = db.Column(db.Integer, db.ForeignKey('deliveryperson.id'))
    status = db.Column(db.Unicode, default="open")
    order_items = db.relationship('Orderitem', backref="order", lazy='dynamic')


class Orderitem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    menuitem_id = db.Column(db.Integer, db.ForeignKey('menuitem.id'))
    Menuitem = db.relationship('Menuitem', uselist=False)
    quantity = db.Column(db.Integer, default=1)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True)
    password = db.Column(db.Unicode)
    name = db.Column(db.Unicode)
    address = db.Column(db.Unicode)
    owner = db.Column(db.Unicode)
    email = db.Column(db.Unicode, unique=True)
    phone = db.Column(db.Unicode)
    subscription_type = db.Column(db.Unicode)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    orders = db.relationship('Order', backref="restaurant", lazy='dynamic')


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode)
    token = db.Column(db.Unicode)


# Create the database tables.
db.create_all()

# Hardcode a few db entries.
menu1 = Menu()
db.session.add(menu1)
menu_item1 = Menuitem(menu_id=1, name="Pizza Margherita", price=6.99)
db.session.add(menu_item1)
menu_item2 = Menuitem(menu_id=1, name="Pizza Salami", price=7.99)
db.session.add(menu_item2)
restaurant1 = Restaurant(username=u'donenzo',
                         password=u'admin',
                         name='Panuccis Pizza',
                         address='Time Square 1, New New York',
                         owner="Enzo Panucci",
                         email="panuccis@example.com",
                         phone="+1 555 123456",
                         subscription_type="Display only",
                         menu_id=1
                         )
db.session.add(restaurant1)
restaurant2 = Restaurant(username=u'veganpower',
                         password=u'admin',
                         name='Hipster Hut',
                         address='Somewhere',
                         owner="Ernst Freigeist",
                         email="veganpower@example.com",
                         phone="+49 213 12321",
                         subscription_type="Premium",
                         )
db.session.add(restaurant2)
db.session.commit()

# Authentication
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    username = flask.request.json.get('username')
    password = flask.request.json.get('password')

    # check if the user is in any of the tables
    matches = Customer.query.filter_by(username=username,
                                       password=password).all()
    matches += Deliveryperson.query.filter_by(username=username,
                                              password=password).all()
    matches += Restaurant.query.filter_by(username=username,
                                          password=password).all()
    if len(matches) > 0:
        # generate a token (this is obviously an insecure way of doing so)
        token = md5(password.encode('utf-8')).hexdigest()
        # store token in database
        dbentry = Token(username=username, token=token)
        db.session.add(dbentry)
        db.session.commit()

        # hand the token to the API client
        return flask.jsonify(token=token)

    # no matching user found
    raise flask_restless.ProcessingException(description='Not Authorized', code=401)

# create the API for User with the authentication guard.
def auth_func(**kw):
    token = flask.request.headers.get('Authorization')
    # search token in databasae
    matches = Token.query.filter_by(token=token).all()
    if len(matches) == 0:
        raise flask_restless.ProcessingException(description='Not Authorized', code=401)


# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
api_manager.create_api(Customer,
                       methods=['GET', 'POST', 'PUT', 'DELETE'],
                       exclude_columns=['password'],
                       preprocessors=dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func],
                                          PUT_SINGLE=[auth_func], PUT_MANY=[auth_func],
                                          DELETE_SINGLE=[auth_func], DELETE_MANY=[auth_func]))
api_manager.create_api(Deliveryperson,
                       methods=['GET', 'POST', 'PUT', 'DELETE'],
                       exclude_columns=['password'],
                       preprocessors=dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func],
                                          PUT_SINGLE=[auth_func], PUT_MANY=[auth_func],
                                          DELETE_SINGLE=[auth_func], DELETE_MANY=[auth_func]))
api_manager.create_api(Menu,
                       methods=['GET', 'POST', 'PUT', 'DELETE'],
                       url_prefix='/api/restaurant',
                       preprocessors=dict(POST_SINGLE=[auth_func], POST_MANY=[auth_func],
                                          PUT_SINGLE=[auth_func], PUT_MANY=[auth_func],
                                          DELETE_SINGLE=[auth_func], DELETE_MANY=[auth_func]))
api_manager.create_api(Menuitem,
                       methods=['GET', 'POST', 'PUT', 'DELETE'],
                       url_prefix='/api/restaurant',
                       preprocessors=dict(POST_SINGLE=[auth_func], POST_MANY=[auth_func],
                                          PUT_SINGLE=[auth_func], PUT_MANY=[auth_func],
                                          DELETE_SINGLE=[auth_func], DELETE_MANY=[auth_func]))
api_manager.create_api(Order,
                       methods=['GET', 'POST', 'PUT'],
                       preprocessors=dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func],
                                          POST=[auth_func],
                                          PUT_SINGLE=[auth_func], PUT_MANY=[auth_func]))
api_manager.create_api(Restaurant,
                       methods=['GET', 'PUT', 'DELETE'],
                       exclude_columns=['password'],
                       preprocessors=dict(PUT_SINGLE=[auth_func], PUT_MANY=[auth_func],
                                          DELETE_SINGLE=[auth_func], DELETE_MANY=[auth_func]))

# start the flask loop
app.run()

import datetime
import flask
import flask_sqlalchemy
import flask_restless

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = flask_sqlalchemy.SQLAlchemy(app)

# Create Flask-SQLALchemy models 
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True)
    firstname = db.Column(db.Unicode)
    lastname = db.Column(db.Unicode)
    email = db.Column(db.Unicode)
    phone = db.Column(db.Unicode)
    orders = db.relationship('Order', backref="customer", lazy='dynamic')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    delivery_address = db.Column(db.Unicode, default="open")
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    status = db.Column(db.Unicode)
    # TODO order_items


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True)
    name = db.Column(db.Unicode)
    address = db.Column(db.Unicode)
    owner = db.Column(db.Unicode)
    email = db.Column(db.Unicode)
    phone = db.Column(db.Unicode)
    subscription_type = db.Column(db.Unicode)
    # TODO menu
    orders = db.relationship('Order', backref="restaurant", lazy='dynamic')


# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Customer, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Order, methods=['GET', 'POST'])
manager.create_api(Restaurant, methods=['GET', 'POST', 'PUT', 'DELETE'])

# start the flask loop
app.run()

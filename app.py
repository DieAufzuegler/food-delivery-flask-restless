import os
import datetime
import flask
import flask_login
import flask_sqlalchemy
import flask_restless
import flask_wtf
import wtforms

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.urandom(24)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = flask_sqlalchemy.SQLAlchemy(app)

# Create the Flask-Restless API manager and Flask-Login manager.
api_manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
login_manager = flask_login.LoginManager()
login_manager.setup_app(app)

# Define Flask-SQLALchemy models
class Customer(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True)
    password = db.Column(db.Unicode)
    firstname = db.Column(db.Unicode)
    lastname = db.Column(db.Unicode)
    email = db.Column(db.Unicode, unique=True)
    phone = db.Column(db.Unicode)
    orders = db.relationship('Order', backref="customer", lazy='dynamic')


class Deliveryperson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True)
    password = db.Column(db.Unicode)
    firstname = db.Column(db.Unicode)
    lastname = db.Column(db.Unicode)
    email = db.Column(db.Unicode, unique=True)
    phone = db.Column(db.Unicode)
    on_duty = db.Column(db.Boolean, default=False)
    has_order_assigned = db.Column(db.Boolean, default=False)
    assigned_order = db.Column(db.Integer, db.ForeignKey('order.id'))
    #assigned_order = db.relationship('Order', backref="assigned_deliveryperson", uselist=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    delivery_address = db.Column(db.Unicode, default="open")
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    #deliveryperson_id = db.Column(db.Integer, db.ForeignKey('deliveryperson.id'))
    status = db.Column(db.Unicode)
    # TODO order_items


class Restaurant(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True)
    password = db.Column(db.Unicode)
    name = db.Column(db.Unicode)
    address = db.Column(db.Unicode)
    owner = db.Column(db.Unicode)
    email = db.Column(db.Unicode, unique=True)
    phone = db.Column(db.Unicode)
    subscription_type = db.Column(db.Unicode)
    # TODO menu
    orders = db.relationship('Order', backref="restaurant", lazy='dynamic')


# Create the database tables.
db.create_all()

# hardcore a few db entries

restaurant1 = Restaurant(username=u'donenzo',
                         password=u'admin',
                         name='Panuccis Pizza',
                         address='Time Square 1, New New York',
                         owner="Enzo Panucci",
                         email="panuccis@example.com",
                         phone="+1 555 123456",
                         subscription_type="Display only",
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

# create user loader
@login_manager.user_loader
def load_user(userid):
    return Restaurant.query.get(userid)

# create the login form.
class LoginForm(flask_wtf.Form):
    username = wtforms.TextField('username')
    password = wtforms.PasswordField('password')
    submit = wtforms.SubmitField('Login')

# custom URIs
@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #
        # you would check username and password here...
        #
        username, password = form.username.data, form.password.data
        matches = Restaurant.query.filter_by(username=username,
                                             password=password).all()
        if len(matches) > 0:
            flask_login.login_user(matches[0])
            return flask.redirect(flask.url_for('index'))
        flask.flash('Username and password pair not found')
    return flask.render_template('login.html', form=form)

# create the API for User with the authentication guard.
def auth_func(**kw):
    if not flask_login.current_user.is_authenticated:
        raise flask_restless.ProcessingException(description='Not Authorized', code=401)


# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
api_manager.create_api(Customer,
                       methods=['GET', 'POST', 'PUT', 'DELETE'],
                       exclude_columns=['password'],
                       preprocessors=dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func]))
api_manager.create_api(Deliveryperson, methods=['GET', 'POST', 'PUT', 'DELETE'], exclude_columns=['password'])
api_manager.create_api(Order, methods=['GET', 'POST'])
api_manager.create_api(Restaurant, methods=['GET', 'PUT', 'DELETE'], exclude_columns=['password'])

# start the flask loop
app.run()

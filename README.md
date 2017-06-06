Prototype of a REST API for a Foodora-like company built with Flask-restless.

Student project for the "Software Engineering - Design" course at FRA-UAS during the summer semester 2017.

## Requirements
* python3
* flask
* flask-restless
* flask-sqlalchemy

### Install requirements in Fedora 25
```sudo dnf install python3 python3-flask python3-pip
sudo pip3 install flask-restless
```

### Install requirements in Ubuntu 17.04
```sudo apt install python3 python3-flask python3-flask-sqlalchemy python3-pip
sudo pip3 install flask-restless
```

## Starting the API server
Clone or download the repository and then run
```cd food-delivery-flask-restless/
python3 app.py
```

## Example requests
Once the API server is running you can start an automated presentation by running `python3 example-requests.py`

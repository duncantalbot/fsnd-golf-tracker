# Golf Tracker API FSND

## About

The project provides the backbone to create and visualize a family tree. Members can add in players and there events including information e.g practice, round info, scores. Guests are allowed to come in and view the persons information. 

https://fsnd-golf-tracker.herokuapp.com

## API

To use the API users need to be authenticated. Users can either be a guest or a member for access. Information about API can be viewed below. A Postman collection is also provided for testing endpoints.

### Retreiving data (Guests and members)

**GET** `/persons`

Retrieves a list of current golfers

```
curl -X GET \
  https://fsnd-golf-tracker.herokuapp.com/persons \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

**GET** `/events`

Retrieves a list of events / activities

```
curl -X GET \
  https://fsnd-golf-tracker.herokuapp.com/events \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

### Managing golf activity data (Members only)

**POST** `/persons`

Add a new person

```
curl -X POST \
  https://fsnd-golf-tracker.herokuapp.com/persons \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "firstname": "Tiger",
    "lastname": "Woods",
    "handicap": "4.2"
}'
```

**PATCH** `/persons/<id>`

Change information for a given person

```
curl -X PATCH \
  https://fsnd-golf-tracker.herokuapp.com/persons/1 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "firstname": "Tiger"
}'
```

**DELETE** `/persons/<id>`

Delete a given person

```
curl -X DELETE \
  https://fsnd-golf-tracker.herokuapp.com/persons/5 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN> ' \

```

**POST** `/events`

Add a new event

```
curl -X POST \
  https://fsnd-family-tree.herokuapp.com/persons \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "event_type": "chipping",
    "date": "01.01.2021"
}'
```

## Installation

The following section explains how to set up and run the project locally.

### Installing Dependencies

The project requires Python 3.6. Using a virtual environment is recommended. Set up the project as follows:

```
Setup virtual environment
install requirements.txt

```

### Database Setup

With Postgres running, create a database:

```

sudo -u postgres createdb golftracker

```

### Running the server

To run the server, first set the environment variables, then execute:

```bash
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql:///golftracker"
python manage.py runserver
```

## Testing

To test the API, first create a test database in postgres and then execute the tests as follows:

```
sudo -u postgres createdb golftracker_test
python test_app.py
```
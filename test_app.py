import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from models import Person, Event


MEMBER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhEZnpkaTJ6NHY5UHg2aGdmczZZQiJ9.eyJpc3MiOiJodHRwczovL2R1bmNhbnRhbGJvdC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZjODc4MGI0Y2QzODkwMDZmYTMzYWE2IiwiYXVkIjpbImh0dHBzOi8vZ29sZnRyYWNrZXIiLCJodHRwczovL2R1bmNhbnRhbGJvdC5hdS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjA2OTkzMjAxLCJleHAiOjE2MDcwNzk2MDEsImF6cCI6IjBvemlqTE9NTFdpSUpteE1Td1JZTFp2b3puNTRHRW5rIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpldmVudHMiLCJnZXQ6ZXZlbnRzIiwicG9zdDpldmVudHMiLCJ1cGRhdGU6ZXZlbnRzIl19.Aw0hQf-Fx7VcbzZ0IDzpcagOm8twZ1pbR3rzsh6tTXh9YYHKdW9ioXPmVzGRFOyc_Vdl8MdYPz23RhMuq9YiPjb6Da-xLBkNCR5YU9Ldg_tCsAvHAtHjK_s-51fm7iwzhwCxjQ4YzM-ADQ6_FPrAri6NkKjJ2lMJuKWLDQ6s3V4G1zoKMXmlGveqk-ynUNqgmO_NaFITucc5sv0nSq0VzujsJYFXeH9XQu2LGHWNdZrGNH9sTSDHySR1bBcSWdYRZv39bOyXkqVMLLryPqWBnU3Rj5QlQKgRBXkBHKW4qDszGaKtLSDHjruSbnASL04dCof5Z7W0jTzC8oqSMxXcUw'


class BasicTest(unittest.TestCase):
    def setUp(self):

        app.config.from_object('config.TestingConfig')
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///golftracker"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.client = app.test_client()
        self.headers = {'Content-Type': 'application/json'}

        db.drop_all()
        db.create_all()

    # executed after each test
    def tearDown(self):
        pass

    '''
    Persons
    '''

    def test_public_add_person(self):
        new_person = {
            "firstname": "Tiger",
            "lastname": "Woods",
            "handicap": "4.2"
        }

        res = self.client.post('/persons', json=new_person)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_member_add_person(self):
        new_person = {
            "firstname": "Tiger",
            "lastname": "Woods",
            "handicap": "4.2"
        }
        self.headers.update({'Authorization': 'Bearer ' + MEMBER_TOKEN})

        res = self.client.post('/persons', json=new_person, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_get_persons(self):
        res = self.client.get('/persons')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_member_get_persons(self):
        self.headers.update({'Authorization': 'Bearer ' + MEMBER_TOKEN})

        res = self.client.get('/persons', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_update_person(self):
        updated_person = {
            "firstname": "Tiger"
        }

        res = self.client.patch('/persons/1', json=updated_person)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_member_update_person(self):
        person = Person(
            firstname='Tiger',
            lastname='Woods',
            handicap='4.2')
        person.insert()
        person_id = person.id

        updated_person = {
            "firstname": "Tiger"
        }

        self.headers.update({'Authorization': 'Bearer ' + MEMBER_TOKEN})

        res = self.client.patch(f'/persons/{person_id}', json=updated_person, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_delete_person(self):

        res = self.client.delete('/persons/1', )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_member_delete_person(self):
        person = Person(
            firstname='Tiger',
            lastname='Woods',
            handicap='4.2')
        person.insert()
        person_id = person.id

        self.headers.update({'Authorization': 'Bearer ' + MEMBER_TOKEN})

        res = self.client.delete(f'/persons/{person_id}', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete'], str(person_id))

    '''
    EVENTS
    '''
    def test_public_add_event(self):
        new_event = {
            "event_type": "chipping",
            "date": "01.12.1900",
            "description": "2 hours chipping"
        }

        res = self.client.post('/events', json=new_event)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_member_add_event(self):
        new_event = {
            "event_type": "chipping",
            "date": "01.12.1900",
            "description": "2 hours chipping"
        }
        self.headers.update({'Authorization': 'Bearer ' + MEMBER_TOKEN})

        res = self.client.post('/events', json=new_event, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_get_events(self):
        res = self.client.get('/events')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_member_get_events(self):
        self.headers.update({'Authorization': 'Bearer ' + MEMBER_TOKEN})

        res = self.client.get('/events', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

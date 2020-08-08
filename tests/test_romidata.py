import unittest
import sys
from os.path import abspath

sys.path.append(abspath('..'))
from romidata.db import Database
from romidata.impl import DefaultFactory



class TestRomiData(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRomiData, self).__init__(*args, **kwargs)
        self.factory = DefaultFactory()
    
    def test_person_create_ok(self):
        person = self.factory.create("Person", {
            "id": "id",
            "short_name": "short_name",
            "name": "name",
            "email": "email",
            "affiliation": "affiliation",
            "role": "role" })
        self.assertEqual(person.id, 'id')
        self.assertEqual(person.short_name, "short_name")
        self.assertEqual(person.name, "name")
        self.assertEqual(person.email, "email")
        self.assertEqual(person.affiliation, "affiliation")
        self.assertEqual(person.role, "role")

    def test_person_create_missing_id(self):
        with self.assertRaises(KeyError):
            person = self.factory.create("Person", {
                "short_name": "short_name",
                "name": "name",
                "email": "email",
                "affiliation": "affiliation",
                "role": "role" })

    def test_person_create_missing_short_name(self):
        with self.assertRaises(KeyError):
            person = self.factory.create("Person", {
                "id": "id",
                "name": "name",
                "email": "email",
                "affiliation": "affiliation",
                "role": "role" })

    def test_person_create_missing_name(self):
        with self.assertRaises(KeyError):
            person = self.factory.create("Person", {
                "id": "id",
                "short_name": "short_name",
                "email": "email",
                "affiliation": "affiliation",
                "role": "role" })

    def test_person_create_missing_email(self):
        with self.assertRaises(KeyError):
            person = self.factory.create("Person", {
                "id": "id",
                "short_name": "short_name",
                "name": "name",
                "affiliation": "affiliation",
                "role": "role" })

    def test_person_create_missing_affiliation(self):
        with self.assertRaises(KeyError):
            person = self.factory.create("Person", {
                "id": "id",
                "short_name": "short_name",
                "email": "email",
                "name": "name",
                "role": "role" })

    def test_person_create_missing_role(self):
        with self.assertRaises(KeyError):
            person = self.factory.create("Person", {
                "id": "id",
                "short_name": "short_name",
                "email": "email",
                "name": "name",
                "affiliation": "affiliation" })

if __name__ == '__main__':
    unittest.main()

    

import unittest
import sys
from os.path import abspath

sys.path.append(abspath('..'))
from romidata2.db import Database
from romidata2.impl import DefaultFactory



class TestRomiData(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRomiData, self).__init__(*args, **kwargs)
        self.factory = DefaultFactory()
    
    def test_person_create_ok(self):
        values = {
            "id": "id",
            "short_name": "short_name",
            "name": "name",
            "email": "email",
            "affiliation": "affiliation",
            "role": "role" }
        person = self.factory.create("Person", values)
        self.assertEqual(person.id, 'id')
        self.assertEqual(person.short_name, "short_name")
        self.assertEqual(person.name, "name")
        self.assertEqual(person.email, "email")
        self.assertEqual(person.affiliation, "affiliation")
        self.assertEqual(person.role, "role")

    def test_person_serialize_ok(self):
        values = {
            "id": "id",
            "short_name": "short_name",
            "name": "name",
            "email": "email",
            "affiliation": "affiliation",
            "role": "role" }
        person = self.factory.create("Person", values)
        self.assertEqual(person.serialize(), values)

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
    
    def test_file_create_ok(self):
        values = {
            "id": "id",
            "source_name": "source_name",
            "source_id": "source_id",
            "short_name": "short_name",
            "path": "path",
            "mimetype": "mimetype" }
        ifile = self.factory.create("File", values)
        self.assertEqual(ifile.id, 'id')
        self.assertEqual(ifile.source_name, "source_name")
        self.assertEqual(ifile.source_id, "source_id")
        self.assertEqual(ifile.short_name, "short_name")
        self.assertEqual(ifile.path, "path")
        self.assertEqual(ifile.mimetype, "mimetype")

    def test_file_seriaize_ok(self):
        values = {
            "id": "id",
            "source_name": "source_name",
            "source_id": "source_id",
            "short_name": "short_name",
            "path": "path",
            "mimetype": "mimetype" }
        ifile = self.factory.create("File", values)
        self.assertEqual(ifile.serialize(), values)

    def test_file_create_missing_id(self):
        values = {
            "source_name": "source_name",
            "source_id": "source_id",
            "short_name": "short_name",
            "path": "path",
            "mimetype": "mimetype" }
        with self.assertRaises(KeyError):
            ifile = self.factory.create("File", values)

    def test_file_create_missing_source_name(self):
        values = {
            "id": "id",
            "source_id": "source_id",
            "short_name": "short_name",
            "path": "path",
            "mimetype": "mimetype" }
        with self.assertRaises(KeyError):
            ifile = self.factory.create("File", values)

    def test_file_create_missing_source_id(self):
        values = {
            "id": "id",
            "source_name": "source_name",
            "short_name": "short_name",
            "path": "path",
            "mimetype": "mimetype" }
        with self.assertRaises(KeyError):
            ifile = self.factory.create("File", values)

    def test_file_create_missing_short_name(self):
        values = {
            "id": "id",
            "source_name": "source_name",
            "source_id": "source_id",
            "path": "path",
            "mimetype": "mimetype" }
        with self.assertRaises(KeyError):
            ifile = self.factory.create("File", values)

    def test_file_create_missing_path(self):
        values = {
            "id": "id",
            "source_name": "source_name",
            "source_id": "source_id",
            "short_name": "short_name",
            "mimetype": "mimetype" }
        with self.assertRaises(KeyError):
            ifile = self.factory.create("File", values)

    def test_file_create_missing_mimetype(self):
        values = {
            "id": "id",
            "source_name": "source_name",
            "source_id": "source_id",
            "short_name": "short_name",
            "path": "path" }
        with self.assertRaises(KeyError):
            ifile = self.factory.create("File", values)

        
if __name__ == '__main__':
    unittest.main()

    

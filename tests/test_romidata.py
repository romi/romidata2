import unittest
import sys
from os.path import abspath
import copy

sys.path.append(abspath('..'))
from romidata2.db import Database
from romidata2.impl import DefaultFactory



class TestRomiData(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRomiData, self).__init__(*args, **kwargs)
        self.factory = DefaultFactory()

        self.values = {}

        self.values["Person"] = {
            "id": "id",
            "short_name": "short_name",
            "name": "name",
            "email": "email",
            "affiliation": "affiliation",
            "role": "role" }
        
        self.values["File"] = {
            "id": "id",
            "source_name": "source_name",
            "source_id": "source_id",
            "short_name": "short_name",
            "path": "path",
            "mimetype": "mimetype" }

        self.values["Parameters"] = {
            "key1": "value1",
            "key2": "value2" }

        self.values["SoftwareModule"] = {
            "id": "id",
            "version": "version",
            "repository": "repository",
            "branch": "branch"
        }

        self.values["ScanPath"] = {
            "short_name": "short_name",
            "type": "type",
            "parameters": { "key1": "value1" }
        }

        self.values["Task"] = {
            "id": "id",
            "short_name": "short_name",
            "state": "Defined",
            "software_module": {
                "id": "id",
                "version": "version",
                "repository": "repository",
                "branch": "branch"
            },
            "parameters": { "key1": "value1" },
            "input_files": ["id1", "id2"],
            "output_files": ["id1", "id2"],
            "log_file": "id"
        }

    ####

    def __test_create_ok(self, classname, values):
        obj = self.factory.create(classname, values)
        for key in values.keys():
            # Can't test composite values, yet. The
            # __test_serialize_ok() handles composite values, though.
            if ((type(values[key]) == str)
                or (type(values[key]) == int)
                or (type(values[key]) == float)):
                value = getattr(obj, key)
                self.assertEqual(value, values[key])

    def __test_serialize_ok(self, classname, values):
        obj = self.factory.create(classname, values)
        self.assertEqual(obj.serialize(), values)

    def __test_clone_ok(self, classname, values, skip, replace):
        obj = self.factory.create(classname, values)
        clone = obj.clone()
        copied_values = copy.copy(values)
        serialized_values = clone.serialize()
        for key in skip:
            serialized_values.pop(key)
            copied_values.pop(key)
        for key in replace.keys():
            copied_values[key] = replace[key]
        self.assertEqual(serialized_values, copied_values)

    def __test_missing_property(self, classname, values, prop):
        copied_values = copy.copy(values)
        copied_values.pop(prop)
        with self.assertRaises(KeyError):
            obj = self.factory.create(classname, copied_values)

    def __test_missing_properties(self, classname, values):
        for prop in values.keys():
            self.__test_missing_property(classname, values, prop)
        
    def __test_datatype(self, classname, skip=[], replace={}):
        self.__test_create_ok(classname, self.values[classname])
        self.__test_serialize_ok(classname, self.values[classname])
        self.__test_clone_ok(classname, self.values[classname], skip, replace)
        self.__test_missing_properties(classname, self.values[classname])

    ####
    
    def test_person(self):
        self.__test_datatype("Person")

    def test_file(self):
        self.__test_datatype("File")

    def test_softwaremodule(self):
        self.__test_datatype("SoftwareModule")

    def test_scanpath(self):
        self.__test_datatype("ScanPath")

    def test_task(self):
        self.__test_datatype("Task", ["id"], {"log_file": "", 'input_files': []})

    # Parameters
    
    def test_parameters(self):
        values = self.values["Parameters"]
        obj = self.factory.create("Parameters", values)
        self.assertEqual(obj.get_value("key1"), "value1")
        self.assertEqual(obj.get_value("key2"), "value2")
        self.assertEqual(obj.serialize(), values)
        self.assertEqual(obj.values, values)

        
if __name__ == '__main__':
    unittest.main()

    

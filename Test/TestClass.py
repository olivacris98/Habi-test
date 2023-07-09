import unittest
from Utils.Tools import Tools
from Utils.Database import Database


class TestClass(unittest.TestCase):
    def test_lambda(self):
        """
        Test lambda property in db
        this test is responsible for the MS using a serverless lambda
        that get all property filter by requests data or json_data_file
        you can see the json_file in Utils/data.json
        """
        conn = Database()
        from Classes.Property import Property
        instance_of = Property(conn)

        # its take an json data in method of class or event
        response = instance_of.get(event={})

        # test
        self.assertEqual(
            response.get("statusCode"), 200,
            "Tests lambda statusCode must be 200"
        )

    def test_json_data(self):
        tools = Tools()
        json_data = tools.get_json_data()
        self.assertIsInstance(
            json_data, dict, "Test json data passed must be a dict"
        )

    def get_event_data(self):
        """
        this method return a simulate event data you can use only
        declaring a var: event = self.get_event_data()
        in test_lambda function
        """
        return {
            "queryStringParameters": {
                "status_id": 2  # for test
            }
        }


if __name__ == '__main__':
    unittest.main()

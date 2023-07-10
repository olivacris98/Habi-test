import unittest
import json
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
            response.get("statusCode"), 200, "Tests lambda statusCode must be 200"
        )

    def test_block_numbers_lambda(self):
        """
        Test lambda block numbers
        this test is responsible for the MS using a serverless lambda
        that process an list of data an wait a response
        depend of list of data
        you can see all documentation in lambda_function into BlockNumber class
        """
        from Classes.BlockNumber import BlockNumber
        block = BlockNumber()

        # this event its manually
        event = self.get_event_data("POST")
        result = block.operation_block(event)
        self.assertEqual(
            json.loads(result["body"]), "12 x 34", "Test no passed"
        )

    def test_json_data(self):
        """
        this validate if json data is a dict
        """
        tools = Tools()
        json_data = tools.get_json_data()
        self.assertIsInstance(
            json_data, dict, "Test json data passed must be a dict"
        )

    def test_block_numbers(self):
        """
        this method return string of data depend of operation in list data
        arg: list of data
        """
        tools = Tools()
        input_data = [2, 1, 0, 0, 3, 4]
        response = tools.process_block(input_data)
        self.assertEqual(response, "12 x 34", "Test no passed")

    def test_empty_list(self):
        """
        this method return an context exception
        if the list of data not contain info
        arg: list of data
        """
        tools = Tools()
        input_data = {"list_of_data": []}
        with self.assertRaises(ValueError) as context:
            tools.process_input(input_data)
        self.assertEqual(
            str(context.exception), "invalid parameters check README.md"
        )

    def test_list_numbers(self):
        """
        this method return an context exception
        if the list of data contain items distinct io integer value
        arg: list of data
        """
        tools = Tools()
        input_data = {"list_of_data": ["item", "x", 0, 0, 3, 4]}
        with self.assertRaises(ValueError) as context:
            tools.process_input(input_data)
        self.assertEqual(
            str(context.exception),
            "The list must contain only numerical values"
        )

    def get_event_data(self, method: str = "GET"):
        """
        this method return a simulate event data you can use only
        declaring a var: event = self.get_event_data(method=["GET", "POST"])
        in test_lambda function
        """
        event = {"httpMethod": method}

        # only for post test
        list_of_data = [2, 1, 0, 0, 3, 4]

        event.update(
            {"queryStringParameters": {"status_id": 3}}
            if method == "GET" else {"body": {"list_of_data": list_of_data}}
        )
        return event


if __name__ == "__main__":
    unittest.main()

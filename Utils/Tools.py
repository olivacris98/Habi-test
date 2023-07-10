import json
from Utils.Constant import ONLY_VIEW_STATUS, OPTIONAL_PARAMS


class Tools:
    def __init__(self):
        pass

    @classmethod
    def get_request_method(cls, event: dict) -> dict:
        """
        Get the request method from the event.
        Args:
            event (dict): The event object.
        Returns:
            dict: The request data.
        """
        input_type = {
            'GET':      'queryStringParameters',
            'POST':     'body',
        }

        # getting a selected method in event
        method = input_type.get(event.get("httpMethod", "GET"))  # default test
        return cls.get_input_data(event.get(method))

    @staticmethod
    def get_json_data() -> dict:
        """
        Load JSON data from the file.
        Returns:
            dict: The JSON data.
        """
        with open('Utils/data.json', 'r') as file:
            return json.load(file)

    @staticmethod
    def get_condition(conditions: dict) -> str:
        """
        Generate the WHERE condition based on the given conditions.
        Args:
            conditions (dict): The conditions dictionary.
        Returns:
            str: The generated WHERE condition.
        """
        where_conditions = [
            "WHERE sh.status_id NOT IN (1, 2)"
        ]
        for key, value in conditions.items():

            # getting filters
            if key == 'status_id' and int(value) in ONLY_VIEW_STATUS:
                where_conditions.append(f"sh.{key} = {value}")

            elif key in OPTIONAL_PARAMS:
                where_conditions.append(
                    f"p.{key} LIKE '%{str(value).lower()}%'"
                )

        return (
            " AND ".join(where_conditions)
            if where_conditions else ""
        )

    @classmethod
    def process_input(cls, request: dict) -> bool:
        """
        this method ensures that the request is the expected one
        Returns:
            bool: True / False
        Raises: ValueError
        """
        list_of_data = request.get('list_of_data', [])

        if not len(list_of_data):
            raise ValueError("invalid parameters check README.md")

        # validate if list of number
        if not cls.validate_list(list_of_data):
            raise ValueError("The list must contain only numerical values")
        return True

    @classmethod
    def validate_list(cls, list_of_data: list):
        """
        Validate if the input is a list of numbers.
        Args:
            input_list (list): The input list to validate.
        Returns:
            bool: True if the input is a valid list of numbers,
            False otherwise.
        """
        max_value = 9
        return isinstance(list_of_data, list) and all(
            isinstance(item, (int, float))
            and item <= max_value for item in list_of_data
        )

    @classmethod
    def process_block(cls, data_list: list) -> str:
        """
        this function keep validate by segments a list of data number
        considering that:
          - an list of data cannot start 0 and end 0
          - if last_value = 0 and next value = 0 into list_of_data then this
            will insert "x"
          - the segments will separate by "" for better read compression
        """
        if data_list[-1] == 0 and data_list[0] == 0:
            raise ValueError("The block cannot start and end with 0")

        segments = []
        result = []

        for data in data_list:
            if data != 0:
                segments.append(data)
            else:
                if segments:
                    segments.sort()
                    result.append("".join(str(num) for num in segments))
                    segments = []
                else:
                    result.append('x')

        if segments:
            segments.sort()
            result.append(''.join(str(num) for num in segments))
        else:
            result.append('x')
        return " ".join(result)

    @classmethod
    def get_input_data(cls, event: any):
        return json.loads(event) if type(event) is str else event

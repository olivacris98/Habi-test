from Utils.Constant import ONLY_VIEW_STATUS, OPTIONAL_PARAMS


class Tools:
    def __init__(self):
        pass

    @staticmethod
    def get_request_method(event) -> dict:
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
        return event[method] if event.get(method) else {}

    @staticmethod
    def get_json_data() -> dict:
        """
        Load JSON data from the file.
        Returns:
            dict: The JSON data.
        """
        import json
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
        where_conditions = []
        for key, value in conditions.items():

            # getting filters
            if key == 'status_id' and int(value) in ONLY_VIEW_STATUS:
                where_conditions.append(f"sh.{key} = {value}")

            elif key in OPTIONAL_PARAMS:
                where_conditions.append(
                    f"p.{key} LIKE '%{str(value).lower()}%'"
                )

        return (
            "WHERE " + " AND ".join(where_conditions)
            if where_conditions else ""
        )

import json
from Utils.Tools import Tools


class BlockNumber:
    """
    class responsible operations with list of data numbers
    for test in habi
    """

    def __init__(self):
        self.utils = Tools()

    def operation_block(self, event) -> dict:
        """
        process all number into in list
        of data and return string with information segmented
        Args:
            event (dict): The event object.
        Returns:
            dict: Aws lambda response
        """
        status_code = 200
        result = []
        try:
            input_data = self.utils.get_request_method(event)
            self.utils.process_input(input_data)
            result = self.utils.process_block(input_data["list_of_data"])
        except ValueError as er:
            result = str(er)
            status_code = 400

        return {"statusCode": status_code, "body": json.dumps(result)}

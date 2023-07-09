from .Abstract import Abstract
from Utils.Tools import Tools


class Property(Abstract):
    """
    class responsible operations in Property habi.
    """
    def __init__(self, db):
        self.db = db
        self.utils = Tools()

    def get(self, event) -> dict:
        """
        get all property by params sended by request or data json
        only by status (en_)
            (this params be contained in database)
        Args:
            event (dict): The event object.
        Returns:
            dict: Aws lambda response
        """
        import json
        result = []
        status_code = 404

        # getting request data
        input_data = self.utils.get_request_method(event)
        json_data = self.utils.get_json_data()

        # statement by test
        stmt = """
            SELECT p.address, p.city, s.name AS STATUS
            FROM property p
            INNER JOIN status_history sh ON sh.property_id = p.id AND sh.id = (
                SELECT MAX(id) AS max_id
                FROM status_history
                WHERE property_id = p.id
            )
            INNER JOIN status s ON s.id = sh.status_id
        """

        # getting condition by two ways
        stmt += self.utils.get_condition(input_data or json_data)
        properties = self.db.all(stmt)

        if properties:
            status_code = 200
            result = properties

        return {"statusCode": status_code, "body": json.dumps(result)}

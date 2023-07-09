from Classes.Property import Property
from Utils.Database import Database


def get_property(event, context):
    conn = Database()
    property_instance = Property(conn)

    http_methods = {
        "GET": property_instance.get,
    }

    http_method = event.get("httpMethod", "GET")
    method_executed = http_methods.get(http_method, property_instance.get)

    return method_executed(event)

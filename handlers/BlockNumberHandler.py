from Classes.BlockNumber import BlockNumber


def block_operation(event, context):
    block_number = BlockNumber()

    http_methods = {
        "POST": block_number.operation_block,
    }

    print("HANDLER")

    http_method = event.get("httpMethod", "POST")
    method_executed = http_methods.get(http_method)

    return method_executed(event)

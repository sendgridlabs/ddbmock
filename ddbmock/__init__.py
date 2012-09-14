from pyramid.config import Configurator

# Main Application
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    # Decipher DynamoDB routes

    config.add_tween('ddbmock.router.dynamodb.dynamodb_router_factory')
    # Add routes
    config.add_route('batch_get_item', '/BatchGetItem')
    config.add_route('batch_write_item', '/BatchWriteItem')
    config.add_route('create_table', '/CreateTable')
    config.add_route('delete_item', '/DeleteItem')
    config.add_route('delete_table', '/DeleteTable')
    config.add_route('describe_table', '/DescribeTable')
    config.add_route('get_item', '/GetItem')
    config.add_route('list_tables', '/ListTables')
    config.add_route('put_item,', '/PutItem')
    config.add_route('query', '/Query')
    config.add_route('scan', '/Scan')
    config.add_route('update_item', '/UpdateItem')
    config.add_route('update_table', '/UpdateTable')

    config.scan()
    return config.make_wsgi_app()

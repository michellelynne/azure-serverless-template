import json
import logging
import os

import azure.functions as func
from azure.cosmos import cosmos_client


def main(request: func.HttpRequest, outdoc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function to CosmosDB.')
    logging.info(request.route_params)
    if request.method == 'GET':
        item_id = request.route_params.get('id')
        if item_id:
            return func.HttpResponse(json.dumps(get_item_from_collection(item_id)))
        else:
            return func.HttpResponse(json.dumps(get_items_from_collection()))
    elif request.method == 'POST':
        outdata = {'items': [request.get_json()]}
        outdoc.set(func.Document.from_json(json.dumps(outdata)))
        return func.HttpResponse(json.dumps(outdata))
    elif request.method == 'PUT':
        item_id = request.params.get('id')
        _item = request.get_json()
        _item['id'] = item_id
        outdata = {'items': [_item]}
        outdoc.set(func.Document.from_json(json.dumps(outdata)))
        return func.HttpResponse(json.dumps(outdata))


def get_cosmos_client():
    """Get the client for all CosmosDB queries.

    Returns:
        CosmosClient

    """
    return cosmos_client.CosmosClient(
        url_connection=os.getenv('CosmosDBHost'),
        auth={'masterKey': os.getenv('CosmosDBMasterKey')}
    )


def get_items_from_collection():
    """Get all items from a collection.

    Returns:
        List<dict>: All items from a collection.
    """
    collection = get_collection()
    client = get_cosmos_client()
    result_iterable = client.QueryItems(
        collection['_self'],
        {'query': 'SELECT * FROM server c'},
        {'enableCrossPartitionQuery': True}
    )
    return [i for i in iter(result_iterable)]


def get_item_from_collection(item_id):
    """Get an item from a collection by an ID.

    Args:
        item_id(str): An item id.

    Returns:
        dict: Single item from a collection.
    """
    collection = get_collection()
    client = get_cosmos_client()
    result_iterable = client.QueryItems(
        collection['_self'],
        {'query': 'SELECT * FROM server c WHERE c.id = \"{}\"'.format(item_id)},
        {'enableCrossPartitionQuery': True}
    )
    return [i for i in iter(result_iterable)][0]


def get_collection():
    """Get the collection the item is in."""
    database_id = os.getenv('DatabaseID')
    collection_id = os.getenv('CollectionID')
    collection_link = 'dbs/{}/colls/{}'.format(database_id, collection_id)
    client = get_cosmos_client()
    return client.ReadContainer(collection_link)

#
# def main(mytimer: func.TimerRequest, outdoc: func.Out[func.Document]):
#     utc_timestamp = datetime.datetime.utcnow().replace(
#         tzinfo=datetime.timezone.utc).isoformat()
#     if mytimer.past_due:
#         logging.info('The timer is past due!')
#     logging.info('Python timer trigger function ran at %s', utc_timestamp)
#
#     try:
#         # Get Blog feeds
#         outdata = {}
#         outdata['items'] = get_feed()
#         # logging.info(outdata)  # for debug
#
#         # Store output data using Cosmos DB output binding
#         outdoc.set(func.Document.from_json(json.dumps(outdata)))
#     except Exception as e:
#         logging.error('Error:')
# logging.error(e)
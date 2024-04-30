import logging

import db_utils
import utils

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler_get(event):
    route_key = event.get('routeKey')
    if route_key == 'GET /expense/{id}':
        id = event.get('pathParameters').get('id')
        expense = db_utils.get_item(key={'id': id})
        if not expense:
            return utils.set_response(404, 'Not Found (expense)')
        return utils.set_response(200, expense)
    return utils.set_response(200, db_utils.get_items())

def handler_post(event):
    expense = utils.get_body(event)
    if not expense:
        return utils.set_response(400, 'Bad Request (No body)')
    
    return utils.set_response(201, db_utils.put_item(expense))

def handler(event, context):
    logger.info(f'Event: {event}')
    method = event.get('requestContext').get('http', {}).get('method')
    logger.info('Method: %s', method)

    if method == 'GET':
        return handler_get(event)
    elif method == 'POST':
        return handler_post(event)
    else:
        return utils.set_response(400, 'Bad Request (Not supported method)')
import logging

import utils
from services.expenses_service import ExpensesService, ExpensesState
from user_info import UserInfo

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def __is_get_by_id(event):
    route_key = event.get('routeKey')
    return route_key == 'GET /expense/{id}'

def __is_approval(event):
    route_key = event.get('routeKey')
    return route_key == 'POST /expense/{id}/approve'

def __is_rejection(event):
    route_key = event.get('routeKey')
    return route_key == 'POST /expense/{id}/reject'

def handler_get(event):

    service = ExpensesService()

    if __is_get_by_id(event):
        id = event.get('pathParameters').get('id')
        expense = service.get_by_id(id)
        if not expense:
            return utils.set_response(404, 'Not Found (expense)')
        return utils.set_response(200, expense)
    
    return utils.set_response(200, service.get_all())

def handler_post(event):
    if __is_approval(event) or __is_rejection(event):
        id = event.get('pathParameters').get('id')
        service = ExpensesService()
        state = ExpensesState.APPROVED if __is_approval(event) else ExpensesState.REJECTED
        expense = service.mark_as(id, state)
        return utils.set_response(200, expense)

    expense = utils.get_body(event)
    if not expense:
        return utils.set_response(400, 'Bad Request (No body)')
    
    user_service = UserInfo()
    sub = event.get('requestContext').get('authorizer').get('jwt').get('claims').get('sub')
    user_info = user_service.get_user_by_id(sub)

    service = ExpensesService()
    expense = service.add_expense(expense.get('amount'),
                                  expense.get('date'),
                                  expense.get('description'),
                                  user_info.get('email'))

    return utils.set_response(201, expense)

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